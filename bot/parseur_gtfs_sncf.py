if __name__ != "__main__":
    print(
        "The file parseur_gtfs is not yet a module you can import, please laucnh this program from the comand line"
    )

import pandas as pd
from zipfile import ZipFile

# variables à modifier pour adapter à d'autre fichiers gtfs
PATH = "../../data/SNCF/horraires/export-ter-gtfs-horraires-ter.zip"
TYPE_DE_TRANSPORT = "train"
NOM_AGENCE = "SNCF"
DEBUGG = True
proportion = 10000  # divide the number of rows by this number to skip
offset_proportion = 0  # number of rows * proportion to skip from the gtfs file

# declaration of variable used for storing the files from gtfs zip
routes_df = trips_df = stops_df = stop_times_df = None

# =================================================================#
#                                                                  #
#            SETP 1: LOADING DATA FROM GTFS ZIP FILE               #
#                                                                  #
# =================================================================#

# Chargement des contenus des fichiers dans un dataframe
with ZipFile(PATH) as myzip:
    myzip.printdir()
    myzip.namelist()

    routes_df = pd.read_csv(
        myzip.open("routes.txt"),
        dtype={
            "route_id": "str",
            "agency_id": "str",
            "route_short_name": "str",
            "route_long_name": "str",
            "route_desc": "str",
            "route_type": "Int64",
            "route_url": "str",
            "route_color": "str",
            "route_text_color": "str",
        },
    )

    trips_df = pd.read_csv(
        myzip.open("trips.txt"),
        dtype={
            "route_id": "str",
            "service_id": "str",
            "trip_id": "str",
            "trip_headsign": "str",
            "direction_id": "str",
            "block_id": "int64",
            "shape_id": "str",
        },
    )

    stops_df = pd.read_csv(
        myzip.open("stops.txt"),
        dtype={
            "stop_id": "str",
            "stop_name": "str",
            "stop_desc": "str",
            "stop_lat": "float64",
            "stop_lon": "float64",
            "zone_id": "str",
            "stop_url": "str",
            "location_type": "int64",
            "parent_station": "str",
        },
    )

    stop_times_df = pd.read_csv(
        myzip.open("stop_times.txt"),
        dtype={
            "trip_id": "str",
            "arrival_time": "str",
            "departure_time": "str",
            "stop_id": "str",
            "stop_sequence": "int64",
            "stop_headsign": "str",
            "pickup_type": "int64",
            "drop_off_type": "int64",
            "shape_dist_traveled": "float64",
        },
    )

# =================================================================#
#                                                                  #
#            SETP 2: CLEAN THE DATA                                #
#                                                                  #
# =================================================================#
# remove useless columns from each dataframe
try:
    del routes_df["agency_id"]
    del routes_df["route_url"]
    del routes_df["route_color"]
    del routes_df["route_text_color"]
    del routes_df["route_desc"]
    del routes_df["route_type"]
    del routes_df["route_short_name"]
except:
    if DEBUGG:
        print("Error while removing columns from routes_df")

try:
    del trips_df["shape_id"]
    del trips_df["service_id"]
    del trips_df["block_id"]
    del trips_df["trip_headsign"]
except:
    if DEBUGG:
        print("Error while removing columns from trips_df")

try:
    del stops_df["stop_desc"], stops_df["zone_id"], stops_df["stop_url"]
    del stops_df["location_type"]
except:
    if DEBUGG:
        print("Error while removing columns from stops_df")

try:
    del stop_times_df["departure_time"]  # because same as arrival_time
    del stop_times_df["stop_headsign"], stop_times_df["shape_dist_traveled"]
    del stop_times_df["pickup_type"], stop_times_df["drop_off_type"]
    del stop_times_df["stop_sequence"]
except:
    if DEBUGG:
        print("Error while removing columns from stop_times_df")


# =================================================================#
#                                                                  #
#            SETP 3: TRANSFROM THE DATA INTO A DICTIONNARY         #
#                                                                  #
# =================================================================#
from number_in_letter import number_in_letter

n1 = len(trips_df)
n1 /= proportion
i1 = offset_proportion * proportion

# liste des dictionnaires représentant les itinéraires pour l'agence de
# transport en commun considérée.
itineraire_dict = []


