import pandas as pd

# Charger les fichiers GTFS en tant que DataFrames
routes = pd.read_csv('routes.txt', dtype={'route_id': str})
stops = pd.read_csv('stops.txt')
stop_times = pd.read_csv('stop_times.txt', dtype=str, low_memory=False)
trips = pd.read_csv('trips.txt')
calendar = pd.read_csv('calendar.txt')
# Fusionner les DataFrames pour obtenir les horaires des arrêts avec les noms des lignes de bus et des arrêts
print(routes.columns)
stop_merge = pd.merge(stop_times, stops, on='stop_id')
calendar_merge = pd.merge(trips, calendar, on='service_id')
#merged_data = pd.merge(merged_data, routes, on='')
total = pd.merge(calendar_merge, stop_merge, on='trip_id')
# Sélectionner uniquement les colonnes d'intérêt
print(stop_merge.columns)
#result = total[[ 'agency_id','trip_id','stop_name', 'arrival_time','stop_name','wheelchair_boarding']]
stop_horraire = pd.merge(stop_merge, trips, on='trip_id')
stop_horraire_ligne = pd.merge(stop_horraire, routes, on='route_id')
nom_lignes = routes['route_long_name'].unique()
print(nom_lignes)
print(stop_horraire_ligne[['stop_name','arrival_time', 'departure_time', 'route_long_name','route_id']])
# Obtenir le chemin des lignes
noms_lignes = routes['route_long_name'].unique()
chemins_lignes = {}
#for nom in noms_lignes:
#    arrets_ligne = stop_horraire_ligne[stop_horraire_ligne['route_long_name'] == nom]['stop_name'].unique()
#    chemins_lignes[nom] = arrets_ligne

#print('\nChemins des lignes :')
#for nom, arrets in chemins_lignes.items():
#"    print(nom, ':', arrets)


# Écriture du résultat dans un fichier CSV
#route_stops.to_csv('arrets_ligne_' + route_name + '.csv', index=False)
#ligne_arret = pd.merge(stop_merge, trips, on='trip_id')
#print(total.columns)
# Afficher les 10 premières lignes du résultat.
#print(result.head(100))
#print()
fichier = open("horraire_ligne.txt", "a")
fichier.write(str(stop_horraire_ligne))
fichier.close()

fichier = open("nom_lignes.txt", "a")
fichier.write(str(nom_lignes))
fichier.close()

