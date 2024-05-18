def Calcolo_picchi_alti_temperature(join,zona,percentile,temperatura):
    #Input: join= dataframe temperature-griglia geografica
    #zona= zona che vogliamo considerare
    #percentile= valore di percentile che vogliamo trovare per i picchi alti
    #temperatura= stringa del nome della colonna su cui possiamo trovare i valori delle temperature
    #Output:
    #picchi alti= valori picchi alti temperatura
    temperature_zone_data = join[['Data', temperatura, zona]]
    temperature_medie_zone_data = join.groupby(['Data', zona])[temperatura].mean().reset_index()

    # Calcolo la soglia alta con il percentile e la soglia bassa con 1-percentile
    soglia_alta = join[temperatura].quantile(percentile)
    # Individuo i rispettivi picchi
    picchi_alti = temperature_medie_zone_data[temperature_medie_zone_data[temperatura] > soglia_alta]
    return picchi_alti


