import pandas as pd
griglia_temperature= pd.read_csv('nome_file_modificato.csv', low_memory= False, encoding='ISO-8859-1', on_bad_lines= 'skip', sep=',')
import geopandas as gpd
griglia_geografica = gpd.read_file('GriglieGeografiche')
import pandas as pd
# Carico il dataframe
griglia_temperature['Data'] = pd.to_datetime(griglia_temperature['Data'])
from Overlap_grid_temperature import *
join = overlap_grid_temp(griglia_temperature,griglia_geografica)

import geopandas as gpd
import matplotlib.pyplot as plt
zona = 'LMB3B_IDna'
temperatura = 'Temperatura'
# Calcolo la media delle temperature giornaliere per zona
mean_temperatures_by_zone = join.groupby(zona)[temperatura].mean()
# Unisci al DataFrame della griglia geografica per ottenere le geometrie delle zone
zone_geometries = griglia_geografica.merge(mean_temperatures_by_zone, left_on=zona, right_index=True)
# Visualizza la distribuzione delle temperature sulla mappa della Lombardia
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
zone_geometries.plot(column=temperatura, cmap='coolwarm', ax=ax, legend=True)
ax.set_title('Distribuzione delle temperature medie per zona in Lombardia')
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
# Calcola la media delle temperature giornaliere per zona
mean_temperatures_by_zone_days = join.groupby(['Data', zona])[temperatura].mean().reset_index()
# Crea un DataFrame pivoted con le date come righe e le zone come colonne
pivoted = mean_temperatures_by_zone_days.pivot(index='Data', columns=zona, values=temperatura)
# Plotta la distribuzione temporale delle medie di temperatura per zona
# al momento non necessaria : fig, ax = plt.subplots(figsize=(14,7))
#pivoted.plot(ax=ax, legend=False, alpha=0.5)
#ax.set_title('Distribuzione temporale delle medie di temperatura per zona')
#ax.set_xlabel('Data')
#ax.set_ylabel('Temperatura media')
#plt.legend(title='Zona', loc='upper left', bbox_to_anchor=(1, 1))
#plt.tight_layout()
#plt.show()

# esempio per zona di Milano
import matplotlib.pyplot as plt

# Filtra i dati solo per la zona di Milano
milano_data = join[join[zona] == 'Milano Zona MSB-000']

# Plotta l'andamento delle temperature per la zona di Milano
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(milano_data['Data'], milano_data[temperatura], color='blue')
ax.set_title('Andamento delle temperature a Milano Zona MSB-000')
ax.set_xlabel('Data')
ax.set_ylabel('Temperatura')
plt.tight_layout()
plt.show()

