# src/preprocessing/preprocessor.py

import re

class Preprocessor:

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""

        text = text.lower()
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        return text.strip()