from Overlap_grid_temperature import overlap_grid_temp
from Calcolo_picchi_alti_temperature import Calcolo_picchi_alti_temperature
import pandas as pd
import geopandas as gpd
import os

# Parametri
zone = ['LMB3B_IDna', 'LMB3A_IDcu']
percentili = [0.9, 0.925, 0.95]
base_directory = r"C:\Users\maria\PycharmProjects\Progetto definitivo\Risultati_picchi_temperature"

# Creazione delle cartelle per ogni combinazione di zona e percentile
for zona in zone:
    for percentile in percentili:
        directory_path = os.path.join(base_directory, "temperatura_media_giornaliera", zona, f"Percentile={percentile}")
        os.makedirs(directory_path, exist_ok=True)

print("Le cartelle sono state create con successo.")


def carica_dati(anno, percorso_base):
    percorso_temperature = rf"{percorso_base}\Temperature_medie_{anno}.csv"
    griglia_temperature = pd.read_csv(percorso_temperature, low_memory=False, encoding='ISO-8859-1',
                                      on_bad_lines='skip', sep=',')
    return griglia_temperature


# Parametri
anni = [2018, 2019, 2021, 2022, 2023]
percentili = [0.9, 0.925, 0.95]
zone = ['LMB3B_IDna', 'LMB3A_IDcu']
percorso_base = r"C:\Users\maria\PycharmProjects\Progetto definitivo"
griglia_geografica = gpd.read_file('GriglieGeografiche')

# Loop attraverso tutte le combinazioni di parametri
for anno in anni:
    griglia_temperature = carica_dati(anno, percorso_base)
    join = overlap_grid_temp(griglia_temperature, griglia_geografica)
    for zona in zone:
        for percentile in percentili:
            temperatura = 'Temperatura'
            picchi_alti = Calcolo_picchi_alti_temperature(join, zona, percentile, temperatura)

            directory_path = os.path.join(base_directory, "temperatura_media_giornaliera", zona,
                                          f"Percentile={percentile}")
            os.makedirs(directory_path, exist_ok=True)

            file_name = f"picchi_alti_t_media_{anno}_{zona}_{percentile}.csv"
            file_path = os.path.join(directory_path, file_name)

            picchi_alti.to_csv(file_path, index=False, sep=";")
            print(
                f"Il file picchi temperatura per l'anno {anno}, la zona {zona} e il percentile temperatura {percentile} è stato salvato in {file_path}")
