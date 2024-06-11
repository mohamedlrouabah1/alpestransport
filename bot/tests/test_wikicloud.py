from AlpesTransportWikibaseIntegratorWrapper import AlpesTransportWiki
from AlpesTransport_config import endpoint, username, password

# from example_format_intermediaire import data
from insert_data_wikibase import insert_data_from_intermediate_format
import requests

# endpoint = "https://alpes-transport-sandbox.wikibase.cloud/w/api.php"
# username = "william"
# password = "william-bot@88hd7lft423pdnt5f95ijnoq8lccliae"

wiki = AlpesTransportWiki(endpoint, username, password)


id = wiki.get_property_id_by_name("a pour longitude")
print(id)

# wiki.create_statement(item_id="Q83", property_id="P311", statement_value=10)
exit(0)
url = endpoint
params = {
    "action": "wbcreateclaim",
    "format": "json",
    "entity": "Q83",
    "property": "P311",
    "value": '{"amount":"10.5", "unit":"1"}',
    "snaktype": "value",
    "token": wiki.wikibase_login.get_edit_token(),
}
print(wiki.wikibase_login.get_edit_token())
# Make API call
response = requests.post(url, data=params)

# Check if API call was successful
if response.status_code == 200 and "success" in response.json():
    claim_id = response.json()["claim"]["id"]
    print(f"Created claim {claim_id}")
else:
    print("Error: failed to create claim")
    # Extract error message from response JSON
    error_message = response.json()["error"]["info"]
    print(f"Error: {error_message}")

exit(0)
# Test du parseur du format intermédiaire
insert_data_from_intermediate_format(data, wiki)

prop = wiki.get_property_id_by_name("horraire premier arret")
print(prop)


exit(0)
item = wiki.get_item_id_by_name("common2")
prop = wiki.get_property_id_by_name("commun à")
print(item, prop)
exit(0)
item = wiki.create_item("common2")
prop = wiki.create_property("commun à")
print(item, prop)
exit(0)


exit(0)
item = wiki.create_item("commonmmmmmmm")
print(item.id)


exit(0)
# Test de création d'un statement
item = wiki.get_item_id_by_name("common2")[0]
prop = wiki.get_property_id_by_name("commun à")[0]
print(item, prop)

wiki.create_multiple_statements(item, [prop, prop], ["multiple1", "multiple2"])


exit(0)
# wikibaseintegrator.wbi_helpers.execute_sparql_query(query, prefix=None, endpoint=None,
# user_agent=None, max_retries=1000,
# retry_after=60)


prop = wiki.get_property_id_by_name("commun a")
print(prop[0])
prop2 = wiki.is_property_exists("commun a")
print(prop2)
