from Estrazione_segnale_zone_temperature import picchi_alti
from Estrazione_segnale_zone_temperature import picchi_bassi
from Media_mobile import picchi_media_mobile
import pandas as pd

picchi_alti = picchi_alti.rename(columns={'Data': 'DATA'})
picchi_alti = picchi_alti.rename(columns={'LMB3B_IDna': 'ZONA'})

picchi_bassi = picchi_bassi.rename(columns={'Data': 'DATA'})
picchi_bassi = picchi_bassi.rename(columns={'LMB3B_IDna': 'ZONA'})

picchi_alti['DATA']=pd.to_datetime(picchi_alti['DATA'])
picchi_media_mobile['DATA']=pd.to_datetime(picchi_media_mobile['DATA'])

# Aggiungi colonne per i giorni successivi al picco di temperatura
picchi_alti['DATA_1_giorno_dopo'] = picchi_alti['DATA'] + pd.DateOffset(days=1)
picchi_alti['DATA_2_giorni_dopo'] = picchi_alti['DATA'] + pd.DateOffset(days=2)

picchi_bassi['DATA_1_giorno_dopo'] = picchi_bassi['DATA'] + pd.DateOffset(days=1)
picchi_bassi['DATA_2_giorni_dopo'] = picchi_bassi['DATA'] + pd.DateOffset(days=2)

# Merge per trovare correlazioni nei due giorni successivi
df_merged_caldo_1 = pd.merge(picchi_media_mobile, picchi_alti, left_on=['DATA', 'ZONA'], right_on=['DATA_1_giorno_dopo', 'ZONA'], how='inner')
df_merged_caldo_2 = pd.merge(picchi_media_mobile, picchi_alti, left_on=['DATA', 'ZONA'], right_on=['DATA_2_giorni_dopo', 'ZONA'], how='inner')

df_merged_freddo_1 = pd.merge(picchi_media_mobile, picchi_bassi, left_on=['DATA', 'ZONA'], right_on=['DATA_1_giorno_dopo', 'ZONA'], how='inner')
df_merged_freddo_2 = pd.merge(picchi_media_mobile, picchi_bassi, left_on=['DATA', 'ZONA'], right_on=['DATA_2_giorni_dopo', 'ZONA'], how='inner')

# Concatena i risultati delle due merge
df_merged_caldo = pd.concat([df_merged_caldo_1, df_merged_caldo_2], ignore_index=True)
df_merged_freddo = pd.concat([df_merged_freddo_1, df_merged_freddo_2], ignore_index=True)

# Rimuovi colonne aggiuntive
df_merged_caldo.drop(columns=['DATA_1_giorno_dopo', 'DATA_2_giorni_dopo'], inplace=True)
df_merged_freddo.drop(columns=['DATA_1_giorno_dopo', 'DATA_2_giorni_dopo'], inplace=True)

# Seleziona solo le colonne desiderate
df_merged_caldo = df_merged_caldo[['Temperatura', 'media_mobile', 'DATA_x', 'ZONA']]
df_merged_freddo = df_merged_freddo[['Temperatura', 'media_mobile', 'DATA_x', 'ZONA']]
