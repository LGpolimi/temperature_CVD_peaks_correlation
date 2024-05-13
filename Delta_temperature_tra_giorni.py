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

#CALCOLO IL DELTA TRA UN GIORNO E IL SUO PRECEDENTE
# Calcolare la differenza di temperatura tra i giorni consecutivi all'interno di ciascuna zona.
temperature_medie_zone_data['Delta Temperatura'] = temperature_medie_zone_data.groupby('LMB3B_IDna')['Temperatura'].diff()

# Crea un nuovo DataFrame contenente solo le colonne 'Zona', 'Data' e 'Delta Temperatura'
temperature_delta = temperature_medie_zone_data[['Data','LMB3B_IDna', 'Delta Temperatura']].dropna()  # Rimuovi le righe con valori NaN
#nel dataframe non c'è il 1/1/2019 poichè non ha nessun giorno precedente con cui confrontarsi

# Calcola il valore assoluto del delta temperatura
temperature_delta['Delta Temperatura Assoluto'] = temperature_delta['Delta Temperatura'].abs()

# Crea un nuovo DataFrame contenente solo le colonne 'Zona', 'Data' e 'Delta Temperatura Assoluto'
temperature_delta_assoluto = temperature_delta[['Data','LMB3B_IDna', 'Delta Temperatura Assoluto']].dropna()

#calcolo la soglia del delta
soglia_delta=temperature_delta_assoluto['Delta Temperatura Assoluto'].quantile(0.90)
# individuo i picchi
picchi_delta=temperature_delta_assoluto[temperature_delta_assoluto['Delta Temperatura Assoluto']>soglia_delta]

#ESEMPIO PER VEDERE L'ANDAMENTO IN UNA ZONA
import matplotlib.pyplot as plt
# Filtra il dataframe solo per la zona 'Milano Zona MSB-000'
milano_data = temperature_delta_assoluto[temperature_delta_assoluto['LMB3B_IDna'] == 'Milano Zona MSB-000']
#trova picchi legati alla singola zona
milano_picchi_delta= picchi_delta[picchi_delta['LMB3B_IDna']=='Milano Zona MSB-000']


# Crea un grafico per mostrare la temperatura nel tempo
plt.figure(figsize=(9, 6))

# Traccia la temperatura rispetto alla data
plt.plot(milano_data['Data'], milano_data['Delta Temperatura Assoluto'], color='green', label='Delta temperatura Assoluto', linestyle='-')

# Evidenzia i picchi delta
plt.scatter(milano_picchi_delta['Data'], milano_picchi_delta['Delta Temperatura Assoluto'], color='red', label='Picco delta')

#Evidenzia valore soglia delta
plt.axhline(y=soglia_delta, color='red', linestyle='--', label = 'Soglia delta')

# Aggiungi titolo e etichette agli assi
plt.title('Delta della temperatura nel tempo - Milano Zona MSB-000')
plt.xlabel('Data')
plt.ylabel('Delta Temperatura Assoluta')
plt.xticks(rotation=45)  # Ruota le etichette sull'asse x per una migliore leggibilità

# Aggiungi una legenda
plt.legend(loc='upper right')

# Rimuovi la griglia
plt.grid(False)
# Mostra il plot
plt.tight_layout()
plt.show()
