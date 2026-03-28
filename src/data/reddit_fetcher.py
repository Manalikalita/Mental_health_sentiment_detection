# src/data/reddit_fetcher.py

import praw
from datetime import datetime


class RedditFetcher:

    def __init__(self, client_id, client_secret, user_agent):
        try:
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
            self.working = True
        except Exception as e:
            print("❌ Reddit API init failed:", e)
            self.working = False

    def fetch_posts(self, subreddit_name, limit=10):

        posts_data = []

        # 🚨 TRY REAL API
        if self.working:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)

                for post in subreddit.new(limit=limit):
                    text = f"{post.title} {post.selftext}"

                    posts_data.append({
                        "text": text,
                        "timestamp": datetime.fromtimestamp(post.created_utc)
                    })

                print(f"✅ Fetched {len(posts_data)} posts from r/{subreddit_name}")
                return posts_data

            except Exception as e:
                print("⚠️ API failed, using fallback:", e)

        # 🟡 FALLBACK DATA (VERY IMPORTANT 🔥)
        return self.get_fallback_data(limit)

    def get_fallback_data(self, limit):

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
                "timestamp": datetime.now()
            })

        print("⚠️ Using fallback data")
        return data