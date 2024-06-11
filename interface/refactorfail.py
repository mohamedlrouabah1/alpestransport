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

@app.route("/search")
def search():
    def get_data(search_param):
        a = rq.get(endpoint + "action=wbsearchentities&format=json&language=fr&type=item&utf8=1&search=" + search_param)
        entity_id = a.json()["search"][0]["id"]
        r = rq.get(endpoint + "action=wbgetentities&format=json&ids=" + entity_id + "&props=claims|labels&languages=fr")
        itineraire_obtenu = r.json()["entities"][entity_id]["claims"]["P1248"][0]["mainsnak"]["datavalue"]["value"]
        return rq.get(endpoint + "action=wbgetentities&format=json&ids=" + itineraire_obtenu + "&props=claims|labels&languages=fr")

    selected_props, option_props = request.args.get('depart'), request.args.get('arrivee')
    r, r2 = get_data(selected_props), (get_data(option_props) if option_props is not None else None)

    def process_data(r):
        entity_id = list(r.json()["entities"].keys())[0]
        entity_claims, item_labels = r.json()["entities"][entity_id]["claims"], r.json()["entities"][entity_id]["labels"]["fr"]["value"]
        props_arrets, props_horraires = ["P282", "P291", "P315", "P317", "P319", "P321", "P323", "P325", "P327", "P329", "P331", "P333", "P335", "P337", "P339", "P341", "P343", "P345", "P347", "P349", "P351", "P353", "P355", "P357", "P359", "P361", "P363", "P365", "P367", "P369", "P371", "P463"], ["P312", "P896", "P316", "P318", "P320", "P322", "P324", "P326", "P328", "P330", "P332", "P334", "P336", "P338", "P340", "P342", "P344", "P346", "P348", "P350", "P352", "P354", "P356", "P358", "P360", "P362", "P364", "P366", "P368", "P370", "P372", "P374"]
        arrets, horaires_arrets, moyen_transport = [], {}, {}
        for prop_id, prop_claims in entity_claims.items():
            for claim in prop_claims:
                if prop_id in props_arrets and "mainsnak" in claim and "datavalue" in claim["mainsnak"] and claim["mainsnak"]["datavalue"]["type"] == "string":
                    temp_id = claim["mainsnak"]["datavalue"]["value"]
                    item_data = rq.get(endpoint + "action=wbgetentities&format=json&ids=" + temp_id + "&props=claims|labels&languages=fr")
                    lons, lats = float(item_data.json()["entities"][temp_id]["claims"]["P1687"][0]["mainsnak"]["datavalue"]["value"]["longitude"]), float(item_data.json()["entities"][temp_id]["claims"]["P1687"][0]["mainsnak"]["datavalue"]["value"]["latitude"])

                    prop_data = rq.get(endpoint + "action=wbgetentities&format=json&ids=" +
                                       prop_id + "&props=claims|labels&languages=fr")

                    arrets.append({
                        'prop_id': prop_id,
                        'name': item_data.json()["entities"][temp_id]["labels"]["fr"]["value"],
                        'coord': [lons, lats],
                        'property_label': prop_data.json()["entities"][prop_id]["labels"]["fr"]["value"]
                    })

        process_data(r)
        return json.dumps({"arrets": arrets, "horaires_arrets": horaires_arrets, "moyen_transport": moyen_transport})

if __name__ == "__main__":
    app.run(debug=True)

