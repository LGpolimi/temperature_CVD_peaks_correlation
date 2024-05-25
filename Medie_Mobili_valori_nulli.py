import pandas as pd
def calcola_medie_mobili(join, zona_colonna, anno):
    join['DATA'] = pd.to_datetime(join['DATA'])

    # Ordina il DataFrame dei pazienti in base alla zona
    dataframe_ordinato = join.sort_values(by=zona_colonna)

    # Raggruppare i pazienti per giorno e per zona e contare il numero di pazienti per ogni combinazione
    pazienti_per_giorno_e_zona = dataframe_ordinato.groupby(
        [dataframe_ordinato['DATA'].dt.date, zona_colonna]).size().reset_index(
        name='numero_pazienti')

    segnali = pazienti_per_giorno_e_zona
    segnali['DATA'] = pd.to_datetime(segnali['DATA'])

    # Creare un intervallo di date completo per l'anno interessato
    start_date = f'{anno}-01-01'
    end_date = f'{anno}-12-31'
    date_range = pd.date_range(start=start_date, end=end_date)

    # Creare un dataframe con tutte le combinazioni di date e zone
    zones = segnali[zona_colonna].unique()
    full_index = pd.MultiIndex.from_product([date_range, zones], names=['DATA', zona_colonna])
    full_df = pd.DataFrame(index=full_index).reset_index()

    # Unire con il dataframe originale
    result = pd.merge(full_df, segnali, on=['DATA', zona_colonna], how='left')

    # Riempire i NaN in 'numero_pazienti' con 0
    result['numero_pazienti'] = result['numero_pazienti'].fillna(0)

    # Assicurarsi che il DataFrame sia ordinato per DATA per calcoli accurati di media mobile
    result = result.sort_values(by=[zona_colonna, 'DATA'])

    # Inizializza un DataFrame vuoto per memorizzare i risultati finali
    risultati_finali = pd.DataFrame()

    # Raggruppa per zona
    gruppi_per_zona = result.groupby(zona_colonna)

    # Cicla attraverso ogni gruppo (zona)
    for nome_zona, gruppo in gruppi_per_zona:
        # Assicurarsi che il gruppo sia ordinato per DATA
        gruppo = gruppo.sort_values(by='DATA')

        # Calcola la media mobile con una finestra centrata di 5 giorni
        gruppo['media_mobile'] = gruppo['numero_pazienti'].rolling(window=5, center=True, min_periods=1).mean()

        # Aggiungi i risultati al DataFrame finale
        risultati_finali = pd.concat([risultati_finali, gruppo])

    return risultati_finali