# from wikibaseintegrator.wbi_config import config as wbi_config_dict
# from wikibaseintegrator.entities.item import ItemEntity
# from wikibaseintegrator.models.labels import Labels as newLabel
# from wikibaseintegrator.models.descriptions import Descriptions as newDescription
# from AlpesTransportWikibaseIntegratorWrapper import AlpesTransportWiki
# import csv

# # Create an instance of the AlpesTransportWiki class
# bot = AlpesTransportWiki(wikibase_url=wbi_config_dict['MEDIAWIKI_API_URL'],
#                           wikibase_user='william',
#                           wikibase_password='william-bot@88hd7lft423pdnt5f95ijnoq8lccliae')

# # Define the items and properties
# properties = {
#     "route_short_name": "string",
#     "route_long_name": "string",
#     "route_type": "string",
#     "route_color": "string",
#     "route_text_color": "string",
#     "trip_headsign": "string",
#     "wheelchair_accessible": "string",
#     "bikes_allowed": "string",
#     "date": "string",
#     "exception_type": "string",
#     "arrival_time": "string",
#     "departure_time": "string",
#     "stop_sequence": "string",
#     "pickup_type": "string",
#     "drop_off_type": "string",
#     "stop_name": "string",
#     "stop_lat": "string",
#     "stop_lon": "string",
#     "location_type": "string"
# }

# items = {
#     "route_id": "identifiant de la route",
#     "agency_id": "identifiant de l'agence",
#     "service_id": "identifiant du service",
#     "trip_id": "identifiant du trajet",
#     "direction_id": "identifiant de la direction",
#     "block_id": "identifiant du bloc",
#     "stop_id": "identifiant de l'arrêt"
# }

# # Create the properties
# for pid, ptype in properties.items():
#     bot.create_property(pid, ptype)

# # Create the items
# for iid, desc in items.items():
#     bot.create_item(iid, desc)

# # Read the data from the CSV file
# with open('merged.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         # Create a new item for the row
#         item_data = {}
#         for key, value in row.items():
#             item_data[key] = value

#         # Add the item to Wikibase
#         item = ItemEntity(data=item_data, mediawiki_api_url=wbi_config_dict['MEDIAWIKI_API_URL'])
#         item.set_label(row['route_short_name'], lang='fr')
#         item.set_description(row['route_long_name'], lang='fr')
#         item.write(login_instance=bot.login_instance)

# print("Successfully added data to Wikibase!")
import requests
import json
from AlpesTransport_config import endpoint, username, password

# Paramètres de connexion à l'API MediaWiki
mediawiki_api_url = "https://alpes-transport-sandbox.wikibase.cloud/w/api.php"
mediawiki_username = username#"Mohamed"
mediawiki_password = password#"alpestransport"

# Fonction pour effectuer une requête POST à l'API MediaWiki
def post_request(params):
    response = requests.post(mediawiki_api_url, data=params)
    response.raise_for_status()
    return json.loads(response.text)

# Connexion à l'API MediaWiki
login_params = {
    "action": "login",
    "format": "json",
    "lgname": mediawiki_username,
    "lgpassword": mediawiki_password
}
login_response = post_request(login_params)
login_token = login_response["login"]["token"]
login_params["lgtoken"] = login_token
post_request(login_params)

# Fonction pour créer une propriété
def create_property(pid, label, description, datatype):
    create_property_params = {
        "action": "wbeditentity",
        "format": "json",
        "new": datatype,
        "data": json.dumps({
            "labels": {
                "en": {
                    "language": "en",
                    "value": label
                }
            },
            "descriptions": {
                "en": {
                    "language": "en",
                    "value": description
                }
            }
        }),
        "token": login_token
    }
    if datatype == "string":
        create_property_params["datatype"] = "string"
    elif datatype == "item":
        create_property_params["datatype"] = "wikibase-item"
    post_request(create_property_params)

# Fonction pour créer un élément
def create_item(iid, label, description):
    create_item_params = {
        "action": "wbeditentity",
        "format": "json",
        "new": "item",
        "data": json.dumps({
            "labels": {
                "en": {
                    "language": "en",
                    "value": label
                }
            },
            "descriptions": {
                "en": {
                    "language": "en",
                    "value": description
                }
            }
        }),
        "token": login_token
    }
    post_request(create_item_params)

# Exemple d'utilisation pour créer une propriété et un élément
create_property("P1", "Route ID", "The unique identifier of a transit route","string")
create_item("Q1", "Example Route", "An example transit route")

create_property("P2", "Agency ID", "The unique identifier of a transit agency","string")
create_item("Q2", "Example Agency", "An example transit agency")

create_property("P3", "Route Short Name", "The short name of a transit route","string")
create_item("Q3", "Example Route Short Name", "An example transit route short name")

create_property("P4", "Route Long Name", "The long name of a transit route","string")
create_item("Q4", "Example Route Long Name", "An example transit route long name")

