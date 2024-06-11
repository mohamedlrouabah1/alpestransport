from wikibaseintegrator.wbi_config import config as wbi_config
from AlpesTransportWikibaseIntegratorWrapper import AlpesTransportWiki
from AlpesTransport_config import endpoint, username, password

bot = AlpesTransportWiki(endpoint, username, password)

# Create the desired properties with their descriptions
property_labels = [
    # "Est une", # pareil que "est un" on fait pas la distinction de genre pour les propriétés.
    "Propose",
    "coûte",
    "Est un",
    # Pour les arrêts, max 25.
    "s'arrete",
    "s'arrête en premier",
    "s'arrête en deuxième",
    "s'arrête en troisième",
    "s'arrête en quatrième",
    "s'arrête en cinquième",
    "s'arrête en sixième",
    "s'arrête en septième",
    "s'arrête en huitième",
    "s'arrête en neuvième",
    "s'arrête en dixième",
    "s'arrête en onzième",
    "s'arrête en douzième",
    "s'arrête en treizième",
    "s'arrête en quatorzième",
    "s'arrête en quinzième",
    "s'arrête en seizième",
    "s'arrête en dix-septième",
    "s'arrête en dix-huitième",
    "s'arrête en dix-neuvième",
    "s'arrête en vingtième",
    "s'arrête en vingt-et-unième",
    "s'arrête en vingt-deuxième",
    "s'arrête en vingt-troisième",
    "s'arrête en vingt-quatrième",
    "s'arrête en vingt-cinquième",
    "s'arrête en dernier",
    # ---------------------
    # horraire des arrêts
    "a pour horaire au premier arrêt",
    "a pour horaire au deuxième arrêt",
    "a pour horaire au troisième arrêt",
    "a pour horaire au quatrième arrêt",
    "a pour horaire au cinquième arrêt",
    "a pour horaire au sixième arrêt",
    "a pour horaire au septième arrêt",
    "a pour horaire au huitième arrêt",
    "a pour horaire au neuvième arrêt",
    "a pour horaire au dixième arrêt",
    "a pour horaire au onzième arrêt",
    "a pour horaire au douzième arrêt",
    "a pour horaire au treizième arrêt",
    "a pour horaire au quatorzième arrêt",
    "a pour horaire au quinzième arrêt",
    "a pour horaire au seizième arrêt",
    "a pour horaire au dix-septième arrêt",
    "a pour horaire au dix-huitième arrêt",
    "a pour horaire au dix-neuvième arrêt",
    "a pour horaire au vingtième arrêt",
    "a pour horaire au vingt-et-unième arrêt",
    "a pour horaire au vingt-deuxième arrêt",
    "a pour horaire au vingt-troisième arrêt",
    "a pour horaire au vingt-quatrième arrêt",
    "a pour horaire au vingt-cinquième arrêt",
    "a pour horaire au dernier arrêt",
    "a pour horaire de début",
    "a pour pas d'horaires",
    "a pour horaire de fin",
    # ---------------------
    # localisation
    "situé en",
    "a pour coord",  # coordonnées géographiques lattitudes et longitudes
    "appartenant au département",
    "jour de fonctionnement de la ligne",
    "est accessible aux personnes à mobilité réduite",
    # "en dernier",
    "a pour nom",
    "a pour code postal",
    "jour horaire arret",
]
# property_descriptions = ["relation entre deux entités", "activité offerte par une entité", "coût d'une entité", "type d'une entité", "arrêt d'une entité", "premier arrêt d'une entité", "dernier arrêt d'une entité", "lieu géographique d'une entité", "coordonnées géographiques d'une entité", "département où est située une entité", "heure de début d'une entité", "heure de fin d'une entité", "jour d'exploitation d'une ligne", "accessibilité pour les personnes à mobilité réduite", "dernier arrêt d'une entité", "nom d'une entité", "code postal d'une entité", "horaire d'un arrêt N d'une entité", "heure de début d'un horaire d'arrêt", "heure de fin d'un horaire d'arrêt", "intervalle de temps entre les horaires d'un arrêt", "jour où un horaire d'arrêt est en vigueur"]

