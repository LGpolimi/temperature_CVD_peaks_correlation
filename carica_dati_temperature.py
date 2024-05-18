import pandas as pd
def carica_dati(anno):
    percorso_temperature = rf"C:\Users\maria\PycharmProjects\Progetto definitivo\Temperature_medie_{anno}.csv"
    griglia_temperature = pd.read_csv(percorso_temperature, sep=';')

    return griglia_temperature