from Overlap_grid_temperature import *
from Calcolo_picchi_alti_temperature import *
import pandas as pd
griglia_temperature= pd.read_csv('Temperature_medie_2019.csv', low_memory= False, encoding='ISO-8859-1', on_bad_lines= 'skip', sep=',')
import geopandas as gpd
griglia_geografica=gpd.read_file('GriglieGeografiche')
join=overlap_grid_temp(griglia_temperature,griglia_geografica)
temperatura = 'Temperatura'
import os
zona = 'LMB3A_IDcu'
percentile = 0.9
picchi_alti = Calcolo_picchi_alti_temperature(join, zona, percentile, temperatura)
directory_path = os.path.join("Risultati_picchi", "temperatura_media_giornaliera", zona, f"Percentile={percentile}")
file_name = f"picchi_alti_t_media_2018_{zona}_{percentile}.csv"
file_path = os.path.join(directory_path, file_name)
picchi_alti.to_csv(file_path, index=False, sep=";")