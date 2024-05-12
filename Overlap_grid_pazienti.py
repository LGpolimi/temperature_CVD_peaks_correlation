def overlap_grid_pazienti (dataframe,griglia):
    # Filtriamo le righe duplicate basate su 'ID_PAZIENTE'
    dataframe = dataframe.drop_duplicates(subset='ID_PAZIENTE', keep='first')
    import geopandas as gpd
    griglia = gpd.GeoDataFrame(griglia)

    # ora dobbiamo cambiare l'EPSG al dataframe coi dati delle chiamate, in modo che le coordinate siano
    # tutte nella stessa unità di misura --> da EPSG 32632 a EPSG 4326
    from pyproj import Proj, transform
    def convert_to_meters(lat_deg, long_deg):
        in_proj = Proj(init='epsg:4326')  # Sistema di riferimento di partenza (WGS 84)
        out_proj = Proj('epsg:32632')  # Sistema di riferimento EPSG:32632 (UTM zone 32N)
        # Converti le coordinate da gradi decimali a metri
        x, y = transform(in_proj, out_proj, long_deg, lat_deg)
        return x, y

    # Applica la funzione ai dati nel dataframe
    dataframe.loc[:, 'X'], dataframe.loc[:, 'Y'] = convert_to_meters(dataframe['LAT'], dataframe['LONG'])

    # Ora il DataFrame contiene due nuove colonne con le coordinate convertite in metri
    import geopandas as gpd
    from shapely.geometry import Point

    # Crea un punto ogni paziente
    dataframe['geometry'] = dataframe.apply(lambda row: Point(row['X'], row['Y']), axis=1)

    # GeoDataFrame dalle coordinate dei soccorsi dei pazienti
    geometry = [Point(xy) for xy in zip(dataframe['X'], dataframe['Y'])]
    crs = {'init': 'epsg:32632'}
    gdf_pazienti = gpd.GeoDataFrame(dataframe, crs=crs, geometry=geometry)

    # Spatial join tra le chiamate di emergenza e la griglia geografica
    join = gpd.sjoin(gdf_pazienti, griglia, how="inner")
    return join