while i1 < n1:
    if DEBUGG:
        print("Tour de boucle ", i1, " sur ", n1)

    itineraire_route_id = trips_df.iloc[i1]["route_id"]
    itineraire_trip_id = trips_df.iloc[i1]["trip_id"]
    itineraire_direction_id = trips_df.iloc[i1]["direction_id"]
    i1 += 1

    horraires_arrets_de_l_itineraire = stop_times_df[
        stop_times_df["trip_id"] == itineraire_trip_id
    ]

    nb_horraires = len(horraires_arrets_de_l_itineraire)
    if nb_horraires > 25 and DEBUGG:
        print("Il y a ", nb_horraires, "arrêts dans cet itinéraire.")

    itineraire_property = []

    # We build the "horaire" entity
    i2 = 0
    nb_horraires = len(horraires_arrets_de_l_itineraire)

    # for horraire in horraires_arrets_de_l_itineraire:
    while i2 < nb_horraires:
        horraire = horraires_arrets_de_l_itineraire.iloc[i2]
        horraire_stop_id = horraire["stop_id"]
        horraire_trip_id = horraire["trip_id"]
        horraire_arrival_time = horraire["arrival_time"]

        # On construit l'item arrêt
        arret = stops_df[stops_df["stop_id"] == horraire_stop_id]
        arret_stop_id = arret["stop_id"]
        arret_stop_name = arret["stop_name"].values[0]
        arret_stop_lat = arret["stop_lat"].values[0]
        arret_stop_lon = arret["stop_lon"].values[0]
        arret_parent_station = arret["parent_station"]

        i2 += 1  # impoprtant de laiser l'incrémentation ici pour avoir le bon indice dans le tableau number_in_letter
        num_arret = number_in_letter[i2]
        if i2 == nb_horraires:
            num_arret = "dernier"

        # construit la propriété horraire
        horraire_property = {
            "entity": "property",
            "label": "horraire " + num_arret + " arret",
            "type": "string",
            "value": horraire_arrival_time,
        }
        itineraire_property += [horraire_property]

        # construit la propriété arret
        arret_property = {
            "entity": "property",
            "label": "s arrete en " + num_arret,
            "type": "item",
            "value": {
                "entity": "item",
                "label": arret_stop_name,
                "property": [
                    {
                        "entity": "property",
                        "label": "est un",
                        "type": "string",
                        "value": "arret",
                    },
                    {
                        "entity": "property",
                        "label": "a pour type arret",
                        "type": "string",
                        "value": "arret de " + TYPE_DE_TRANSPORT,
                    },
                    {
                        "entity": "property",
                        "label": "a pour longitude",
                        "type": "string",
                        "value": arret_stop_lon,
                    },
                    {
                        "entity": "property",
                        "label": "a pour latitude",
                        "type": "string",
                        "value": arret_stop_lat,
                    },
                ],
            },
        }
        itineraire_property += [arret_property]

    itineraire_property += [
        {
            "entity": "property",
            "label": "est un",
            "type": "string",
            "value": TYPE_DE_TRANSPORT,
        }
    ]
    # construit la propriété itineraire
    itineraire_dict += [
        {
            "entity": "item",
            "label": routes_df[routes_df["route_id"] == itineraire_route_id][
                "route_long_name"
            ].values[0],
            "property": itineraire_property,
        }
    ]


# lie les itinéraires à l'agence de transport en commun
intermediate_rdf_model = {
    "entity": "item",
    "label": NOM_AGENCE,
    "property": [
        {
            "entity": "property",
            "label": "est un",
            "type": "string",
            "value": "agence de transports en comun",
        },
        {
            "entity": "property",
            "label": "propose",
            "type": "listItem",
            "value": itineraire_dict,
        },
    ],
}


# debugg message, display the final dict:
if DEBUGG:
    # modules to make an indented display of dictionnarries. if needed for debbug
    import json

    print(json.dumps(intermediate_rdf_model, indent=4))


# =================================================================#
#                                                                  #
#            SETP 3: INSERT DATA INTO WIKIBASE                     #
#                                                                  #
# =================================================================#
from insert_data_wikibase import insert_data_wikibase
from AlpesTransport_config import endpoint, username, password
from AlpesTransportWikibaseIntegratorWrapper import AlpesTransportWiki

wiki = AlpesTransportWiki(endpoint, username, password)

insert_data_wikibase(intermediate_rdf_model, wiki, DEBUGG)

print(
    "Your data has been inserted into Wikibase '"
    + endpoint
    + "' with the user '"
    + username
    + "."
)
