import pandas as pd
missdb = pd.read_csv('EVT_MISS_PZ_2022.tab', low_memory= False, encoding='ISO-8859-1', on_bad_lines= 'skip', sep='\t')
# per prima cosa estraiamo i dati di AREU
from preprocessing_AREU import *
# applichiamo il preprocessing in modo da filtrare e risistemare i dati
dataframe=preprocessing(missdb)
#importiamo ora le griglie geografiche
import geopandas as gpd
griglia = gpd.read_file('GriglieGeografiche')
# trasformiamo le griglie in un GeoDataframe con i poligoni
import geopandas as gpd
griglia_gdf = gpd.GeoDataFrame(griglia)
from Overlap_grid_pazienti import *
join = overlap_grid_pazienti(dataframe,griglia)
import pandas as pd
import matplotlib.pyplot as plt

join['DATA'] = pd.to_datetime(join['DATA'])

pazienti_per_giorno = join.groupby(join['DATA'].dt.date).size()

# Visualizzazione del numero di pazienti per giorno
pazienti_per_giorno.plot(kind='line', figsize=(10, 6), title='Numero di pazienti soccorsi per giorno')
plt.xlabel('Data')
plt.ylabel('Numero pazienti')
plt.show()

# seleziona la divisione di zone d'interesse
zona = 'LMB3B_IDna' # per zona da 100k usa LMB3A_IDcu
# Aggrega il numero di pazienti per ogni zona
pazienti_per_zona = join.groupby(zona).size()

# Unisci i conteggi delle chiamate di emergenza con la griglia
griglia = griglia.merge(pazienti_per_zona.rename('pazienti_per_zona'), left_on=zona, right_index=True)

# Visualizza la densità dei pazienti per zona sulla mappa
griglia.plot(column='pazienti_per_zona', cmap='viridis', legend=True)
plt.title('Numero di pazienti soccorsi per zona')
plt.xlabel('Longitudine')
plt.ylabel('Latitudine')
plt.show()