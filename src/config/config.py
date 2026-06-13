# src/config/config.py

import os

# 🔐 Reddit API Credentials (PUT YOUR REAL VALUES)
REDDIT_CLIENT_ID = "your_client_id"
REDDIT_CLIENT_SECRET = "your_client_secret"
REDDIT_USER_AGENT = "mental-health-detector"

# Twitter API credentials
TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN", "")

# Model path
MODEL_PATH = "models/model_pipeline.pkl"

# Data paths
DATA_PATH = "data/raw/dataset.csv"
OUTPUT_PATH = "data/outputs/results.csv"

# Alert thresholds
HIGH_THRESHOLD = 0.75
MEDIUM_THRESHOLD = 0.5

# Social media defaults
DEFAULT_TWITTER_QUERY = "mental health"
DEFAULT_POST_LIMIT = 10