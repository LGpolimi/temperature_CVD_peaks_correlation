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
# Raggruppa i pazienti per zona
pazienti_per_zona = dataframe_ordinato.groupby('ZONA')

# Convertire la colonna 'DATA' in tipo datetime, se non è già in quel formato
dataframe['DATA'] = pd.to_datetime(dataframe['DATA'])

# Raggruppare i pazienti per giorno e per zona e contare il numero di pazienti per ogni combinazione
pazienti_per_giorno_e_zona = dataframe.groupby([dataframe['DATA'].dt.date, 'ZONA']).size().reset_index(name='numero_pazienti')
# Calcola il 90° percentile per ogni zona
percentili_per_zona = pazienti_per_giorno_e_zona.groupby('ZONA')['numero_pazienti'].quantile(0.9)
# Aggiungi i risultati come una nuova colonna al DataFrame originale
pazienti_per_giorno_e_zona['90esimo_percentile'] = pazienti_per_giorno_e_zona['ZONA'].map(percentili_per_zona)
#ora devo cercare di isolare solo i picchi, ossia solo ciò che è oltre il 90-esimo percentile, per poi
pazienti_per_giorno_e_zona.groupby(['ZONA'])
# Filtra le righe in cui 'numero_pazienti' è maggiore del '90esimo_percentile' per ogni zona
Picchi_pazienti = pazienti_per_giorno_e_zona[pazienti_per_giorno_e_zona['numero_pazienti'] > pazienti_per_giorno_e_zona['90esimo_percentile']]

#ESEMPIO PER VEDERE L'ANDAMENTO IN UNA ZONA
# Trovo i picchi legati alla singola zona
picchi_milano000 = Picchi_pazienti[Picchi_pazienti['ZONA']=='Milano Zona MSB-000']
import matplotlib.pyplot as plt
# Filtra le righe relative alla zona 'Bergamo Zona MSB-001'
milano_zona_msb_000 = pazienti_per_giorno_e_zona[pazienti_per_giorno_e_zona['ZONA'] == 'Milano Zona MSB-000']
# Crea il plot di tutti i giorni dell'anno e il numero di pazienti
plt.figure(figsize=(9, 6))
plt.plot(milano_zona_msb_000['DATA'], milano_zona_msb_000['numero_pazienti'], color='blue', label='Numero pazienti')
# Evidenzia i giorni che soddisfano la condizione di picchi_bergamo001
plt.scatter(picchi_milano000['DATA'], picchi_milano000['numero_pazienti'], color='red', label='Picchi')
# Imposta titoli ed etichette degli assi
plt.title('Pazienti per giorno in Milano Zona MSB-000')
plt.xlabel('Data')
plt.ylabel('Numero pazienti')
# Aggiungi una legenda
plt.legend()
# Ruota le etichette dell'asse x per una migliore leggibilità
plt.xticks(rotation=45)
# Rimuovi la griglia
plt.grid(False)
# Mostra il plot
plt.tight_layout()
plt.show()