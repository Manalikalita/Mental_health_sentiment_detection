# src/storage/storage_manager.py

import pandas as pd
import os
from datetime import datetime


class StorageManager:

    def __init__(self, output_path):
        self.output_path = output_path

        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

    def save_results(self, results):

        # Convert to DataFrame
        df = pd.DataFrame(results)

        # Add timestamp column
        df["saved_at"] = datetime.now()

        # If file exists → append
        if os.path.exists(self.output_path):
            df.to_csv(self.output_path, mode='a', header=False, index=False)
        else:
            df.to_csv(self.output_path, index=False)

        print(f"💾 Results saved to {self.output_path}")