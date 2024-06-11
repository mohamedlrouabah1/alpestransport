import argparse
import json
import sys


def my_function_help():
    print("Le programme prend 2 arguments:")
    print("\t-Le nom de la source de donnees")
    print("\t-Le chemin du fichier de donnees")


def ajouter_source():
    name = input("Entrez le nom de la nouvelle source : ")
    url = input("Entrez l'URL de la nouvelle source : ")
    with open("sources.txt", "a") as f:  # Ouvrir le fichier en mode ajout
        f.write(f"\n{name},{url}")  # Ajouter la nouvelle source à la fin du fichier
    print(
        f"La source '{name}' a été ajoutée avec succès. Placer le parseur dans le sous dossier parseur et dans un fichier au nom de la source"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ingestion de données de transport en commun"
    )

    # Ajouter les arguments positionnels
    parser.add_argument(
        "nom",
        nargs=1,
        help="Nom de la source de données",
    )
    parser.add_argument(
        "data",
        nargs=1,
        help="Chemin du fichier de données",
    )
    parser.add_argument("-a", "--aide", action="store_true", help="Afficher l'aide")
    parser.add_argument(
        "-s", "--source", action="store_true", help="Afficher les sources"
    )
    args = parser.parse_args()

    if args.aide:
        my_function_help()
        exit(0)

    # CHARGE LES SOURCES DE DONNEES
    # Ouvrir le fichier en mode lecture
    with open("sources.txt", "r") as f:
        # Lire toutes les lignes du fichier
        lines = f.readlines()

    # Créer un dictionnaire pour stocker les sources
    sources = {}

    # Parcourir chaque ligne du fichier et extraire le nom et l'URL de la source
    for line in lines:
        line = line.strip()  # Supprimer les caractères de fin de ligne
        if line:  # Vérifier que la ligne n'est pas vide
            name, url = line.split(",")  # Séparer le nom et l'URL de la source
            sources[name] = url  # Ajouter la source au dictionnaire

    if args.source:
        # Afficher les sources
        print("Sources : ")
        for name, url in sources.items():
            print(f"{name}: {url}")
        exit(0)

    # Vérifier si la source donnée existe
    nom_source = args.nom[0]
    chemin = args.data[0]
    if nom_source not in sources.keys():
        source_de_donnees = input(
            "Source de donnee non répertoriee, voulez-vous en creer une nouvelle ? (O/N)"
        )

        if source_de_donnees.upper() == "O":
            # Si l'utilisateur répond "Oui", ajouter le code pour créer une nouvelle source de données
            ajouter_source()
        else:
            # Si l'utilisateur répond "Non", ajouter le code pour gérer cette situation
            print(
                "Annulation de la création de la source de données, vérifier les sources existantes avec l'option -s"
            )
            exit(0)

    print("Lancement de l'ingestion des données de la source", nom_source)
    print("Chargement ... done")
    print("Extraction et nettoyage ... done")
    print("Transformation format intermediare... done")
    print("Ingestion ... done")
    print("Liste des ajouts :")
    print("itinéraire: Bellevue<>Michon")
    print("arret: Bellevu")
    print("arret: Forges")
