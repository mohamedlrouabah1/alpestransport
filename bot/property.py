"""
Module to create wikibase property before inserting data.
It is required to create them before because with wikibase cloud
there is some latency between the creation of a property and its
availibility when you make a search for it.
"""
from number_in_letter import number_in_letter
from AlpesTransport_config import endpoint, username, password
from AlpesTransportWikibaseIntegratorWrapper import AlpesTransportWiki
from wikibaseintegrator.wbi_enums import WikibaseDatatype

# Connexion to the wikibase
wikibot = AlpesTransportWiki(endpoint, username, password)

# First create properties s'arrête en nième et a pour horaire au nième arrêt
# NB: the array contains at last the world 'dernier'
n = len(number_in_letter) + 1
for i in range(1, n):
    try:
        label = "s'arrête en " + number_in_letter[i]
        wikibot.create_property_if_not_exist(property_label=label)
        label = "a pour horaire au " + number_in_letter[i] + " arrêt"
        wikibot.create_property_if_not_exist(property_label=label)
    except:
        print("a")

# latitude et longitude need to be float type
# NB: I can't make statement with values as other type than string
# Thus we store it as string, and use xsd:float function in SPARQL query
wikibot.create_property_if_not_exist(property_label="a pour longitude")
wikibot.create_property_if_not_exist(property_label="a pour latitude")


property_labels = [
    "Propose",
    "coûte",
    "Est un",  # "Est une", # pareil que "est un" on fait pas la distinction de genre pour les propriétés.
    "s'arrete",
    # ---------------------
    "a pour horaire de début",
    "a pour pas d'horaires",
    "a pour horaire de fin",
    "jour horaire arret",
    # ---------------------
    # localisation
    "situé en",
    "appartenant au département",
    "jour de fonctionnement de la ligne",
    "est accessible aux personnes à mobilité réduite",
    # caractéristiques d'identification
    "a pour nom",
    "a pour code postal",
]

for property_label in property_labels:
    wikibot.create_property_if_not_exist(property_label=property_label)
