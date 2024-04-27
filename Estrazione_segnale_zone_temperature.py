import pandas as pd
griglia_temperature= pd.read_csv('griglia_temp_2019.csv', low_memory= False, encoding='ISO-8859-1', on_bad_lines= 'skip', sep=';')

# Carica il primo file CSV
#df1 = pd.read_csv('Temperature_medie_2019_1.csv', low_memory=False, encoding='ISO-8859-1', on_bad_lines='skip', sep=',')
# Carica il secondo file CSV
#df2 = pd.read_csv('Temperature_medie_2019_2.csv', low_memory=False, encoding='ISO-8859-1', on_bad_lines='skip', sep=',')

# Concatena i due dataframe
#griglia_temperature = pd.concat([df1, df2], ignore_index=True)

import geopandas as gpd
griglia_geografica = gpd.read_file('GriglieGeografiche')
import pandas as pd

# Converti la colonna 'Giorno' in formato data
griglia_temperature['Data'] = pd.to_datetime(griglia_temperature['Data'])
# Raggruppa i dati per giorno, latitudine e longitudine e calcola la media delle temperature
media_temperature_giornaliere= griglia_temperature

import geopandas as gpd
from shapely.geometry import Point
#calcolo della media per giorno:
# creazione di un punto per ogni temperatura
media_temperature_giornaliere['geometry'] = media_temperature_giornaliere.apply(lambda row: Point(row['Latitudine'], row['Longitudine']), axis=1)

# GeoDataFrame dalle coordinate delle chiamate di emergenza
geometry = [Point(xy) for xy in zip(media_temperature_giornaliere['Longitudine'], media_temperature_giornaliere['Latitudine'])]
crs = {'init': 'epsg:32632'}
gdf_temperatura = gpd.GeoDataFrame(media_temperature_giornaliere, crs=crs, geometry=geometry)

# Spatial join tra le temperature e la griglia geografica--> formazione di nuova colonna index_right
join = gpd.sjoin(gdf_temperatura, griglia_geografica, how="inner")
temperature_zone_data = join[['Data','Temperatura','LMB3B_IDna']]
temperature_medie_zone_data = join.groupby(['Data', 'LMB3B_IDna'])['Temperatura'].mean().reset_index()

# Calcolo la soglia alta con il 92.5 percentile e la soglia bassa con il 7.5 percentile
soglia_bassa = join['Temperatura'].quantile(0.075)
soglia_alta = join['Temperatura'].quantile(0.925)
# Individuo i rispettivi picchi
picchi_bassi = temperature_medie_zone_data[temperature_medie_zone_data['Temperatura']<soglia_bassa]
picchi_alti = temperature_medie_zone_data[temperature_medie_zone_data['Temperatura']>soglia_alta]

#salvo il file totale in CSV
#griglia_temperature.to_csv("griglia_temp_2019.csv", index=False, sep=";")

#ESEMPIO PER VEDERE L'ANDAMENTO IN UNA ZONA
import matplotlib.pyplot as plt
# Filtra il dataframe solo per la zona 'Milano Zona MSB-000'
milano_data = temperature_medie_zone_data[temperature_medie_zone_data['LMB3B_IDna'] == 'Milano Zona MSB-000']
#trova picchi alti e bassi legati alla singola zona
milano_picchi_alti= picchi_alti[picchi_alti['LMB3B_IDna']=='Milano Zona MSB-000']
milano_picchi_bassi= picchi_bassi[picchi_bassi['LMB3B_IDna']=='Milano Zona MSB-000']

# Crea un grafico per mostrare la temperatura nel tempo
plt.figure(figsize=(9, 6))

# Traccia la temperatura rispetto alla data
plt.plot(milano_data['Data'], milano_data['Temperatura'], color='green', label='temperatura', linestyle='-')

# Evidenzia i picchi bassi e alti
plt.scatter(milano_picchi_bassi['Data'], milano_picchi_bassi['Temperatura'], color='blue', label='Picco basso')
plt.scatter(milano_picchi_alti['Data'], milano_picchi_alti['Temperatura'], color='red', label='Picco alto')
#Evidenzia valore soglia bassa e alta
plt.axhline(y=soglia_bassa, color='blue', linestyle='--', label = 'Soglia bassa')
plt.axhline(y=soglia_alta, color='red', linestyle='--', label = 'Soglia alta')
# Aggiungi titolo e etichette agli assi
plt.title('Variazione della temperatura nel tempo - Milano Zona MSB-000')
plt.xlabel('Data')
plt.ylabel('Temperatura')
plt.xticks(rotation=45)  # Ruota le etichette sull'asse x per una migliore leggibilità

# Aggiungi una legenda
plt.legend(loc='upper right')

# Rimuovi la griglia
plt.grid(False)
# Mostra il plot
plt.tight_layout()
plt.show()
