import json
from functools import partial
from collections import OrderedDict
import requests as rq
from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
endpoint = "https://alpes-transport-sandbox.wikibase.cloud/w/api.php?"


@app.route("/")
def home():
    return render_template("index.html")

def wbget_url(ids):
        return rq.get(endpoint + "action=wbgetentities&format=json&ids=" +
                      ids + "&props=claims|labels&languages=fr")

@app.route("/search")
def search():

    depart_input = request.args.get("depart")
    arrivee_input = request.args.get("arrivee")
    transport_mode = request.args.get('transport_mode')


    if arrivee_input is not None and depart_input is not None:
        a = rq.get(
        endpoint + "action=wbsearchentities&format=json&language=fr&type=item&utf8=1&search=" + arrivee_input)
        entity_id = a.json()["search"][0]["id"]

        r = wbget_url(ids=entity_id)
        claims = r.json()["entities"][entity_id]["claims"]

        itineraire_obtenu = claims["P1248"][0]["mainsnak"]["datavalue"]["value"]
        r = wbget_url(ids=itineraire_obtenu)

        entity_claims = r.json()["entities"][itineraire_obtenu]["claims"]
        item_labels = r.json()[
            "entities"][itineraire_obtenu]["labels"]["fr"]["value"]

        if transport_mode == 'stas':
            props_arrets = ["P282", "P291", "P315", "P317",
                            "P319", "P321", "P323", "P325","P327","P329","P331","P333","P335","P337","P339","P341","P343","P345","P347","P349","P351","P353","P355","P357","P359","P361","P363","P365","P367","P369","P371","P463"]
            props_horraires = ["P312", "P896", "P316", "P318","P320","P322","P324","P326","P328","P330","P332","P334","P336","P338","P340","P342","P344","P346","P348","P350","P352","P354","P356","P358","P360","P362","P364","P366","P368","P370","P372","P374"]
        elif transport_mode == 'sncf':
            props_arrets = ["P282", "P291", "P315", "P317",
                        "P319", "P321", "P323", "P325", "P463"]
            props_horraires = ["P312", "P896", "P316", "P318",
                        "P320", "P322", "P324", "P326", "P328"]
        else : 
            props_arrets = ["P282", "P291", "P315", "P317",
                        "P319", "P321", "P323", "P325", "P463"]
            props_horraires = ["P312", "P896", "P316", "P318",
                        "P320", "P322", "P324", "P326", "P328"]

        filtered_claims = OrderedDict((prop_id, prop_claims) for prop_id, prop_claims in entity_claims.items(
        ) if prop_id in props_arrets + props_horraires)
        property_labels = OrderedDict((prop_id, wbget_url(ids=prop_id).json()["entities"][prop_id]["labels"]["fr"]["value"]) for prop_id in props_arrets)
        tmp_list, coordinates, noms_arrets = OrderedDict(), [], []
        horaires_arrets, moyen_transport = OrderedDict(), OrderedDict()

        # Pour conserver l'ordre des coordonnées en fonction de l'ordre d'entrée des props_arrets
        coordinates = OrderedDict((prop_id, []) for prop_id in props_arrets)

        for prop_id, prop_claims in entity_claims.items():
            # pour les arrêts
            if prop_id in props_arrets:
                filtered_claims[prop_id] = prop_claims
                for claim in prop_claims:
                    if "mainsnak" in claim and "datavalue" in claim["mainsnak"] and claim["mainsnak"]["datavalue"]["type"] == "string":
                        temp_id = claim["mainsnak"]["datavalue"]["value"]
                        item_data = wbget_url(ids=temp_id).json()["entities"][temp_id]
                        tmp_list[prop_id] = item_data["labels"]["fr"]["value"]
                        lons = item_data["claims"]["P468"][0]["mainsnak"]["datavalue"]["value"]
                        lats = item_data["claims"]["P473"][0]["mainsnak"]["datavalue"]["value"]
                        coordinates[prop_id].append([lons, lats])
                        noms_arrets.append(item_data["labels"]["fr"]["value"])
            # pour les horaires
            if prop_id in props_horraires:
                horaires_arrets[prop_id] = prop_claims[0]["mainsnak"]["datavalue"]["value"]
            
            # pour les moyens de transport
            if prop_id == "P280":
                moyen_transport[prop_id] = prop_claims[0]["mainsnak"]["datavalue"]["value"]
    if depart_input is not None and arrivee_input is None:
        a = rq.get(
        endpoint + "action=wbsearchentities&format=json&language=fr&type=item&utf8=1&search=" + depart_input)
        entity_id = a.json()["search"][0]["id"]

        r = wbget_url(ids=entity_id)
        claims = r.json()["entities"][entity_id]["claims"]

        itineraire_obtenu = claims["P1248"][0]["mainsnak"]["datavalue"]["value"]
        r = wbget_url(ids=itineraire_obtenu)

        entity_claims = r.json()["entities"][itineraire_obtenu]["claims"]
        item_labels = r.json()[
            "entities"][itineraire_obtenu]["labels"]["fr"]["value"]

        if transport_mode == 'stas':
            props_arrets = ["P282", "P291", "P315", "P317",
                            "P319", "P321", "P323", "P325","P327","P329","P331","P333","P335","P337","P339","P341","P343","P345","P347","P349","P351","P353","P355","P357","P359","P361","P363","P365","P367","P369","P371","P463"]
            props_horraires = ["P312", "P896", "P316", "P318","P320","P322","P324","P326","P328","P330","P332","P334","P336","P338","P340","P342","P344","P346","P348","P350","P352","P354","P356","P358","P360","P362","P364","P366","P368","P370","P372","P374"]
        elif transport_mode == 'sncf':
            props_arrets = ["P282", "P291", "P315", "P317",
                        "P319", "P321", "P323", "P325", "P463"]
            props_horraires = ["P312", "P896", "P316", "P318",
                        "P320", "P322", "P324", "P326", "P328"]
        else : 
            props_arrets = ["P282", "P291", "P315", "P317",
                        "P319", "P321", "P323", "P325", "P463"]
            props_horraires = ["P312", "P896", "P316", "P318",
                        "P320", "P322", "P324", "P326", "P328"]

        filtered_claims = OrderedDict((prop_id, prop_claims) for prop_id, prop_claims in entity_claims.items(
        ) if prop_id in props_arrets + props_horraires)
        property_labels = OrderedDict((prop_id, wbget_url(ids=prop_id).json()["entities"][prop_id]["labels"]["fr"]["value"]) for prop_id in props_arrets)
        tmp_list, coordinates, noms_arrets = OrderedDict(), [], []
        horaires_arrets, moyen_transport = OrderedDict(), OrderedDict()

        # Pour conserver l'ordre des coordonnées en fonction de l'ordre d'entrée des props_arrets
        coordinates = OrderedDict((prop_id, []) for prop_id in props_arrets)

        for prop_id, prop_claims in entity_claims.items():
            # pour les arrêts
            if prop_id in props_arrets:
                filtered_claims[prop_id] = prop_claims
                for claim in prop_claims:
                    if "mainsnak" in claim and "datavalue" in claim["mainsnak"] and claim["mainsnak"]["datavalue"]["type"] == "string":
                        temp_id = claim["mainsnak"]["datavalue"]["value"]
                        item_data = wbget_url(ids=temp_id).json()["entities"][temp_id]
                        tmp_list[prop_id] = item_data["labels"]["fr"]["value"]
                        lons = item_data["claims"]["P468"][0]["mainsnak"]["datavalue"]["value"]
                        lats = item_data["claims"]["P473"][0]["mainsnak"]["datavalue"]["value"]
                        coordinates[prop_id].append([lons, lats])
                        noms_arrets.append(item_data["labels"]["fr"]["value"])
            # pour les horaires
            if prop_id in props_horraires:
                horaires_arrets[prop_id] = prop_claims[0]["mainsnak"]["datavalue"]["value"]
            
            # pour les moyens de transport
            if prop_id == "P280":
                moyen_transport[prop_id] = prop_claims[0]["mainsnak"]["datavalue"]["value"]

    if depart_input is None and arrivee_input is not None:
        a = rq.get(
        endpoint + "action=wbsearchentities&format=json&language=fr&type=item&utf8=1&search=" + arrivee_input)
        entity_id = a.json()["search"][0]["id"]

        r = wbget_url(ids=entity_id)
        claims = r.json()["entities"][entity_id]["claims"]

        itineraire_obtenu = claims["P1248"][0]["mainsnak"]["datavalue"]["value"]
        r = wbget_url(ids=itineraire_obtenu)

        entity_claims = r.json()["entities"][itineraire_obtenu]["claims"]
        item_labels = r.json()[
            "entities"][itineraire_obtenu]["labels"]["fr"]["value"]

        if transport_mode == 'stas':
            props_arrets = ["P282", "P291", "P315", "P317",
                            "P319", "P321", "P323", "P325","P327","P329","P331","P333","P335","P337","P339","P341","P343","P345","P347","P349","P351","P353","P355","P357","P359","P361","P363","P365","P367","P369","P371","P463"]
            props_horraires = ["P312", "P896", "P316", "P318","P320","P322","P324","P326","P328","P330","P332","P334","P336","P338","P340","P342","P344","P346","P348","P350","P352","P354","P356","P358","P360","P362","P364","P366","P368","P370","P372","P374"]
        elif transport_mode == 'sncf':
            props_arrets = ["P282", "P291", "P315", "P317",
                        "P319", "P321", "P323", "P325", "P463"]
            props_horraires = ["P312", "P896", "P316", "P318",
                        "P320", "P322", "P324", "P326", "P328"]
        else : 
            props_arrets = ["P282", "P291", "P315", "P317",
                        "P319", "P321", "P323", "P325", "P463"]
            props_horraires = ["P312", "P896", "P316", "P318",
                        "P320", "P322", "P324", "P326", "P328"]

        filtered_claims = OrderedDict((prop_id, prop_claims) for prop_id, prop_claims in entity_claims.items(
        ) if prop_id in props_arrets + props_horraires)
        property_labels = OrderedDict((prop_id, wbget_url(ids=prop_id).json()["entities"][prop_id]["labels"]["fr"]["value"]) for prop_id in props_arrets)
        tmp_list, coordinates, noms_arrets = OrderedDict(), [], []
        horaires_arrets, moyen_transport = OrderedDict(), OrderedDict()

        # Pour conserver l'ordre des coordonnées en fonction de l'ordre d'entrée des props_arrets
        coordinates = OrderedDict((prop_id, []) for prop_id in props_arrets)

        for prop_id, prop_claims in entity_claims.items():
            # pour les arrêts
            if prop_id in props_arrets:
                filtered_claims[prop_id] = prop_claims
                for claim in prop_claims:
                    if "mainsnak" in claim and "datavalue" in claim["mainsnak"] and claim["mainsnak"]["datavalue"]["type"] == "string":
                        temp_id = claim["mainsnak"]["datavalue"]["value"]
                        item_data = wbget_url(ids=temp_id).json()["entities"][temp_id]
                        tmp_list[prop_id] = item_data["labels"]["fr"]["value"]
                        lons = item_data["claims"]["P468"][0]["mainsnak"]["datavalue"]["value"]
                        lats = item_data["claims"]["P473"][0]["mainsnak"]["datavalue"]["value"]
                        coordinates[prop_id].append([lons, lats])
                        noms_arrets.append(item_data["labels"]["fr"]["value"])
            # pour les horaires
            if prop_id in props_horraires:
                horaires_arrets[prop_id] = prop_claims[0]["mainsnak"]["datavalue"]["value"]
            
            # pour les moyens de transport
            if prop_id == "P280":
                moyen_transport[prop_id] = prop_claims[0]["mainsnak"]["datavalue"]["value"]
    # Renvoyer les résultats de la requête dans un template
    return render_template("search_par_API.html", results=r.json(), itineraire=a.json(), horaires_arrets=json.dumps(list(horaires_arrets.values())), moyen_transport=json.dumps(moyen_transport), entity_claims=filtered_claims, property_arrets=json.dumps(list(property_labels.values())), item_labels=item_labels, entity_id=entity_id, props_arrets=props_arrets, property_labels=property_labels, tmp_list=tmp_list, noms_arrets=json.dumps(noms_arrets), coordinates=json.dumps(list(coordinates.values())))

    

    

if __name__ == "__main__":
    app.run(debug=True)







