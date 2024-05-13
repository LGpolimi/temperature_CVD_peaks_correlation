import pandas as pd
from Delta_temperature_tra_giorni import picchi_delta
from Media_mobile import picchi_media_mobile

picchi_delta = picchi_delta.rename(columns={'Data': 'DATA'})
picchi_delta = picchi_delta.rename(columns={'LMB3B_IDna': 'ZONA'})


picchi_delta['DATA']=pd.to_datetime(picchi_delta['DATA'])
picchi_media_mobile['DATA']=pd.to_datetime(picchi_media_mobile['DATA'])

# Aggiungi colonne per i giorni successivi al picco di temperatura
picchi_delta['DATA_1_giorno_dopo'] = picchi_delta['DATA'] + pd.DateOffset(days=1)
picchi_delta['DATA_2_giorni_dopo'] = picchi_delta['DATA'] + pd.DateOffset(days=2)


# Merge per trovare correlazioni nei due giorni successivi
df_merged_delta_1 = pd.merge(picchi_media_mobile, picchi_delta, left_on=['DATA', 'ZONA'], right_on=['DATA_1_giorno_dopo', 'ZONA'], how='inner')
df_merged_delta_2 = pd.merge(picchi_media_mobile, picchi_delta, left_on=['DATA', 'ZONA'], right_on=['DATA_2_giorni_dopo', 'ZONA'], how='inner')

# Concatena i risultati delle due merge
df_merged_delta = pd.concat([df_merged_delta_1, df_merged_delta_2], ignore_index=True)

# Rimuovi colonne aggiuntive
df_merged_delta.drop(columns=['DATA_1_giorno_dopo', 'DATA_2_giorni_dopo'], inplace=True)

# Seleziona solo le colonne desiderate
df_merged_delta = df_merged_delta[['Delta Temperatura Assoluto', 'media_mobile', 'DATA_x', 'ZONA']]
