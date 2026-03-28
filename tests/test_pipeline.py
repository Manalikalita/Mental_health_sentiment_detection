# tests/test_pipeline.py

from src.data.reddit_fetcher import RedditFetcher
from src.preprocessing.preprocessor import Preprocessor
from src.models.predict_model import Predictor
from src.alert.alert_system import AlertSystem
from src.config.config import MODEL_PATH
from src.storage.storage_manager import StorageManager
from src.config.config import OUTPUT_PATH

def run_pipeline():

    print("🚀 Starting Full Pipeline...\n")

    # 1. Fetch Data (Fallback will be used)
    fetcher = RedditFetcher("dummy", "dummy", "dummy")
    posts = fetcher.fetch_posts("depression", limit=5)

    # 2. Preprocess
    pre = Preprocessor()
    texts = [pre.clean_text(p["text"]) for p in posts]

    # 3. Predict
    predictor = Predictor(MODEL_PATH)
    labels, confidences = predictor.predict(texts)

    # 4. Alert System
    alert_system = AlertSystem()

    results = []

    for i in range(len(posts)):
        alert = alert_system.generate_alert(labels[i], confidences[i])

        result = {
            "text": posts[i]["text"],
            "label": labels[i],
            "confidence": float(round(confidences[i], 2)),
            "alert": alert
        }

        results.append(result)

    # 5. Print Results
    print("\n📊 RESULTS:\n")
    for r in results:
        print(r)

    storage = StorageManager(OUTPUT_PATH)
    storage.save_results(results)

if __name__ == "__main__":
    run_pipeline()

# Save results