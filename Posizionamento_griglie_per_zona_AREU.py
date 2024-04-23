import pandas as pd
missdb = pd.read_csv('EVT_MISS_PZ_2022.tab', low_memory= False, encoding='ISO-8859-1', on_bad_lines= 'skip', sep='\t')
# per prima cosa estraiamo i dati di AREU
from preprocessing_AREU import *
# applichiamo il preprocessing in modo da filtrare e risistemare i dati
dataframe=preprocessing(missdb)
# Filtriamo le righe duplicate basate su 'ID_PAZIENTE'
dataframe = dataframe.drop_duplicates(subset='ID_PAZIENTE',keep='first')
#importiamo ora le griglie geografiche
import geopandas as gpd
griglia = gpd.read_file('GriglieGeografiche')
# trasformiamo le griglie in un GeoDataframe con i poligoni
import geopandas as gpd
griglia_gdf = gpd.GeoDataFrame(griglia)
# Estrai le coordinate geografiche (latitudine e longitudine) per ciascun poligono
# Calcola i centroidi dei poligoni della griglia
griglia['latitudine_centroide'] = griglia.geometry.centroid.y
griglia['longitudine_centroide'] = griglia.geometry.centroid.x

# ora dobbiamo cambiare l'EPSG al dataframe coi dati delle chiamate, in modo che le coordinate siano
# tutte nella stessa unità di misura --> da EPSG 32632 a EPSG 4326
from pyproj import Proj, transform
def convert_to_meters(lat_deg, long_deg):
    in_proj = Proj(init='epsg:4326')  # Sistema di riferimento di partenza (WGS 84)
    out_proj = Proj('epsg:32632')  # Sistema di riferimento EPSG:32632 (UTM zone 32N)
    # Converti le coordinate da gradi decimali a metri
    x, y = transform(in_proj, out_proj, long_deg, lat_deg)
    return x, y
# Applica la funzione ai dati nel dataframe
dataframe.loc[:, 'X'], dataframe.loc[:, 'Y'] = convert_to_meters(dataframe['LAT'], dataframe['LONG'])
# Ora il DataFrame contiene due nuove colonne con le coordinate convertite in metri
from shapely.geometry import Point
# Crea un punto ogni paziente
dataframe['geometry'] = dataframe.apply(lambda row: Point(row['X'], row['Y']), axis=1)
import geopandas as gpd


# Aggiungi un identificatore univoco per ogni zona nel DataFrame della griglia
griglia['zona_id'] = griglia['LMB3B_IDna'].astype('category').cat.codes

# Crea un GeoDataFrame per i pazienti
geometry = [Point(xy) for xy in zip(dataframe['X'], dataframe['Y'])]
crs = {'init': 'epsg:32632'}
gdf_pazienti = gpd.GeoDataFrame(dataframe, crs=crs, geometry=geometry)
join = gpd.sjoin(gdf_pazienti, griglia, how="inner")

import pandas as pd
import matplotlib.pyplot as plt

join['DATA'] = pd.to_datetime(join['DATA'])

pazienti_per_giorno = join.groupby(join['DATA'].dt.date).size()

# Visualizzazione del numero di pazienti per giorno
pazienti_per_giorno.plot(kind='line', figsize=(10, 6), title='Numero di pazienti soccorsi per giorno')
plt.xlabel('Data')
plt.ylabel('Numero pazienti')
plt.show()
# Join tra i pazienti e la griglia sulla colonna che rappresenta la zona
join = gpd.sjoin(gdf_pazienti, griglia, how="inner")

# Aggrega il numero di pazienti per ogni zona
pazienti_per_zona = join.groupby('LMB3B_IDna').size()

# Unisci i conteggi delle chiamate di emergenza con la griglia
griglia = griglia.merge(pazienti_per_zona.rename('pazienti_per_zona'), left_on='LMB3B_IDna', right_index=True)

# Visualizza la densità dei pazienti per zona sulla mappa
griglia.plot(column='pazienti_per_zona', cmap='viridis', legend=True)
plt.title('Numero di pazienti soccorsi per zona')
plt.xlabel('Longitudine')
plt.ylabel('Latitudine')
plt.show()