import importlib.util
import sys
from pathlib import Path

import os
from datetime import datetime
from typing import List, Dict


def _load_snscrape_twitter():
    try:
        import snscrape
        twitter_path = Path(snscrape.__file__).parent / "modules" / "twitter.py"
        if not twitter_path.exists():
            return None

        module_name = "snscrape.modules.twitter"
        spec = importlib.util.spec_from_file_location(module_name, twitter_path)
        if spec is None or spec.loader is None:
            return None

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except Exception:
        return None


sntwitter = _load_snscrape_twitter()
HAS_SNSCRAPE = sntwitter is not None


class TwitterFetcher:

    TWITTER_SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"

    def __init__(self, bearer_token: str = None):
        self.bearer_token = (bearer_token or os.environ.get("TWITTER_BEARER_TOKEN", "")).strip()
        self.available = bool(self.bearer_token)
        self.last_error = None

        if not self.available:
            self.last_error = "Twitter bearer token not configured; will attempt snscrape if available."

    def fetch_tweets(self, query: str, limit: int = 10, save_csv: str = None) -> List[Dict]:
        """Fetch tweets for a query.

        Order of attempts:
        1. Official Twitter API (if `TWITTER_BEARER_TOKEN` configured)
        2. `snscrape` (if installed)
        3. Local fallback sample data

        If `save_csv` is provided, the resulting tweets will be written as a CSV.
        """
        # 1) Try official API
        if self.available:
            try:
                tweets = self._fetch_from_twitter(query, limit)
                if tweets:
                    if save_csv:
                        self._save_to_csv(tweets, save_csv)
                    return tweets
                self.last_error = "Twitter API returned no tweets."
            except Exception as e:
                self.last_error = f"Twitter API failed: {e}"

        # 2) Try snscrape if available
        if HAS_SNSCRAPE:
            try:
                tweets = self._fetch_with_snscrape(query, limit)
                if tweets:
                    if save_csv:
                        self._save_to_csv(tweets, save_csv)
                    return tweets
                self.last_error = "snscrape returned no tweets."
            except Exception as e:
                self.last_error = f"snscrape failed: {e}"

        # 3) Fallback
        tweets = self.get_fallback_data(limit)
        if save_csv:
            self._save_to_csv(tweets, save_csv)
        return tweets

    def _fetch_from_twitter(self, query: str, limit: int) -> List[Dict]:
        import requests

        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "User-Agent": "mental-health-detector"
        }
        params = {
            "query": query,
            "max_results": min(max(limit, 1), 100),
            "tweet.fields": "created_at",
            "expansions": "author_id",
            "user.fields": "username"
        }

        response = requests.get(self.TWITTER_SEARCH_URL, headers=headers, params=params, timeout=20)
        if response.status_code != 200:
            raise RuntimeError(f"{response.status_code} - {response.text}")

        payload = response.json()
        users = {u["id"]: u["username"] for u in payload.get("includes", {}).get("users", [])}

        tweets = []
        for tweet in payload.get("data", [])[:limit]:
            author_id = tweet.get("author_id")
            username = users.get(author_id, "")
            tweets.append({
                "text": tweet.get("text", ""),
                "timestamp": tweet.get("created_at"),
                "username": username,
                "url": f"https://twitter.com/{username}/status/{tweet.get('id')}" if username else ""
            })

        return tweets

    def _fetch_with_snscrape(self, query: str, limit: int) -> List[Dict]:
        if not HAS_SNSCRAPE:
            raise RuntimeError("snscrape is not installed")

        tweets = []
        for i, t in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i >= limit:
                break
            username = getattr(t.user, "username", "") if getattr(t, "user", None) else ""
            tweet_id = getattr(t, "id", None)
            tweets.append({
                "text": getattr(t, "content", "") or getattr(t, "rawContent", ""),
                "timestamp": getattr(t, "date", datetime.now()),
                "username": username,
                "url": f"https://twitter.com/{username}/status/{tweet_id}" if username and tweet_id else ""
            })

        return tweets

    def _save_to_csv(self, tweets: List[Dict], path: str) -> None:
        try:
            import pandas as pd
        except Exception:
            # pandas is optional; ignore save if not available
            return

        df = pd.DataFrame(tweets)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False)

    def get_fallback_data(self, limit: int = 10) -> List[Dict]:
        fallback = [
            "I feel empty and tired of everything",
            "I am very stressed about my exams",
            "Life is going well today",
            "I feel anxious all the time",
            "I don't enjoy things anymore",
            "I'm feeling motivated and happy",
            "Everything feels overwhelming lately",
            "I can't focus and feel lost",
            "Today was a good day",
            "I feel sad and alone"
        ]

        data = []
        for i in range(min(limit, len(fallback))):
            data.append({
                "text": fallback[i],
                "timestamp": datetime.now(),
                "username": "fallback",
                "url": ""
            })

        return data