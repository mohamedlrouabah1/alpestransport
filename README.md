# Projet d'intéropérabilité

## Documentation

Veuillez vous référer aux documents et diagrammes réalisés durant le projet se situant dans le répertoire doc.  
Ci dessous ce trouve un lien vers le rapport final et les slides utilisées lors de la soutenance du projet.

- [rapport pdf](docs/compte_rendu/document_de_conception_final-groupe2-AlpesTransport-22_03_2023.pdf)  
- [slides de présentation pdf](docs/compte_rendu/alpestransport_presentation_finale.pdf)
- deploiement du site : https://william228.pythonanywhere.com (en attente d'ajout de wikibase cloud à la liste des api autorisées)

## Table des matières

- [Documentation](#documentation)
  - [rapport pdf](docs/compte_rendu/document_de_conception_final-groupe2-AlpesTransport-22_03_2023.pdf)
  - [slides de présentation pdf](docs/compte_rendu/alpestransport_presentation_finale.pdf)
- [Aperçu du client web](#aperçu-du-client-web)
- [Technologies utilisées](#technologies-utilisées)
  - [Container Wikibase + Sparql](#container-wikibase--sparql)
    - [Introduction](#introduction)
    - [utilisation en local](#utilisation-en-local)
  - [Serveur web python + Flask](#serveur-web-python--flask)
- [Sections en cours de modifications](#sections-en-cours-de-modifications)
  - [Lancer la wikibase](#lancer-la-wikibase)
  - [Lancer bot](#lancer-bot)
  - [Tips](#tips)
- [Annexe 1 : diagrammes](#annexe-1--diagrammes)
  - [Modélisation en processus du projet](#modélisation-en-processus-du-projet)
  - [Modèle RDF de la wikibase](#modèle-rdf-de-la-wikibase)
  - [Architecture de médiation](#architecture-de-médiation)
  - [Diagramme UML de sequence interface utilisateur](#diagramme-uml-de-sequence-interface-utilisateur)
  - [Diagramme UML d'activité insertion de données](#diagramme-uml-dactivité-insertion-de-données)
- [Annexe 2 : planning JIRA](#annexe-2--planning-jira)
- [Annexe 3 : Exemples d'utilisation](#annexe-3--exemple-dutilisation)

## Aperçu du client web

![home](/docs/screen-shots/1_home_page.gif)

![home](/docs/screen-shots/2_result_page.gif)

![home](/docs/screen-shots/3_error_page.gif)

## Technologies utilisées

### Container Wikibase + Sparql

Comming soon ...

#### Introduction

Wikibase est une plateforme open-source développée par la Wikimedia Foundation qui permet de stocker, gérer et publier des données structurées et liées en utilisant des technologies du Web sémantique telles que RDF (Resource Description Framework) et SPARQL (SPARQL Protocol and RDF Query Language).

#### utilisation en local

L'utilisation de Wikibase en local permet de créer sa propre base de données de connaissances, de gérer ses propres données et d'avoir un contrôle total sur l'accès et la sécurité de ces données. Cela peut être utile pour des organisations ou des projets ayant besoin de gérer des données complexes et structurées, comme des bibliothèques, des musées, des entreprises, etc.

### Serveur web python + Flask

Comming soon ...

## Sections en cours de modifications

### Lancer la wikibase

- `cd/docker`
- `docker-compose -f docker-compose.yml -f docker-compose.extra.yml up --no-build -d`

### Lancer bot

- `cd/bot`
- `python wikIntegraorBot.py`

### Tips

- `restart docker : docker-compose -f docker-compose.yml -f docker-compose.extra.yml restart`
- `down docker : docker-compose -f docker-compose.yml -f docker-compose.extra.yml down`
- `kill docker : docker-compose -f docker-compose.yml -f docker-compose.extra.yml kill`
- `stop docker : docker-compose -f docker-compose.yml -f docker-compose.extra.yml stop`

## Annexe 1 : Diagrammes

### Modélisation en processus du projet

![d](/docs/diagrams/modelisation_processus.drawio.png)

### Modèle RDF de la wikibase

![d](/docs/diagrams/modele_wikibase_22_02_2023.drawio.png)

### Architecture de médiation

![d](/docs/diagrams/architecture%20de%20mediation.drawio.png)

### Diagramme UML de sequence interface utilisateur

![d](/docs/diagrams/diagramme%20de%20sequence%20interface%20utilisateur.drawio.png)
![d](/docs/diagrams/diagramme%20de%20sequence%20interface%20utilisateur_2.drawio.png)

### Diagramme UML d'activité insertion de données

![d](/docs/diagrams/uml_activite_insertion.drawio.png)


## Annexe 2 : Planning JIRA

![d](/docs/screen-shots/jira_vue_d'ensemble_planning.png)

## Annexe 3 : Exemples d'utilisation

La page d'accueil du site permet de faire des recherches de deux types :

- [recherche d'informations sur un arrêt](#recherche-dun-arrêt)
- [recherche d'itinéraire entre un départ et une arrivée](#recherche-dun-itinéraire)

![search](/docs/screen-shots/exemple_utilisation/0_search.png)

### Recherche d'un arrêt

L'utilisateur rentre le nom d'un arrêt et envoie le formulaire.
Il est ensuite redirigé sur une page de résultat qui permet de consulter
les lignes de transport qui passe par cet arrêt.  

![search 1](/docs/screen-shots/exemple_utilisation/1_1_search.png)

![result 1](/docs/screen-shots/exemple_utilisation/1_2_result.png)

### Recherches d'un itinéraire

L'utilisateur rentre un arrêt de départ et un arrêt d'arrivé et envoie le formulaire.
Il est ensuite redirigé sur une page de résultat qui permet de consulter les lignes de
transports à utiliser pour effectuer son itinéraire.  
(pour des raisons de simplicité de l'UI, il n'est proposé qu'un seul trajet)

![search 2](/docs/screen-shots/exemple_utilisation/1ItineraireBernay_Lisieux.png)

![result 2](/docs/screen-shots/exemple_utilisation/1itineraireBernay_Lisieux_resultat.png)

![search 3](/docs/screen-shots/exemple_utilisation/2InitineraireTroyes_Curel.png)

![result 3](/docs/screen-shots/exemple_utilisation/2InitineraireTroyes_Curel_resultat.png)
