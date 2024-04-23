import pandas as pd
# per prima cosa estraiamo i dati di AREU
missdb = pd.read_csv('EVT_MISS_PZ_2022.tab', low_memory= False, encoding='ISO-8859-1', on_bad_lines= 'skip', sep='\t')
# applichiamo il preprocessing in modo da filtrare e risistemare i dati
from preprocessing_AREU import *
dataframe=preprocessing(missdb)
# Filtriamo le righe duplicate basate su 'ID_PAZIENTE', in modo da isolare ogni singolo paziente soccorso, senza ripetizioni
dataframe = dataframe.drop_duplicates(subset='ID_PAZIENTE',keep='first')
#importiamo ora le griglie geografiche
import geopandas as gpd
griglia = gpd.read_file('GriglieGeografiche')
# trasformiamo le griglie in un GeoDataframe con i poligoni
import geopandas as gpd
griglia_gdf = gpd.GeoDataFrame(griglia)
# Estraiamo le coordinate geografiche (latitudine e longitudine) per ciascun poligono
# Calcoliamo i centroidi dei poligoni della griglia
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
import geopandas as gpd
from shapely.geometry import Point

# Crea un punto ogni paziente
dataframe['geometry'] = dataframe.apply(lambda row: Point(row['X'], row['Y']), axis=1)

# GeoDataFrame dalle coordinate dei soccorsi dei pazienti
geometry = [Point(xy) for xy in zip(dataframe['X'], dataframe['Y'])]
crs = {'init': 'epsg:32632'}
gdf_pazienti = gpd.GeoDataFrame(dataframe, crs=crs, geometry=geometry)

# Spatial join tra le chiamate di emergenza e la griglia geografica
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

import geopandas as gpd
import matplotlib.pyplot as plt

# Raggruppa per 'index_right' e conta il numero di chiamate di emergenza per ogni cella della griglia
densita_pazienti = join['index_right'].value_counts()

# Unisci i conteggi delle chiamate di emergenza con la griglia
griglia['densita_pazienti'] = densita_pazienti

# Visualizza la densità dei pazienti sulla griglia
griglia.plot(column='densita_pazienti', cmap='viridis', legend=True)
plt.title('Densità dei pazienti soccorsi per cella della griglia')
plt.xlabel('Longitudine')
plt.ylabel('Latitudine')
plt.show()