from Delta_temperature_tra_giorni import picchi_delta

import pandas as pd
from Media_mobile import picchi_media_mobile
picchi_delta = picchi_delta.rename(columns={'Data': 'DATA'})
picchi_delta = picchi_delta.rename(columns={'LMB3B_IDna': 'ZONA'})

import pandas as pd
picchi_delta['DATA']=pd.to_datetime(picchi_delta['DATA'])
picchi_media_mobile['DATA']=pd.to_datetime(picchi_media_mobile['DATA'])
df_merged_delta = pd.merge(picchi_media_mobile, picchi_delta, on=['DATA', 'ZONA'], how='outer', indicator=True)
# Filtrare il DataFrame per ottenere solo i casi in cui la colonna '_merge' è segnata come 'both'
df_both_delta = df_merged_delta[df_merged_delta['_merge'] == 'both'].drop(columns=['_merge'])

