# src/features/vectorizer.py

from sklearn.feature_extraction.text import TfidfVectorizer

def get_vectorizer():
    return TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2)
    )