# src/models/predict_model.py

import joblib

class Predictor:

    def __init__(self, model_path):
        self.model = joblib.load(model_path)

    def predict(self, texts):
        preds = self.model.predict(texts)
        probs = self.model.predict_proba(texts).max(axis=1)
        return preds, probs