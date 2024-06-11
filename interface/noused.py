
# ############################################################
# requête SPARQL pour récupérer les données d'une entité ########
# ############################################################

# from flask import Flask, render_template, request
# import requests as rq

# app = Flask(__name__)

# endpoint = "https://alpes-transport-sandbox.wikibase.cloud/w/api.php?"

# @app.route("/")
# def home():
#     return render_template("index.html")


# @app.route("/search")
# def search():
#     # Obtenir la requête de recherche de l'utilisateur
#     item = request.args.get("item")
#     # Envoyer une requête GET pour récupérer les entités correspondant à la requête de recherche
#     a = rq.get(endpoint + "action=wbsearchentities&format=json&language=fr&type=item&utf8=1&search=" + item)
#     # Extraire l'ID de l'entité correspondante à la requête de recherche
#     print(a.json())
#     entity_id = a.json()["search"][0]["id"]
#     # Envoyer une requête GET pour récupérer les données de l'entité correspondante à l'ID
#     r = rq.get(endpoint + f"action=wbgetclaims&format=json&entity={entity_id}&property=P31")
#     # Extraire les informations de déclarations de l'entité
#     entity_claims = r.json()["claims"]
#     # Récupérer les entités correspondant à la propriété "est un arrêt" (Q11482705)
#     arret_claim = None
#     for claim in entity_claims.get("P31", []):
#         if claim["mainsnak"]["datavalue"]["value"]["id"] == "Q11482705":
#             arret_claim = claim
#             break
#     # Récupérer les entités correspondant à la propriété "situer sur la ligne" (P81) de l'arrêt
#     line_claims = []
#     if arret_claim is not None:
#         for qualifier in arret_claim["qualifiers"].get("P81", []):
#             line_id = qualifier["datavalue"]["value"]["id"]
#             r = rq.get(endpoint + f"action=wbgetentities&format=json&ids={line_id}&props=labels&languages=fr")
#             line_label = r.json()["entities"][line_id]["labels"]["fr"]["value"]
#             line_claims.append(line_label)
#     # Extraire la description de l'entité
#     entity_description = a.json()["search"][0]["description"]
#     # Renvoyer les résultats de la requête dans un template
#     return render_template("search_par_API.html", results=a.json(), arret_claims=line_claims, entity_description=entity_description)

# if __name__ == "__main__":
#     app.run(debug=True)


################################################################
# requête SPARQL pour récupérer les données d'une entité #######
################################################################
# from flask import Flask, render_template, request
# import requests as rq
# import json

# app = Flask(__name__)

# endpoint = "https://alpes-transport-sandbox.wikibase.cloud/query/sparql?"

# @app.route("/")
# def home():
#     return render_template("index.html")


# @app.route("/search")
# def search():
#     # Obtenir la requête de recherche de l'utilisateur
#     item = request.args.get("item")
#     # Construire la requête SPARQL pour récupérer les informations de l'entité correspondante à la requête de recherche
#     query = """
#         PREFIX schema: <http://schema.org/>
#         PREFIX wd: <http://www.wikidata.org/entity/>
#         PREFIX wdt: <http://www.wikidata.org/prop/direct/>
#         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

#         SELECT ?entity ?entityLabel ?description ?claims WHERE {{
#             ?entity schema:name ?item.
#             ?entity rdfs:label ?entityLabel filter (lang(?entityLabel) = "fr").
#             ?entity schema:description ?description filter (lang(?description) = "fr").
#             ?entity ?p ?o.
#             OPTIONAL {{
#                 ?entity ?p ?s.
#                 ?s wdt:P31 wd:Q16521.
#             }}
#             SERVICE wikibase:label {{ bd:serviceParam wikibase:language "fr". }}
#             FILTER (REGEX(?item, "{}", "i"))
#         }}
#     """.format(item)

#     # Envoyer une requête POST pour exécuter la requête SPARQL
#     response = rq.post(endpoint, data={"query": query})

#     # Vérifier que la réponse est en JSON valide avant de l'extraire
#     try:
#         json_response = response.json()
#         if "results" not in json_response:
#             raise Exception("Response does not contain results")
#         results = json_response["results"]["bindings"]
#     except (json.decoder.JSONDecodeError, Exception) as e:
#         print(f"Error: {e}")
#         results = []

#     # Renvoyer les résultats de la requête dans un template
#     return render_template("search_par_SPARQL.html", results=results)

# if __name__ == "__main__":
#     app.run(debug=True)
