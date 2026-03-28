# app/app.py

import streamlit as st
import pandas as pd
import os

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
st.caption("Analyze Reddit data or your own text with ML-based mental health signals")

st.divider()

# -------------------------------
# 📌 SECTION 1: REDDIT ANALYSIS
# -------------------------------
st.header("🔎 Reddit Analysis")

col1, col2 = st.columns([2, 1])

with col1:
    subreddit = st.text_input("Subreddit", "depression")

with col2:
    num_posts = st.slider("Posts", 1, 20, 5)

if st.button("🚀 Fetch & Analyze"):

    with st.spinner("Analyzing posts..."):

        fetcher = RedditFetcher("dummy", "dummy", "dummy")
        posts = fetcher.fetch_posts(subreddit, limit=num_posts)

        pre = Preprocessor()
        texts = [pre.clean_text(p["text"]) for p in posts]

        predictor = Predictor(MODEL_PATH)
        labels, confidences = predictor.predict(texts)

        alert_system = AlertSystem()

        results = []

        for i in range(len(posts)):
            alert = alert_system.generate_alert(labels[i], confidences[i])

            results.append({
                "text": posts[i]["text"],
                "label": labels[i],
                "confidence": float(round(confidences[i], 2)),
                "alert": alert
            })

        df = pd.DataFrame(results)

        # Save
        storage = StorageManager(OUTPUT_PATH)
        storage.save_results(results)

        st.success("Analysis complete!")

        # -------------------------------
        # 📊 RESULTS
        # -------------------------------
        st.subheader("📊 Results")
        st.dataframe(df, use_container_width=True)

        # -------------------------------
        # 📈 CHARTS
        # -------------------------------
        st.subheader("📈 Distribution")

        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(df["label"].value_counts())

        with col2:
            st.write(df["label"].value_counts())

        # -------------------------------
        # 🚨 ALERTS
        # -------------------------------
        st.subheader("🚨 Alerts")

        for _, row in df.iterrows():
            if row["alert"] == "HIGH":
                st.error(f"🔴 {row['text']}")
            elif row["alert"] == "MEDIUM":
                st.warning(f"🟡 {row['text']}")
            else:
                st.success(f"🟢 {row['text']}")

st.divider()

# -------------------------------
# ✍️ SECTION 2: MANUAL INPUT
# -------------------------------
st.header("✍️ Analyze Your Own Text")

user_text = st.text_area("Enter text")

if st.button("🧠 Analyze Text"):

    if user_text.strip() == "":
        st.warning("Enter some text")
    else:
        pre = Preprocessor()
        clean_text = pre.clean_text(user_text)

        predictor = Predictor(MODEL_PATH)
        label, confidence = predictor.predict([clean_text])

        label = label[0]
        confidence = float(round(confidence[0], 2))

        alert_system = AlertSystem()
        alert = alert_system.generate_alert(label, confidence)

        st.subheader("Result")

        st.metric("Label", label)
        st.metric("Confidence", confidence)

        if alert == "HIGH":
            st.error("🔴 HIGH ALERT")
        elif alert == "MEDIUM":
            st.warning("🟡 MEDIUM ALERT")
        else:
            st.success("🟢 LOW ALERT")

st.divider()

# -------------------------------
# 📜 SECTION 3: HISTORY
# -------------------------------
st.header("📜 Analysis History")

search = st.text_input("🔍 Search history")

if os.path.exists(OUTPUT_PATH):

    history_df = pd.read_csv(OUTPUT_PATH)

    # Search filter
    if search:
        history_df = history_df[
            history_df["text"].str.contains(search, case=False, na=False)
        ]

    if not history_df.empty:
        st.dataframe(history_df.tail(15), use_container_width=True)
    else:
        st.info("No matching results")

else:
    st.info("No history yet")

# -------------------------------
# 🗑️ CLEAR HISTORY
# -------------------------------
if st.button("🗑️ Clear History"):
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)
        st.success("History cleared")