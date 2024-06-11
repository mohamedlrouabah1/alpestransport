# Global Configuration of the url of the wikibase :
from wikibaseintegrator.wbi_config import config as wbi_config

wbi_config["MEDIAWIKI_API_URL"] = "http://localhost:8181/api.php"
wbi_config[
    "SPARQL_ENDPOINT_URL"
] = "http://localhost:8834/proxy/wdqs/bigdata/namespace/wdq/sparql"
wbi_config["WIKIBASE_URL"] = "http://wikibase.svc"


# Login to the wikibase
endpoint = "http://localhost:8181/api.php"
username = "AlpesTransport@william-bot"
password = "6pg8ht2cd2brl80voash352ale77qfuv"


from AlpesTransportWikibaseIntegratorWrapper import AlpesTransportWiki

wiki = AlpesTransportWiki(endpoint, username, password)
print(AlpesTransportWiki)
print(wiki.wikibase_login.get_session())

# wiki.create_item("Test of the class")

print("Create a test entity:")
# item = wiki.create_item("Test of the class 2")
# print(item)

property = wiki.create_property("Test class 6 create property")
print(property)


exit(0)


from wikibaseintegrator import entities
from wikibaseintegrator import models
import wikibaseintegrator.wbi_login as wbi_login
import wikibaseintegrator.wbi_helpers as wbi_helpers
from wikibaseintegrator import wbi_login, WikibaseIntegrator
from wikibaseintegrator.datatypes import ExternalID
from wikibaseintegrator.wbi_config import config as wbi_config

# Create a connection
wb = wbi_login.Login(
    user=username,
    password=password,
    mediawiki_api_url="http://localhost:8181/api.php",
)
# print(help(wbi_login))
# print(help(wbi_login.Login))
session = wb.get_session()
print(session)
# print(dir(session))
# print(help(session))

# print("\nConnected\n\n\n")
# Object to create item
wbi = WikibaseIntegrator(login=wb, is_bot=True)
#print("wikibaseIntegrator: ", wbi)
#print(dir(WikibaseIntegrator))
#print(help(WikibaseIntegrator))
#print("Help object wbi: ")
#print(dir(wbi))
#print(help(wbi.item))
#print(help(ExternalID))


# ----- copy -paste
# data type object, e.g. for a NCBI gene entrez ID
entrez_gene_id = ExternalID(value="42")  # , prop_nr='P351')

# data goes into a list, because many data objects can be provided to
data = [entrez_gene_id]

# Create a new item
item = wbi.item.new()

# prop = wbi.property.new()
# propertype='string', datatype='string', description='A string property', label='String property', aliases=['string', 'str']
# prop.write(login=wbi.login, is_bot=True)

property_label = "22222222222222222222222222222222"
property_description = "description de la propriété"


label = models.labels.Labels()
label.set(language="fr", value=property_label)

property_engine = entities.property.PropertyEntity(
    datatype="string",
    labels=label,
    # descriptions={property_description: "fr"}
)

property_engine.write(login=wbi.login, is_bot=True)

print(property_engine)






exit(0)

# Set an english label
item.labels.set(language="fr", value="Un autre item ajouté par le bot")

# Set a French description
item.descriptions.set(language="fr", value="Une description un peu longue")

item.claims.add(data)
item.write(login=wbi.login, is_bot=True)
print(item)
exit(0)
