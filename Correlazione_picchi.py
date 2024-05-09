from Estrazione_segnale_zone_temperature import picchi_alti
from Estrazione_segnale_zone_temperature import picchi_bassi
import pandas as pd
from Media_mobile import picchi_media_mobile
picchi_alti = picchi_alti.rename(columns={'Data': 'DATA'})
picchi_alti = picchi_alti.rename(columns={'LMB3B_IDna': 'ZONA'})

picchi_bassi = picchi_bassi.rename(columns={'Data': 'DATA'})
picchi_bassi = picchi_bassi.rename(columns={'LMB3B_IDna': 'ZONA'})
import pandas as pd
picchi_alti['DATA']=pd.to_datetime(picchi_alti['DATA'])
picchi_media_mobile['DATA']=pd.to_datetime(picchi_media_mobile['DATA'])
df_merged_caldo = pd.merge(picchi_media_mobile, picchi_alti, on=['DATA', 'ZONA'], how='outer', indicator=True)
# Filtrare il DataFrame per ottenere solo i casi in cui la colonna '_merge' è segnata come 'both'
df_both_caldo = df_merged_caldo[df_merged_caldo['_merge'] == 'both'].drop(columns=['_merge'])
import pandas as pd
picchi_bassi['DATA']=pd.to_datetime(picchi_bassi['DATA'])
picchi_media_mobile['DATA']=pd.to_datetime(picchi_media_mobile['DATA'])
df_merged_freddo = pd.merge(picchi_media_mobile, picchi_bassi, on=['DATA', 'ZONA'], how='outer', indicator=True)
# Filtrare il DataFrame per ottenere solo i casi in cui la colonna '_merge' è segnata come 'both'
df_both_freddo = df_merged_freddo[df_merged_freddo['_merge'] == 'both'].drop(columns=['_merge'])
