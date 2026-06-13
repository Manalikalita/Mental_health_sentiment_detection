# src/models/train_model.py

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

# IMPORTS (IMPORTANT 🔥)
from src.data.data_loader import load_data
from src.preprocessing.preprocessor import Preprocessor
from src.features.vectorizer import get_vectorizer


MODEL_PATH = "models/model_pipeline.pkl"
DATA_PATH = "data/raw/dataset.csv"


def train_model(X, y, vectorizer, test_size=0.2, random_state=42):

    model = LogisticRegression(class_weight="balanced", max_iter=300)

    pipeline = Pipeline([
        ("tfidf", vectorizer),
        ("clf", model)
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )

    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, preds)

    print("✅ Evaluation results")
    print(f"Accuracy: {accuracy:.4f}")
    print(classification_report(y_test, preds, digits=4))

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