for i, label in enumerate(property_labels):
    try:
        bot.create_property(label)
        print(f"property {i}: {label} successfuly created.")
    except:
        print(f"property {i}: {label} already exists.")

exit(0)

# Create the desired items with their descriptions
item_labels = [
    "Itinéraire",
    "Arrêt de départ",
    "Arrêt Terminus",
    "Horaire",
    "Nom de commune",
    "Département",
]
# item_descriptions = ["route de transport", "point de départ d'un itinéraire de transport", "point d'arrivée d'un itinéraire de transport", "horaire de transport", "nom d'une commune", "département d'une commune"]

for i, label in enumerate(item_labels):
    bot.create_item(label, item_labels[i])

print("Successfully created items and properties in Wikibase!")


# # Get or create items
# departure_stop = bot.get_or_create_item("Arrêt de départ", "Departure stop")
# municipality_name = bot.get_or_create_item("Nom de commune", "Municipality name")
# department = bot.get_or_create_item("Département", "Department")

# # Set labels and descriptions
# bot.set_label(departure_stop, "Arrêt de départ", "Departure stop")
# bot.set_description(departure_stop, "Arrêt de départ pour un itinéraire de transport", "Departure stop for a transportation route")

# bot.set_label(municipality_name, "Nom de commune", "Municipality name")
# bot.set_description(municipality_name, "Nom d'une commune", "Name of a municipality")

# bot.set_label(department, "Département", "Department")
# bot.set_description(department, "Division administrative territoriale en France", "Administrative territorial division in France")

# # Create claims
# bot.create_claim(departure_stop, "situé en", municipality_name, "item")
# bot.create_claim(departure_stop, "a pour coord", "48.8566° N, 2.3522° E", "string")
# bot.create_claim(departure_stop, "Est un", "Arrêt de départ", "item")
# bot.create_claim(municipality_name, "appartenant au département", department, "item")
# bot.create_claim(municipality_name, "a pour code postal", "75000", "string")
# bot.create_claim(municipality_name, "Est un", "Nom de commune", "item")
# bot.create_claim(municipality_name, "a pour code commune", "12345", "string")
# bot.create_claim(department, "a pour code", "75", "string")


# # Get or create items
# departure_stop = bot.get_or_create_item("Departure stop", "Arrêt de départ")
# municipality_name = bot.get_or_create_item("Municipality name", "Nom de commune")
# department = bot.get_or_create_item("Department", "Département")

# # Set labels and descriptions
# bot.set_label(departure_stop, "Departure stop", "Arrêt de départ")
# bot.set_description(departure_stop, "Stop at the beginning of a transportation route", "Arrêt au début d'un itinéraire de transport")

# bot.set_label(municipality_name, "Municipality name", "Nom de commune")
# bot.set_description(municipality_name, "Name of a municipality", "Nom d'une commune")

# bot.set_label(department, "Department", "Département")
# bot.set_description(department, "Administrative territorial division in France", "Division administrative territoriale en France")

# # Create claims
# bot.create_claim(departure_stop, "located in", municipality_name, "item")
# bot.create_claim(departure_stop, "has coordinates", "48.8566° N, 2.3522° E", "string")
# bot.create_claim(departure_stop, "Is a", "Departure stop", "item")
# bot.create_claim(municipality_name, "belongs to department", department, "item")
# bot.create_claim(municipality_name, "has postal code", "75000", "string")
# bot.create_claim(municipality_name, "Is a", "Municipality name", "item")
# bot.create_claim(municipality_name, "has INSEE code", "12345", "string")
# bot.create_claim(department, "has INSEE department code", "75", "string")

# print("Successfully add statements in Wikibase!")
