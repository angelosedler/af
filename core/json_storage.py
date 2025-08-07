import json
import os

# === POSTS ===

def save_posts_to_json_overwrite(posts, filename="data/posts.json"):
    """Overwrite the posts.json file"""
    os.makedirs("data", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"posts": posts}, f, indent=2, ensure_ascii=False)

def save_posts_to_json(posts_to_merge, filename="data/posts.json"):
    """
    Merge posts with existing posts in posts.json.
    If the file doesn't exist, create it.
    """
    os.makedirs("data", exist_ok=True)

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        all_posts = data.get("posts", [])
    except FileNotFoundError:
        all_posts = []

    post_map = {p["post_id"]: p for p in all_posts}
    for new_post in posts_to_merge:
        post_map[new_post["post_id"]] = new_post

    merged = list(post_map.values())

    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"posts": merged}, f, indent=2, ensure_ascii=False)

def load_posts_from_json(filename="data/posts.json"):
    """Load all posts from posts.json"""
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("posts", [])

# === USERS ===

def save_users_to_json(users_to_merge, filename="data/users.json"):
    """
    Guarda los usuarios haciendo merge con los existentes.
    Si el archivo no existe, lo crea.
    """
    os.makedirs("data", exist_ok=True)

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        existing_users = data.get("users", [])
    except FileNotFoundError:
        existing_users = []

    user_map = {u["username"]: u for u in existing_users}
    for user in users_to_merge:
        user_map[user["username"]] = user  # sobrescribe si ya existía

    merged = list(user_map.values())

    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"users": merged}, f, indent=2, ensure_ascii=False)

def load_users_from_json(filename="data/users.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("users", [])
    except FileNotFoundError:
        return []