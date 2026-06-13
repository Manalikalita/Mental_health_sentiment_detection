# app.py

import os
import sys
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

sys.path.append(os.path.dirname(__file__))

from src.alert.alert_system import AlertSystem
from src.config.config import DEFAULT_POST_LIMIT, DEFAULT_TWITTER_QUERY, MODEL_PATH, OUTPUT_PATH, TWITTER_BEARER_TOKEN
from src.data.twitter_fetcher import TwitterFetcher, HAS_SNSCRAPE
from src.models.predict_model import Predictor
from src.preprocessing.preprocessor import Preprocessor
from src.storage.storage_manager import StorageManager


st.set_page_config(
    page_title="Mental Health Sentiment Detection",
    layout="wide"
)

st.title("🧠 Mental Health Sentiment Detection System")
st.caption("Analyze text or public tweets for mental health sentiment.")

st.divider()

# Sidebar controls
with st.sidebar:
    st.header("Input Options")
    use_twitter = st.checkbox("Enable Twitter search", value=True)
    twitter_query = st.text_input("Twitter search query", DEFAULT_TWITTER_QUERY)
    twitter_limit = st.slider("Tweet count", 5, 30, DEFAULT_POST_LIMIT)
    twitter_token = st.text_input("Twitter Bearer Token", value=TWITTER_BEARER_TOKEN, type="password")
    st.markdown("---")
    st.markdown(
        "This app uses a local ML model and public tweet text. Enter a Twitter Bearer Token to fetch live tweets via the official API."
    )

# Tabs for different input sources
tabs = st.tabs(["Manual Text", "Twitter Search"])

with tabs[0]:
    st.header("✍️ Manual Text Analysis")
    user_text = st.text_area("Enter your text here:", height=180)

    if st.button("Analyze Text"):
        if not user_text.strip():
            st.warning("Please enter some text to analyze.")
        else:
            pre = Preprocessor()
            cleaned = pre.clean_text(user_text)

            predictor = Predictor(MODEL_PATH)
            label, confidence = predictor.predict([cleaned])
            label = label[0]
            confidence = float(round(confidence[0], 2))
            alert = AlertSystem().generate_alert(label, confidence)

            result = {
                "text": user_text,
                "cleaned_text": cleaned,
                "label": label,
                "confidence": confidence,
                "alert": alert,
                "source": "manual",
                "saved_at": datetime.now()
            }

            StorageManager(OUTPUT_PATH).save_results([result])

            st.success("Analysis complete!")
            st.write("**Predicted sentiment:**", label)
            st.write("**Confidence:**", confidence)
            st.write("**Alert level:**", alert)

with tabs[1]:
    st.header("🐦 Twitter Search Analysis")
    if not use_twitter:
        st.info("Enable Twitter search in the sidebar to analyze public tweets.")
    else:
        if st.button("Fetch Tweets and Analyze"):
            if not twitter_query.strip():
                st.warning("Enter a search query for public tweets.")
            else:
                fetcher = TwitterFetcher(bearer_token=twitter_token)

                # Show which method will be used
                if fetcher.available:
                    st.info("Using Twitter API (bearer token provided)")
                elif HAS_SNSCRAPE:
                    st.info("Using snscrape to fetch public tweets (no Twitter API token required)")
                else:
                    st.info("Using built-in fallback tweets (install snscrape for real tweets)")

                tweets = fetcher.fetch_tweets(twitter_query, limit=twitter_limit)

                if fetcher.last_error:
                    st.warning(f"Tweet fetch warning: {fetcher.last_error}")

                if not tweets:
                    st.warning("No tweets were retrieved.")
                else:
                    pre = Preprocessor()
                    texts = [pre.clean_text(tweet["text"]) for tweet in tweets]
                    predictor = Predictor(MODEL_PATH)
                    labels, confidences = predictor.predict(texts)

                    results = []
                    for tweet, label, confidence in zip(tweets, labels, confidences):
                        alert = AlertSystem().generate_alert(label, confidence)
                        results.append({
                            "text": tweet["text"],
                            "label": label,
                            "confidence": float(round(confidence, 2)),
                            "alert": alert,
                            "username": tweet.get("username", ""),
                            "url": tweet.get("url", ""),
                            "timestamp": tweet.get("timestamp"),
                            "source": "twitter"
                        })

                    StorageManager(OUTPUT_PATH).save_results(results)

                    df = pd.DataFrame(results)
                    st.success(f"Analyzed {len(results)} tweets.")
                    st.dataframe(df[["username", "text", "label", "confidence", "alert"]].head(20), use_container_width=True)

                    st.subheader("Sentiment counts")
                    st.bar_chart(df["label"].value_counts())

st.divider()

st.header("📜 Analysis History")
search = st.text_input("Search history")

if os.path.exists(OUTPUT_PATH):
    try:
        history_df = pd.read_csv(OUTPUT_PATH)
    except Exception:
        st.warning("History file is invalid or corrupted. Clearing history file.")
        os.remove(OUTPUT_PATH)
        history_df = pd.DataFrame()

    if not history_df.empty:
        if search:
            history_df = history_df[history_df["text"].str.contains(search, case=False, na=False)]
        if not history_df.empty:
            st.dataframe(history_df.tail(20), use_container_width=True)
        else:
            st.info("No matching history records.")
    else:
        st.info("No history yet.")
else:
    st.info("No history yet.")

if st.button("Clear History"):
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)
        st.success("History cleared")
