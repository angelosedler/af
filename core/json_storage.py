import json
import os

def save_posts_to_json(posts, filename="data/posts.json"):
    os.makedirs("data", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"posts": posts}, f, indent=2, ensure_ascii=False)

def load_posts_from_json(filename="data/posts.json"):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("posts", [])
