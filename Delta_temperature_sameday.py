import pandas as pd
def delta_temp (nome_file1, nome_file2):
    # Leggi il file CSV esistente
    df1 = pd.read_csv(nome_file1, low_memory=False, encoding='ISO-8859-1', on_bad_lines='skip', sep=';')

    # Effettua le modifiche necessarie al DataFrame
    df1['Data'] = pd.to_datetime(df1['Data'])

    # Raggruppa i dati per giorno, latitudine e longitudine e calcola la temperatura massima e minima
    temperature_giornaliere1 = df1.groupby(['Data', 'Latitudine', 'Longitudine'])['Temperatura'].agg(
        [('Temperatura_massima', 'max'), ('Temperatura_minima', 'min')]).reset_index()

    # Calcola la differenza tra temperatura massima e temperatura minima per ogni riga
    temperature_giornaliere1['Delta_Temperatura'] = temperature_giornaliere1['Temperatura_massima'] - \
                                                    temperature_giornaliere1['Temperatura_minima']

    # Salva il DataFrame delle differenze di temperatura in un nuovo file CSV
    temperature_giornaliere1.to_csv('Delta_Temperature_2019_1.csv', index=False)

    # Leggi il file CSV esistente
    df = pd.read_csv(nome_file2, low_memory=False, encoding='ISO-8859-1', on_bad_lines='skip', sep=';')

    # Effettua le modifiche necessarie al DataFrame
    df['Data'] = pd.to_datetime(df['Data'])

    # Raggruppa i dati per giorno, latitudine e longitudine e calcola la temperatura massima e minima
    temperature_giornaliere = df.groupby(['Data', 'Latitudine', 'Longitudine'])['Temperatura'].agg(
        [('Temperatura_massima', 'max'), ('Temperatura_minima', 'min')]).reset_index()

    # Calcola la differenza tra temperatura massima e temperatura minima per ogni riga
    temperature_giornaliere['Delta_Temperatura'] = temperature_giornaliere['Temperatura_massima'] - \
                                                   temperature_giornaliere['Temperatura_minima']

    # Salva il DataFrame delle differenze di temperatura in un nuovo file CSV
    temperature_giornaliere.to_csv('Delta_Temperature_2019_2.csv', index=False)
    # Stampa i risultati
    print(temperature_giornaliere1)
    print(temperature_giornaliere)

    Delta_Temperature_2019 = pd.concat([df1, df], ignore_index=True)
    Delta_Temperature_2019.to_csv('Delta_Temperature_2019.csv', index=False, sep=',')
    return Delta_Temperature_2019