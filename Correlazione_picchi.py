from Estrazione_segnale_zone_temperature import picchi_alti
from Estrazione_segnale_zone_temperature import picchi_bassi
import pandas as pd
from Estrazione_segnale_zone_AREU import Picchi_pazienti
picchi_alti = picchi_alti.rename(columns={'Data': 'DATA'})
picchi_alti = picchi_alti.rename(columns={'LMB3B_IDna': 'ZONA'})

picchi_bassi = picchi_bassi.rename(columns={'Data': 'DATA'})
picchi_bassi = picchi_bassi.rename(columns={'LMB3B_IDna': 'ZONA'})
import pandas as pd
picchi_alti['DATA']=pd.to_datetime(picchi_alti['DATA'])
Picchi_pazienti['DATA']=pd.to_datetime(Picchi_pazienti['DATA'])
df_merged_caldo = pd.merge(Picchi_pazienti, picchi_alti, on=['DATA', 'ZONA'], how='outer', indicator=True)
# Filtrare il DataFrame per ottenere solo i casi in cui la colonna '_merge' è segnata come 'both'
df_both_caldo = df_merged_caldo[df_merged_caldo['_merge'] == 'both'].drop(columns=['_merge'])
import pandas as pd
picchi_bassi['DATA']=pd.to_datetime(picchi_bassi['DATA'])
Picchi_pazienti['DATA']=pd.to_datetime(Picchi_pazienti['DATA'])
df_merged_freddo = pd.merge(Picchi_pazienti, picchi_bassi, on=['DATA', 'ZONA'], how='outer', indicator=True)
# Filtrare il DataFrame per ottenere solo i casi in cui la colonna '_merge' è segnata come 'both'
df_both_freddo = df_merged_freddo[df_merged_freddo['_merge'] == 'both'].drop(columns=['_merge'])

somma_pazienti_picchi = Picchi_pazienti['numero_pazienti'].sum()
somma_pazienti_both_caldo= df_both_caldo['numero_pazienti'].sum()
somma_pazienti_both_freddo= df_both_freddo['numero_pazienti'].sum()