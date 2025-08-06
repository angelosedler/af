import os
import praw
from dotenv import load_dotenv
from datetime import datetime, timezone
from pprint import pprint
from db import insert_user, insert_post  # funciones que vos definís en db.py

load_dotenv()

# Reddit client setup
try:
    reddit = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent="RedditScraperAssignment"
    )
    print("✅ Successfully connected to Reddit API")
except Exception as e:
    print(f"❌ Failed to initialize Reddit client: {e}")
    exit(1)

# Parameters (set manually here)
SUBREDDIT_NAME = "Palestine"
POST_LIMIT = 50

def scrape(subreddit_name: str, limit: int):
    """Scrape posts from a subreddit and save them to DB."""
    try:
        subreddit = reddit.subreddit(subreddit_name)
        print(f"🔍 Scraping r/{subreddit_name}, up to {limit} posts...")

        posts = list(subreddit.new(limit=limit))
        if not posts:
            print(f"⚠️ No posts found in r/{subreddit_name}")
            return

        for post in posts:
            try:
                # Handle username (unique fallback if author is None)
                username = str(post.author) if post.author else f"unknown_{post.id}"

                # Build user object for DB
                user_data = {
                    "username": username,
                    "created_utc": None,  # we could query redditor for account age
                    "total_posts": 1,
                    "radical_score": 0.0,
                    "explanation": None,
                    "prompt_id": None,
                    "notes": None
                }
                insert_user(user_data)

                # Build post object for DB
                post_data = {
                    "post_id": post.id,
                    "username": username,
                    "subreddit": subreddit_name,
                    "title": post.title,
                    "selftext": post.selftext,
                    "created_utc": datetime.fromtimestamp(
                        post.created_utc, tz=timezone.utc
                    ).isoformat(),
                    "radical_score": 0.0,
                    "language": "en",
                    "explanation": "Not yet scored",
                    "permalink": f"https://www.reddit.com{post.permalink}",
                    "url": post.url,
                    "image_url": None
                }

                # Try to extract image if preview exists
                if hasattr(post, "preview"):
                    try:
                        post_data["image_url"] = post.preview["images"][0]["source"]["url"]
                    except Exception:
                        pass

                insert_post(post_data)
                pprint({"user": user_data, "post": post_data})

            except Exception as e:
                print(f"⚠️ Failed to process a post: {e}")

        print(f"✅ Finished scraping. Total posts processed: {len(posts)}")

    except Exception as e:
        print(f"❌ Error scraping subreddit '{subreddit_name}': {e}")

if __name__ == "__main__":
    print("🚀 Starting subreddit scraper...")
    scrape(SUBREDDIT_NAME, POST_LIMIT)
