import os
import re
import pandas as pd
import geopandas as gpd
# Creazione cartella dove andrò a salvare i file csv
os.makedirs("results", exist_ok=True)

# Regex per estrarre i numeri--> il programma saprà cosa andare a cercare nei file per poi estrarlo
pattern = "[+-]?[0-9]+\.?[0-9]*"

# Ciclo su tutti i files
cartella = "TEMP2m_ytd2018/"
files = os.listdir(cartella)
dfs = []
for file in files:

    print("Lettura del file:", file)

    # Estrazione data e ora dal nome del file
    data_ora_str = file.split("_")[1]
    data = pd.to_datetime(data_ora_str[:8], format='%Y%m%d')
    ora = int(data_ora_str[8:10])  # Estrarre l'ora

    # Lettura dei file ed estrazione dei valori
    with open(cartella + file, "r") as f:
        # Leggi righe
        text = f.read()
        # Estraggo valori
        valori = re.findall(pattern, text)
        # Estraggo i primi 6 valori e li rimuovo
        ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value = list(map(float, valori[:6]))
        valori = valori[6:]

    # Creazione pandas dataframe con calcolo latitudine e longitudine
    df = pd.Series(valori, name="Temperatura").astype(float).to_frame()
    df["idx"] = df.index
    df["Data"] = data
    df["Ora"] = ora
    df["Latitudine"] = yllcorner + (nrows - 1 - df["idx"] // ncols) * cellsize
    df["Longitudine"] = xllcorner + (df["idx"] % ncols) * cellsize

    # Rimuovi colonna idx e ordina colonne
    df.drop("idx", axis=1, inplace=True)
    cols = df.columns.to_list()
    cols.remove("Temperatura")
    cols.append("Temperatura")
    df = df[cols]

    # Rimuovi righe contenenti NODATA_value
    df["Temperatura"] = df["Temperatura"].apply(lambda x: None if x == NODATA_value else x)
    df.dropna(inplace=True)

    # Append df
    dfs.append(df)

    # Save result to file
    df.to_csv("results/" + file.replace(".txt", ".csv"), index=False, sep=";")

# Put together dfs
print("Salva risultati in results/totale.csv")
df_final = pd.concat(dfs)

# Converte longitudine e latitudine da EPSG 3003(Coordinate Gauss Boaga) in EPSG 32632 utilizzando Geopandas
gdf = gpd.GeoDataFrame(df_final, geometry=gpd.points_from_xy(df_final.Longitudine, df_final.Latitudine), crs='EPSG:3003')
gdf = gdf.to_crs(epsg=32632)
df_final['Longitudine'], df_final['Latitudine'] = gdf.geometry.x, gdf.geometry.y

#salvo il file totale in CSV
df_final.to_csv("results/totale.csv", index=False, sep=";")