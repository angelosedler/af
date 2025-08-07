import json
from datetime import datetime
from core.db import (
    get_all_users_sorted_by_score,
    get_posts_by_username,
    insert_post
)
from core.json_storage import (
    load_users_from_json,
    load_posts_from_json,
    save_posts_to_json
)

# === Load config ===
with open("input.json", "r", encoding="utf-8") as f:
    config = json.load(f)

params = config.get("search_radicalized_users", {})
input_source = params.get("input", "json")
output_target = params.get("output", "json")
users_limit = params.get("users_limit")
post_limit = params.get("limit")
date_limit_str = params.get("date_limit")

date_limit = None
if date_limit_str:
    try:
        date_limit = datetime.strptime(date_limit_str, "%d/%m/%Y")
    except ValueError:
        print(f"❌ Invalid date format. Use dd/mm/yyyy → Got: {date_limit_str}")
        exit()

# === Load users sorted by radical_score descending ===
if input_source == "db":
    users = get_all_users_sorted_by_score(limit=users_limit)
else:
    all_users = load_users_from_json()
    sorted_users = sorted(
        all_users,
        key=lambda u: u.get("radical_score", 0),
        reverse=True
    )
    users = sorted_users[:users_limit] if users_limit else sorted_users

if not users:
    print("⚠️ No users found.")
    exit()

print(f"🔍 Selected top {len(users)} radicalized users")

# === Load all posts (only if input is json) ===
if input_source == "json":
    all_posts = load_posts_from_json()

collected_posts = []

for user in users:
    username = user.get("username")
    if not username:
        continue

    if input_source == "db":
        posts = get_posts_by_username(username)
    else:
        posts = [p for p in all_posts if p.get("username") == username]

    # Apply filters
    if date_limit:
        posts = [
            p for p in posts
            if "created_utc" in p and datetime.fromisoformat(p["created_utc"]) >= date_limit
        ]

    if post_limit:
        posts = posts[:post_limit]

    if not posts:
        print(f"⚠️ No posts found for user '{username}' after filtering.")
        continue

    print(f"✅ Collected {len(posts)} posts from user '{username}'")

    if output_target == "db":
        for post in posts:
            insert_post(post)
    else:
        collected_posts.extend(posts)

# === Save to JSON if needed ===
if output_target == "json":
    print("💾 Saving collected posts to data/posts.json")
    save_posts_to_json(collected_posts)

print("✅ Done. All filtered posts processed.")
