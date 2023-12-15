import pandas as pd

def load_nutrition_data(nutrition_path):
    nutrition_df = pd.read_csv(nutrition_path)
    labels = nutrition_df.kategori.values
    nutrition = nutrition_df.values[:, 1:]

    return labels, nutrition