
def preprocessing(missdab):
    import pandas as pd
    dataframe = pd.DataFrame(missdab)
    dataframe = dataframe[['ZONA', 'COMUNE', 'PROV', 'ID_PZ', 'ID_SOCC', 'CD_OPERATOR_SK', 'DATA', 'ORA', 'MOTIVO_DTL',
                       'CD_FLT', 'GEN', 'ETA', 'LUOGO', 'LONG', 'LAT', 'INVIO_MSA1', 'INVIO_MSA2', 'ASSISTENZA_MAX',
                       'ID_MISS',
                       'CD_MISS', 'CD_TRA']]
    dataframe = dataframe.rename(columns={'ID_PZ': 'ID_PAZIENTE'})
    month_map = {'JAN': 'Jan', 'FEB': 'Feb', 'MAR': 'Mar', 'APR': 'Apr', 'MAY': 'May', 'JUN': 'Jun',
                 'JUL': 'Jul', 'AUG': 'Aug', 'SEP': 'Sep', 'OCT': 'Oct', 'NOV': 'Nov', 'DEC': 'Dec'}

    for column_name, var in dataframe[['DATA', 'INVIO_MSA1', 'INVIO_MSA2']].items():
        var = var.astype(str)  # Converti la Series in stringa
        for month_abbr, month_full in month_map.items():
            var = var.str.replace(month_abbr, month_full)

        try:
            formato = '%d%b%Y:%H:%M:%S.%f'
            var = pd.to_datetime(var, format=formato, errors='coerce')
        except ValueError:
            print(f"Errore")

        dataframe[column_name] = var
    dataframe = dataframe.loc[dataframe['MOTIVO_DTL'].isin(['CARDIOCIRCOLATORIA', 'RESPIRATORIA'])]
    media = round(dataframe['ETA'].mean())
    dataframe.fillna({'ETA': media}, inplace=True)
    return dataframe