import json
from flask import Flask, render_template, request
import requests as rq
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
endpoint = "https://alpes-transport-sandbox.wikibase.cloud/w/api.php?"


@app.route("/")
def home():
    return render_template("index.html")


def list_arrets():
    props_arrets = ["P282", "P291", "P315", "P317",
                            "P319", "P321", "P323", "P325", "P327", "P329", "P331", "P333", "P335", "P337", "P339", "P341", "P343", "P345", "P347", "P349", "P351", "P353", "P355", "P357", "P359", "P361", "P363", "P365", "P367", "P369", "P371", "P463"]
    return props_arrets


def list_horraires():
    props_horraires = ["P312", "P896", "P316", "P318", "P320", "P322", "P324", "P326", "P328", "P330", "P332", "P334", "P336", "P338", "P340",
                       "P342", "P344", "P346", "P348", "P350", "P352", "P354", "P356", "P358", "P360", "P362", "P364", "P366", "P368", "P370", "P372", "P374"]
    return props_horraires


@app.route("/search")
def search():

    selected_props = None
    selected_props = [request.args.get('depart'), request.args.get('arrivee')]
    print(selected_props)
    coordinates = []
    noms_arrets = []
    property_arrets = []
    horaires_arrets = {}
    moyen_transport = {}
    list_items_labels = []
    arrets = []
    for i in range(len(selected_props)):
        # Envoyer une requête GET pour récupérer les entités correspondant à la requête de recherche
        if (selected_props[i] == None or selected_props[i] == ''):
            if (i + 1) < len(selected_props) and (selected_props[i+1] is None or selected_props[i+1] == ''):
                break
            if (i + 1) < len(selected_props):
                selected_props[i] = selected_props[i+1]

        else:
            a = rq.get(
                endpoint + "action=wbsearchentities&format=json&language=fr&type=item&search=" + selected_props[i])
            print(selected_props[i])
            if not a.json()["search"]:
                return render_template("404.html")
            # Extraire l'ID de l'entité correspondante à la requête de recherche
            entity_id = a.json()["search"][0]["id"]

            # Envoyer une requête GET pour récupérer les données de l'entité correspondante à l'ID
            r = rq.get(endpoint + "action=wbgetentities&format=json&ids=" +
                    entity_id + "&props=claims|labels&languages=fr")
            # Extraire les informations de déclarations et de description de l'entité
            # print(r.json())
            itineraire_obtenu = r.json()[
                "entities"][entity_id]["claims"]["P1248"][0]["mainsnak"]["datavalue"]["value"]
            r = rq.get(endpoint + "action=wbgetentities&format=json&ids=" +
                    itineraire_obtenu + "&props=claims|labels&languages=fr")
            # Extraire les informations de déclarations et de description de l'entité
            entity_claims = r.json()["entities"][itineraire_obtenu]["claims"]
            item_labels = r.json()[
                "entities"][itineraire_obtenu]["labels"]["fr"]["value"]
            list_items_labels.append(item_labels)

            props_arrets = list_arrets()
            props_horraires = list_horraires()

            for prop_id, prop_claims in entity_claims.items():
                if prop_id in props_arrets:
                    for claim in prop_claims:
                        if "mainsnak" in claim and "datavalue" in claim["mainsnak"] and claim["mainsnak"]["datavalue"]["type"] == "string":
                            temp_id = claim["mainsnak"]["datavalue"]["value"]
                            item_data = rq.get(
                                endpoint + "action=wbgetentities&format=json&ids=" + temp_id + "&props=claims|labels&languages=fr")
                            lons = float(item_data.json()[
                                "entities"][temp_id]["claims"]["P468"][0]["mainsnak"]["datavalue"]["value"])
                            lats = float(item_data.json()[
                                "entities"][temp_id]["claims"]["P473"][0]["mainsnak"]["datavalue"]["value"])

                            prop_data = rq.get(endpoint + "action=wbgetentities&format=json&ids=" +
                                            prop_id + "&props=claims|labels&languages=fr")

                            arrets.append({
                                'prop_id': prop_id,
                                'name': item_data.json()["entities"][temp_id]["labels"]["fr"]["value"],
                                'coord': [lons, lats],
                                'property_label': prop_data.json()["entities"][prop_id]["labels"]["fr"]["value"]
                            })

                # pour les horaires
                if prop_id in props_horraires:
                    for claim in prop_claims:
                        horaires_arrets[prop_id] = claim["mainsnak"]["datavalue"]["value"]

                # pour les moyens de transport
                if prop_id == "P280":
                    for claim in prop_claims:
                        moyen_transport[prop_id] = claim["mainsnak"]["datavalue"]["value"]

    arrets.sort(key=lambda x: props_arrets.index(x['prop_id']))
    coordinates = [arret['coord'] for arret in arrets]
    noms_arrets = [arret['name'] for arret in arrets]
    property_arrets = [arret['property_label'] for arret in arrets]
    moyen_transport = list(moyen_transport.values())
    horaires_arrets = list(horaires_arrets.values())

    return render_template("search_par_API.html", 
                           property_arrets=json.dumps(property_arrets), 
                           horaires_arrets=json.dumps(horaires_arrets), 
                           moyen_transport=json.dumps(moyen_transport), 
                           item_labels=list_items_labels,
                           noms_arrets=json.dumps(noms_arrets), 
                           coordinates=json.dumps(coordinates))


if __name__ == "__main__":
    app.run(debug=True)
