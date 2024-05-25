import pandas as pd
import geopandas as gpd
from Medie_Mobili_valori_nulli import *
from Finestra_globale_percentili import *
import numpy as np
join = pd.read_csv('pazienti_2019.csv',low_memory=False, encoding='ISO-8859-1', on_bad_lines='skip', sep=',')
zone = ['LMB3B_IDna', 'LMB3A_IDcu','LMB2A_IDna']
lag_considerato = [15,20,30]
percentili = np.arange(85, 91, 1)
# Dizionario per salvare i risultati per combinazione
risultati_per_combinazione = {}
anno = 2019
# Iteriamo sulle zone, finestre e percentili
for zona in zone:
    #creo dataframe con numero pazienti anche nulli e faccio media mobile
    segnale = calcola_medie_mobili(join,zona,anno)
    # Apro file popolazioni
    popo = pd.read_csv(f'{zona}.csv')
    #Li unisco
    segnale = pd.merge(segnale,popo, on= zona)
    # Calcolo medie mobili normalizzate rispetto alla popolazione (100k)
    segnale['medie_mobili_normalizzate']=segnale['media_mobile']/segnale['POP_2018']*100000
    # Trovo numero abitanti
    numero_abitanti = popo['POP_2018'].sum()
    # Trovo il numero di pazienti totali per ogni giorno
    segnale['Pazienti_totali_giorno']=segnale.groupby('DATA')['numero_pazienti'].transform('sum')
    # Calcolo la media mobile sul numero di pazienti totali per ogni giorno
    segnale['media_mobile_totale'] = segnale['Pazienti_totali_giorno'].rolling(
        window=5, center=True,
        min_periods=1).mean()
    # Normalizzo queste ultime medie mobili
    segnale['media_mobile_totale_normalizzata']=segnale['media_mobile_totale']/numero_abitanti*100000
    for window in lag_considerato:
        for per in percentili:
            # Calcoliamo il percentile sulla finestra
            segnale_zona = finestra_globale_percentili(window, per, segnale)
            # Troviamo le righe dove la media mobile normalizzata supera il percentile
            picchi = segnale_zona[segnale_zona['medie_mobili_normalizzate'] > segnale_zona['Percentili']]

            # Assegniamo un nome unico per la chiave del dizionario
            nome_variabile = f"Picchi_{zona}_{window}_{per}"

            # Memorizziamo il DataFrame dei picchi nel dizionario
            risultati_per_combinazione[(zona, window, per)] = picchi

# Ora 'risultati_per_combinazione' contiene tutti i DataFrame per ciascuna combinazione di zona, window e percentile

import os

# Specifica il percorso della cartella dove vuoi salvare i file
cartella = f'Picchi Pazienti {anno} nuovi'

# Crea la cartella se non esiste già
if not os.path.exists(cartella):
    os.makedirs(cartella)

for zona in zone:
    for window in lag_considerato:
        for per in percentili:
            chiave = (zona, window, per)
            risultati = risultati_per_combinazione[chiave]
            per_formatted = per / 100  # Converti il percentile
            # Costruisci il nome del file con il percorso della cartella
            filename = f'picchi_{anno}_{zona}_{window}_{per_formatted:.3f}.csv'
            filepath = os.path.join(cartella, filename)
            risultati.to_csv(filepath, index=False, sep=';')
