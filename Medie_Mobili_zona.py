import pandas as pd
def medie_mobili_zona (join,zona_selezionata):
    join['DATA'] = pd.to_datetime(join['DATA'])
    zona = zona_selezionata  # per zona da 100k usa LMB3B_IDna
    # Ordina il DataFrame dei pazienti in base alla zona
    dataframe_ordinato = join.sort_values(by=zona)
    pazienti_per_zona = dataframe_ordinato.groupby(zona)
    # Raggruppare i pazienti per giorno e per zona e contare il numero di pazienti per ogni combinazione
    pazienti_per_giorno_e_zona = dataframe_ordinato.groupby([dataframe_ordinato['DATA'].dt.date, zona]).size().reset_index(
        name='numero_pazienti')
    # Calcola la media mobile per ogni zona
    risultati = pd.DataFrame()
    for nome_zona, gruppo in pazienti_per_zona:
        # Calcola il numero di pazienti per giorno e per zona
        pazienti_per_giorno_e_zona = gruppo.groupby([gruppo['DATA'].dt.date]).size().reset_index(name='numero_pazienti')
        # Calcola la media mobile con finestra temporale centrata di 5 giorni
        pazienti_per_giorno_e_zona['media_mobile'] = pazienti_per_giorno_e_zona['numero_pazienti'].rolling(
            window=5, center=True,
            min_periods=1).mean()  # Imposta min_periods=1 per considerare anche i periodi con meno di 5 giorni
        # Aggiungi la zona come colonna aggiuntiva
        pazienti_per_giorno_e_zona[zona] = nome_zona
        # Aggiungi i risultati al dataframe dei risultati
        risultati = pd.concat([risultati, pazienti_per_giorno_e_zona])
    return risultati