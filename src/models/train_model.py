# src/models/train_model.py

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# IMPORTS (IMPORTANT 🔥)
from src.data.data_loader import load_data
from src.preprocessing.preprocessor import Preprocessor
from src.features.vectorizer import get_vectorizer


MODEL_PATH = "models/model_pipeline.pkl"
DATA_PATH = "data/raw/dataset.csv"


def train_model(X, y, vectorizer):

    model = LogisticRegression(class_weight="balanced", max_iter=200)

    pipeline = Pipeline([
        ("tfidf", vectorizer),
        ("clf", model)
    ])

    pipeline.fit(X, y)

    joblib.dump(pipeline, MODEL_PATH)

    return pipeline


if __name__ == "__main__":

    print("🚀 Loading dataset...")
    df = load_data(DATA_PATH)

    if df is None:
        exit()

    print("🧹 Preprocessing text...")
    pre = Preprocessor()
    df["text"] = df["text"].apply(pre.clean_text)

    X = df["text"]
    y = df["label"]

    print("🔢 Vectorizing...")
    vectorizer = get_vectorizer()

    print("🤖 Training model...")
    train_model(X, y, vectorizer)

    print("✅ Model saved at:", MODEL_PATH)