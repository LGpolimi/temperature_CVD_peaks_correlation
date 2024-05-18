import numpy as np
import pandas as pd
def finestra_percentili(window, percentile, zona, risultati):
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

    result_list = []
    for name, group in risultati.groupby(zona):
        group = group.copy()
        group['Percentili'] = group['media_mobile'].rolling(window=window, center=True, min_periods=1).apply(
            apply_custom_percentile, raw=True)
        result_list.append(group)

    risultati_finali = pd.concat(result_list)
    return risultati_finali

