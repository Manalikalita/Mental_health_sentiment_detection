# app/app.py

import streamlit as st
import pandas as pd

# Imports from your project
from src.data.reddit_fetcher import RedditFetcher
from src.preprocessing.preprocessor import Preprocessor
from src.models.predict_model import Predictor
from src.alert.alert_system import AlertSystem
from src.storage.storage_manager import StorageManager
from src.config.config import MODEL_PATH, OUTPUT_PATH


# -------------------------------
# 🚀 PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Mental Health Signal Detection",
    layout="wide"
)

st.title("🧠 Mental Health Signal Detection System")

# -------------------------------
# 🧾 USER INPUT
# -------------------------------
subreddit = st.text_input("Enter Subreddit", "depression")
num_posts = st.slider("Number of Posts", 1, 20, 5)

# -------------------------------
# 🔘 BUTTON
# -------------------------------
if st.button("Fetch & Analyze"):

    st.info("Fetching data and analyzing...")

    # 1. Fetch Data
    fetcher = RedditFetcher("dummy", "dummy", "dummy")
    posts = fetcher.fetch_posts(subreddit, limit=num_posts)

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

        results.append({
            "Text": posts[i]["text"],
            "Label": labels[i],
            "Confidence": float(round(confidences[i], 2)),
            "Alert": alert
        })

    # Convert to DataFrame
    df = pd.DataFrame(results)

    # 5. Save results
    storage = StorageManager(OUTPUT_PATH)
    storage.save_results(results)

    # -------------------------------
    # 📊 DISPLAY RESULTS
    # -------------------------------
    st.subheader("📊 Analysis Results")
    st.dataframe(df)

    # -------------------------------
    # 📈 CHARTS
    # -------------------------------
    st.subheader("📈 Sentiment Distribution")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Bar Chart")
        st.bar_chart(df["Label"].value_counts())

    with col2:
        st.write("Pie Chart")
        st.write(df["Label"].value_counts())

    # -------------------------------
    # 🚨 ALERT DISPLAY
    # -------------------------------
    st.subheader("🚨 Alerts")

    for _, row in df.iterrows():
        if row["Alert"] == "HIGH":
            st.error(f"🔴 HIGH: {row['Text']}")
        elif row["Alert"] == "MEDIUM":
            st.warning(f"🟡 MEDIUM: {row['Text']}")
        else:
            st.success(f"🟢 LOW: {row['Text']}")