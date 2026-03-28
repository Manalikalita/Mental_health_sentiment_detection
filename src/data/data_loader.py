# src/data/data_loader.py

import pandas as pd

def load_data(path):
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None