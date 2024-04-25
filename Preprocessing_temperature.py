import pandas as pd
griglia_temperature= pd.read_csv('nome_file_modificato.csv', low_memory= False, encoding='ISO-8859-1', on_bad_lines= 'skip', sep=',')
import geopandas as gpd
griglia_geografica = gpd.read_file('GriglieGeografiche')
import pandas as pd
# Carico il dataframe
griglia_temperature['Data'] = pd.to_datetime(griglia_temperature['Data'])
# Raggruppo i dati per giorno, latitudine e longitudine e calcola la media delle temperature
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

import geopandas as gpd
import matplotlib.pyplot as plt

# Calcolo la media delle temperature giornaliere per zona
mean_temperatures_by_zone = join.groupby('LMB3B_IDna')['Temperatura'].mean()
# Unisci al DataFrame della griglia geografica per ottenere le geometrie delle zone
zone_geometries = griglia_geografica.merge(mean_temperatures_by_zone, left_on='LMB3B_IDna', right_index=True)
# Visualizza la distribuzione delle temperature sulla mappa della Lombardia
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
zone_geometries.plot(column='Temperatura', cmap='coolwarm', ax=ax, legend=True)
ax.set_title('Distribuzione delle temperature medie per zona in Lombardia')
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
# Calcola la media delle temperature giornaliere per zona
mean_temperatures_by_zone_days = join.groupby(['Data', 'LMB3B_IDna'])['Temperatura'].mean().reset_index()
# Crea un DataFrame pivoted con le date come righe e le zone come colonne
pivoted = mean_temperatures_by_zone_days.pivot(index='Data', columns='LMB3B_IDna', values='Temperatura')
# Plotta la distribuzione temporale delle medie di temperatura per zona
# al momento non necessaria : fig, ax = plt.subplots(figsize=(14,7))
#pivoted.plot(ax=ax, legend=False, alpha=0.5)
#ax.set_title('Distribuzione temporale delle medie di temperatura per zona')
#ax.set_xlabel('Data')
#ax.set_ylabel('Temperatura media')
#plt.legend(title='Zona', loc='upper left', bbox_to_anchor=(1, 1))
#plt.tight_layout()
#plt.show()

# esempio per zona di Milano
import matplotlib.pyplot as plt

# Filtra i dati solo per la zona di Milano
milano_data = join[join['LMB3B_IDna'] == 'Milano Zona MSB-000']

# Plotta l'andamento delle temperature per la zona di Milano
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(milano_data['Data'], milano_data['Temperatura'], color='blue')
ax.set_title('Andamento delle temperature a Milano Zona MSB-000')
ax.set_xlabel('Data')
ax.set_ylabel('Temperatura')
plt.tight_layout()
plt.show()

