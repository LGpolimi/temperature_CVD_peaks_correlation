import pandas as pd
missdb = pd.read_csv('EVT_MISS_PZ_2019.tab', low_memory= False, encoding='ISO-8859-1', on_bad_lines= 'skip', sep='\t')
# per prima cosa estraiamo i dati di AREU
from preprocessing_AREU import *
# applichiamo il preprocessing in modo da filtrare e risistemare i dati
dataframe=preprocessing(missdb)
# Filtriamo le righe duplicate basate su 'ID_PAZIENTE'
dataframe = dataframe.drop_duplicates(subset='ID_PAZIENTE', keep='first')
# Ordina il DataFrame dei pazienti in base alla zona
dataframe_ordinato = dataframe.sort_values(by='ZONA')
pazienti_per_zona = dataframe_ordinato.groupby('ZONA')

# Convertire la colonna 'DATA' in tipo datetime, se non è già in quel formato
dataframe['DATA'] = pd.to_datetime(dataframe['DATA'])

# Raggruppare i pazienti per giorno e per zona e contare il numero di pazienti per ogni combinazione
pazienti_per_giorno_e_zona = dataframe.groupby([dataframe['DATA'].dt.date, 'ZONA']).size().reset_index(name='numero_pazienti')

# Calcola la media mobile per ogni zona
risultati = pd.DataFrame()  # Inizializza un dataframe vuoto per contenere i risultati
for nome_zona, gruppo in pazienti_per_zona:
    # Calcola il numero di pazienti per giorno e per zona
    pazienti_per_giorno_e_zona = gruppo.groupby([gruppo['DATA'].dt.date]).size().reset_index(name='numero_pazienti')
    # Calcola la media mobile con finestra temporale di 3 giorni
    pazienti_per_giorno_e_zona['media_mobile'] = pazienti_per_giorno_e_zona['numero_pazienti'].rolling(window=3).mean()
    # Aggiungi la zona come colonna aggiuntiva
    pazienti_per_giorno_e_zona['ZONA'] = nome_zona
    # Aggiungi i risultati al dataframe dei risultati
    risultati = pd.concat([risultati, pazienti_per_giorno_e_zona])

# Ora il dataframe risultati contiene la media mobile della frequenza dei pazienti per ogni zona nel dataframe originale,
# insieme alla data a cui si riferiscono i valori della media mobile

# Calcola il 90° percentile per ogni zona sulla media mobile
percentili_per_zona = risultati.groupby('ZONA')['media_mobile'].quantile(0.9)

# Aggiungi i risultati come una nuova colonna al DataFrame risultati
risultati['90esimo_percentile_media_mobile'] = risultati['ZONA'].map(percentili_per_zona)

# Filtra le righe in cui 'media_mobile' è maggiore del '90esimo_percentile_media_mobile' per ogni zona
picchi_media_mobile = risultati[risultati['media_mobile'] > risultati['90esimo_percentile_media_mobile']]

#ESEMPIO PER LA ZONA DI MILANO
import matplotlib.pyplot as plt
# Trova i picchi della media mobile legati alla singola zona
picchi_milano000 = risultati[(risultati['ZONA'] == 'Milano Zona MSB-000') & (risultati['media_mobile'] > risultati['90esimo_percentile_media_mobile'])]

# Filtra le righe relative alla zona 'Milano Zona MSB-000'
milano_zona_msb_000 = risultati[risultati['ZONA'] == 'Milano Zona MSB-000']

# Crea il plot di tutti i giorni e la media mobile
plt.figure(figsize=(9, 6))
plt.plot(milano_zona_msb_000['DATA'], milano_zona_msb_000['media_mobile'], color='blue', label='Media mobile')
# Evidenzia i giorni che soddisfano la condizione di picchi_milano000
plt.scatter(picchi_milano000['DATA'], picchi_milano000['media_mobile'], color='red', label='Picchi')
# Imposta titoli ed etichette degli assi
plt.title('Media mobile in Milano Zona MSB-000')
plt.xlabel('Data')
plt.ylabel('Media mobile')
# Aggiungi una legenda
plt.legend()
# Ruota le etichette dell'asse x per una migliore leggibilità
plt.xticks(rotation=45)
# Rimuovi la griglia
plt.grid(False)
# Mostra il plot
plt.tight_layout()
plt.show()
