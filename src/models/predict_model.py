# src/models/predict_model.py

import warnings
import joblib
import numpy as np

class Predictor:

    POSITIVE_TERMS = {
        "happy", "joy", "joyful", "glad", "love", "great",
        "wonderful", "amazing", "awesome", "excited", "smile",
        "good", "peaceful", "optimistic", "relaxed", "fantastic"
    }

    OVERRIDE_LABELS = {
        "depression", "suicidal", "stress", "anxiety",
        "bipolar", "personality disorder"
    }

    def __init__(self, model_path):
        self.model = joblib.load(model_path)

    def predict(self, texts):
        preds = self.model.predict(texts)

        try:
            probs = self.model.predict_proba(texts).max(axis=1)
        except AttributeError:
            warnings.warn(
                "Model does not support predict_proba in this environment. "
                "Falling back to decision_function or default confidence values."
            )
            probs = self._fallback_confidence(texts, preds)
        except Exception as exc:
            warnings.warn(
                f"predict_proba failed ({exc}). Falling back to default confidence values."
            )
            probs = self._fallback_confidence(texts, preds)

        adjusted_labels = []
        adjusted_probs = []
        for text, label, prob in zip(texts, preds, probs):
            new_label, new_prob = self._apply_positive_override(text, label, prob)
            adjusted_labels.append(new_label)
            adjusted_probs.append(new_prob)

        return np.array(adjusted_labels), np.array(adjusted_probs)

    def _apply_positive_override(self, text, label, probability):
        if not isinstance(label, str):
            return label, probability

        normalized = label.strip().lower()
        if normalized in self.OVERRIDE_LABELS and probability < 0.45:
            tokens = set(text.lower().split())
            if tokens & self.POSITIVE_TERMS:
                return "Normal", max(probability, 0.55)

        return label, probability

    def _fallback_confidence(self, texts, preds):
        if hasattr(self.model, "decision_function"):
            try:
                decision = self.model.decision_function(texts)
                if decision.ndim == 1:
                    probs = 1 / (1 + np.exp(-decision))
                else:
                    exp_decision = np.exp(decision - np.max(decision, axis=1, keepdims=True))
                    probs = exp_decision / np.sum(exp_decision, axis=1, keepdims=True)
                    probs = probs.max(axis=1)
                return np.clip(probs, 0.0, 1.0)
            except Exception:
                pass

        return np.array([0.5] * len(preds), dtype=float)
