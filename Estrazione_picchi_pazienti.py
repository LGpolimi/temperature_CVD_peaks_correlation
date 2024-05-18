import pandas as pd
import geopandas as gpd
from preprocessing_AREU import *
from Overlap_grid_pazienti import *
from Medie_Mobili_zona import *
from Finestra_Percentili import *

# Carichiamo i dati
missdb = pd.read_csv('EVT_MISS_PZ_2021.tab', low_memory=False, encoding='ISO-8859-1', on_bad_lines='skip', sep='\t')

griglie_pazienti = preprocessing(missdb)
# Carichiamo le griglie
griglie_geografiche = gpd.read_file('GriglieGeografiche')
# Uniamo dati e griglie
join = overlap_grid_pazienti(griglie_pazienti, griglie_geografiche)
join['DATA'] = pd.to_datetime(join['DATA'])
dataframe = join.sort_values(by='DATA')
# Definiamo le zone, le finestre e i percentili
zone = ['LMB3B_IDna', 'LMB3A_IDcu']
lag_considerato = [15, 20, 30]
percentili = [90, 92.5, 95]

# Dizionario per salvare i risultati per combinazione
risultati_per_combinazione = {}

# Iteriamo sulle zone, finestre e percentili
for zona in zone:
    segnale = medie_mobili_zona(join, zona)
    for window in lag_considerato:
        for per in percentili:
            # Calcoliamo il percentile sulla finestra
            segnale_zona = finestra_percentili(window, per, zona, segnale)

            # Troviamo le righe dove la media mobile supera il percentile
            picchi = segnale_zona[segnale_zona['media_mobile'] > segnale_zona['Percentili']]

            # Assegniamo un nome unico per la chiave del dizionario
            nome_variabile = f"Picchi_{zona}_{window}_{per}"

            # Memorizziamo il DataFrame dei picchi nel dizionario
            risultati_per_combinazione[(zona, window, per)] = picchi

# Ora 'risultati_per_combinazione' contiene tutti i DataFrame per ciascuna combinazione di zona, window e percentile
