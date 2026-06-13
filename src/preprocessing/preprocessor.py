# src/preprocessing/preprocessor.py

import re

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    nltk.data.find("tokenizers/punkt")
    nltk.data.find("corpora/stopwords")
    nltk.data.find("corpora/wordnet")
    nltk.data.find("corpora/omw-1.4")
    STOPWORDS = set(stopwords.words("english"))
    LEMMATIZER = WordNetLemmatizer()
except Exception:
    nltk = None
    STOPWORDS = {
        "a", "an", "the", "and", "or", "but", "if", "in", "on", "at",
        "for", "with", "without", "of", "to", "from", "by", "is", "it",
        "this", "that", "i", "you", "he", "she", "they", "we", "my",
        "your", "our", "me", "us", "them", "can", "will", "just", "too"
    }
    LEMMATIZER = None


class Preprocessor:

    def __init__(self):
        self.stopwords = STOPWORDS
        self.lemmatizer = LEMMATIZER

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""

        text = text.lower()
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"[^a-zA-Z\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        tokens = [token for token in text.split() if token not in self.stopwords and len(token) > 1]

        if self.lemmatizer is not None:
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]

        return " ".join(tokens)