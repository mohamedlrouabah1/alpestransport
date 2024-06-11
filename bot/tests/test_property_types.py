from wikibaseintegrator.wbi_enums import WikibaseDatatype
from AlpesTransportWikibaseIntegratorWrapper import AlpesTransportWiki
from AlpesTransport_config import endpoint, username, password
from example_format_intermediaire import data
from insert_data_wikibase import insert_data_from_intermediate_format
from wikibaseintegrator import datatypes
from wikibaseintegrator.models import snaks

# endpoint = "https://alpes-transport-sandbox.wikibase.cloud/w/api.php"
# username = "william"
# password = "william-bot@88hd7lft423pdnt5f95ijnoq8lccliae"

wiki = AlpesTransportWiki(endpoint, username, password)
# test création de statement avec value item
# wiki.create_statement(
#     item_id="Q83",  # Garfield
#     property_id="P300",  # item2
#     statement_value='{datavalue={"value":{"id":"Q83"},"type":"wikibase-entityid"}}',
# )
# création du statement
# item_value = wiki.wikibase_connection.item.get(entity_id="Q83")
# snack_item_value = snaks.Snak(
#     property_number="P300", datatype="wikibase-entityid", value="Q83"
# )
# statement = datatypes.ExternalID(
#     value="Q83",
#     prop_nr="P300",
# )
# # {'value': {'entity-type': 'item', 'numeric-id': 83, 'id': 'Q83'}
# data = [statement]


# # récupération de l'item
# item = wiki.wikibase_connection.item.get(entity_id="Q83")
# print("Get item result: ", item)

# item.claims.add(data)
# item.write(login=wiki.wikibase_login, is_bot=True)

exit(0)
prop = wiki.create_property("string2", datatype=WikibaseDatatype.STRING)
prop2 = wiki.create_property("item2", datatype=WikibaseDatatype.ITEM)
prop3 = wiki.create_property("tabular data2", datatype=WikibaseDatatype.TABULARDATA)
prop4 = wiki.create_property("time2", datatype=WikibaseDatatype.TIME)
prop5 = wiki.create_property("quantity2", datatype=WikibaseDatatype.QUANTITY)
prop6 = wiki.create_property("url2", datatype=WikibaseDatatype.URL)
prop7 = wiki.create_property("external id2", datatype=WikibaseDatatype.EXTERNALID)
prop8 = wiki.create_property(
    "monolingual text", datatype=WikibaseDatatype.MONOLINGUALTEXT
)
prop9 = wiki.create_property("geo shape", datatype=WikibaseDatatype.GEOSHAPE)
prop10 = wiki.create_property("math", datatype=WikibaseDatatype.MATH)

print("properties created")
