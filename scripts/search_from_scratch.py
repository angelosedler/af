import os
import json
import praw
from dotenv import load_dotenv
from datetime import datetime, timezone
from langdetect import detect
from core.db import insert_user, insert_post
from core.json_storage import save_posts_to_json
import sys

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

load_dotenv()

# Read input.json
with open("input.json", "r", encoding="utf-8") as f:
    config = json.load(f)

params = config.get("search_from_scratch", {})
keywords = params.get("keywords", [])
usernames = params.get("usernames", [])
subreddits = params.get("subreddits", [])
limit = params.get("limit", 50)
output = params.get("output", "json")

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent="RedditScraperAssignment"
)

print("✅ Connected to Reddit")

results = []

def build_post_data(post):
    username = str(post.author) if post.author else f"unknown_{post.id}"
    text = f"{post.title} {post.selftext}".strip()

    try:
        lang = detect(text)
    except:
        lang = "unknown"

    post_data = {
        "post_id": post.id,
        "username": username,
        "subreddit": str(post.subreddit),
        "title": post.title,
        "selftext": post.selftext,
        "created_utc": datetime.fromtimestamp(post.created_utc, tz=timezone.utc).isoformat(),
        "radical_score": 0.0,
        "language": lang,
        "explanation": "Not yet scored",
        "permalink": f"https://www.reddit.com{post.permalink}",
        "url": post.url,
        "image_url": None
    }

    if hasattr(post, "preview"):
        try:
            post_data["image_url"] = post.preview["images"][0]["source"]["url"]
        except:
            pass

    return post_data

def process_post(post):
    post_data = build_post_data(post)
    user_data = {
        "username": post_data["username"],
        "created_utc": None,
        "total_posts": 1,
        "radical_score": 0.0,
        "explanation": None,
        "prompt_id": None,
        "notes": None
    }

    if output == "db":
        insert_user(user_data)
        insert_post(post_data)
    else:
        results.append({"user": user_data, "post": post_data})

### Search por subreddit
for sub in subreddits:
    print(f"🔍 Searching subreddit: r/{sub}")
    try:
        for post in reddit.subreddit(sub).new(limit=limit):
            process_post(post)
    except Exception as e:
        print(f"⚠️ Failed to fetch from subreddit '{sub}': {e}")

### Search por keyword
for keyword in keywords:
    print(f"🔍 Searching keyword: '{keyword}'")
    try:
        for post in reddit.subreddit("all").search(keyword, limit=limit):
            process_post(post)
    except Exception as e:
        print(f"⚠️ Failed to search keyword '{keyword}': {e}")

### Search por username
for user in usernames:
    print(f"🔍 Searching user: u/{user}")
    try:
        for post in reddit.redditor(user).submissions.new(limit=limit):
            process_post(post)
    except Exception as e:
        print(f"⚠️ Failed to fetch user '{user}': {e}")

### Si es JSON, guardamos
if output == "json":
    print("💾 Saving results to data/posts.json")
    save_posts_to_json([item["post"] for item in results])

print("✅ Search completed.")
