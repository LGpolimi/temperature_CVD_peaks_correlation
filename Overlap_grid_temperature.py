import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
def overlap_grid_temp (griglia_temperature,griglia_geografica):
    griglia_temperature['Data'] = pd.to_datetime(griglia_temperature['Data'])
    # Raggruppo i dati per giorno, latitudine e longitudine e calcola la media delle temperature
    temperature_giornaliere = griglia_temperature
    # creazione di un punto per ogni temperatura
    temperature_giornaliere['geometry'] = temperature_giornaliere.apply(
        lambda row: Point(row['Latitudine'], row['Longitudine']), axis=1)

    # GeoDataFrame dalle coordinate delle chiamate di emergenza
    geometry = [Point(xy) for xy in
                zip(temperature_giornaliere['Longitudine'], temperature_giornaliere['Latitudine'])]
    crs = {'init': 'epsg:32632'}
    gdf_temperatura = gpd.GeoDataFrame(temperature_giornaliere, crs=crs, geometry=geometry)

    # Spatial join tra le temperature e la griglia geografica--> formazione di nuova colonna index_right
    join = gpd.sjoin(gdf_temperatura, griglia_geografica, how="inner")
    return join

