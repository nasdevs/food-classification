import pandas as pd

def load_nutrition_data(nutrition_path):
    nutrition_df = pd.read_csv(nutrition_path, dtype={'energi__kkal': 'float16', 'lemak_total__mg': 'float16', 'karbohidrat_total__mg': 'float16', 'protein__mg': 'float16'})
    labels = nutrition_df.kategori.values
    nutrition = nutrition_df.values[:, 1:]

    return labels, nutrition