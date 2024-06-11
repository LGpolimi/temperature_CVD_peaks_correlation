import numpy as np
import pandas as pd
# Calcola la finestra sui pazienti totali e ne ricava i percentili
def finestra_globale_percentili(window, percentile, risultati):
    def custom_percentile(window, percentile):
        center_index = len(window) // 2
        if len(window) > 1:
            new_window = np.delete(window, center_index)
        else:
            new_window = window

        # Debug: stampa la finestra e il percentile calcolato
        print("Window:", new_window)
        print("Percentile:", percentile)
        print("Calculated percentile value:", np.percentile(new_window, percentile))

        return np.percentile(new_window, percentile)

    def apply_custom_percentile(window):
        return custom_percentile(window, percentile)

    risultati['Percentili'] = risultati['media_mobile_totale_normalizzata'].rolling(window=window, center=True,
                                                                                    min_periods=1).apply(
        apply_custom_percentile, raw=True)

    return risultati
