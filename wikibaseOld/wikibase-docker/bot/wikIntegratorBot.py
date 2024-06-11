# from wikibaseintegrator.wbi_config import config as wbi_config
# from AlpesTransportWikibaseIntegratorWrapper import AlpesTransportWiki


# # Set up WikibaseIntegrator config
# wbi_config['MEDIAWIKI_API_URL'] = "http://localhost:8181/w/api.php"
# wbi_config['SPARQL_ENDPOINT_URL'] = 'http://localhost:8834/proxy/wdqs/bigdata/namespace/wdq/sparql'
# wbi_config['WIKIBASE_URL'] = 'http://wikibase.svc'

# # Login to the wikibase
# # endpoint="http://localhost:8181/api.php"
# # username="AlpesTransport"
# # password="new@em08fiktfdroqr1phf41t9igs288t51r"


# # Create an instance of the AlpesTransportWiki class
# bot = AlpesTransportWiki(wikibase_url=wbi_config['MEDIAWIKI_API_URL'],
#                           wikibase_user='AlpesTransport@mohamed-bot',
#                           wikibase_password='jktjrbuj9q9jkqkd5jlutrofbon11ehm')

# # bot =  AlpesTransportWiki(endpoint, username, password)

# # Create the desired properties
# property_labels = ["Est une", "Propose", "coût", "Est un", "s'arrête", "s'arrête en premier", "s'arrête en dernier", "situé en", "a pour coord"]
# for label in property_labels:
#     bot.create_property(label)

# # # Create the desired items
# # item_labels = ["Itinéraire", "Arret de départ", "Arret Terminus", "Horraire", "Nom de commune", "Département"]
# # for label in item_labels:
# #     bot.create_item(label)

# # print("Successfully created item and property in Wikibase!")

from wikibaseintegrator.wbi_config import config as wbi_config

# Set up WikibaseIntegrator config
wbi_config["MEDIAWIKI_API_URL"] = "http://localhost:8383/api.php"
wbi_config["SPARQL_ENDPOINT_URL"] = 'http://localhost:8282/proxy/wdqs/bigdata/namespace/wdq/sparql'
wbi_config['WIKIBASE_URL'] = 'http://wikibase.svc'

from AlpesTransportWikibaseIntegratorWrapper import AlpesTransportWiki

# Login to the wikibase
# endpoint="http://localhost:8181/api.php"
# username="AlpesTransport@bot"
# password="bmpht074kffk7rska77jlofoahjt7dvf"

# Create an instance of the AlpesTransportWiki class
wiki = AlpesTransportWiki(wikibase_url='http://localhost:8383/api.php',
                          wikibase_user='WikibaseAdmin@common-bot',
                          wikibase_password='eemgmiv4d1cufpitq47ep7lclt87hnvl')

# wiki =  AlpesTransportWiki(endpoint, username, password)

# Create a property
property_label = "coût"
property_description = "Le coût d'un trajet"
datatype = "Quantity"
new_property = wiki.create_property(property_label=property_label,
                                    property_description=property_description,
                                    datatype=datatype)

# Create an item
item_label = "Ligne de bus 123"
item_description = "Une ligne de bus qui relie deux villes"
new_item = wiki.create_item(item_label=item_label,
                            item_description=item_description)

# Add a statement to the item
statement_value = 5.5
statement_property = new_property
new_item.write(login=wiki.wikibase_login, is_bot=True, claims=[{statement_property: statement_value}])

print("Successfully created item and property in Wikibase!")
