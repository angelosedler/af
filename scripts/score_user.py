import json
from core.db import (
    get_unscored_posts_by_user,
    get_posts_by_username,
    update_post_score,
    update_user_score,
)
from core.json_storage import (
    load_posts_from_json,
    save_posts_to_json,
    load_users_from_json,
    save_users_to_json,
)
from core.llm_scoring import score_post_with_llm
from core.user_scoring import calculate_user_score

# === Read input.json ===
with open("input.json", "r", encoding="utf-8") as f:
    config = json.load(f)

params = config.get("score_user", {})
username = params.get("username")
input_source = params.get("input", "json")
output_target = params.get("output", "json")
limit = params.get("limit", 50)

if not username:
    print("❌ You must provide a 'username' in the input.")
    exit()

# === Load posts for user ===
if input_source == "db":
    posts = get_unscored_posts_by_user(username, limit)
else:
    all_posts = load_posts_from_json()
    posts = [
        p for p in all_posts
        if p.get("username") == username
    ][:limit]

if not posts:
    print(f"⚠️ No posts found for user '{username}'.")
    exit()

print(f"🔍 Scoring posts for user '{username}'...")

scored_new_posts = []

for post in posts:
    if post.get("explanation") != "Not yet scored":
        continue

    try:
        score, explanation = score_post_with_llm(post)
        post["radical_score"] = score
        post["explanation"] = explanation

        if output_target == "db":
            update_post_score(post["post_id"], score, explanation)

        scored_new_posts.append(post)
        print(f"✅ Scored post {post['post_id']}: {score}")
    except Exception as e:
        print(f"⚠️ Error scoring post {post['post_id']}: {e}")

# Save scored posts if output is JSON
if output_target == "json" and scored_new_posts:
    save_posts_to_json(scored_new_posts)

# === Load all posts for user (including already scored) to calculate global score ===
if input_source == "db":
    all_user_posts = get_posts_by_username(username)
else:
    all_user_posts = [
        p for p in load_posts_from_json()
        if p.get("username") == username and "radical_score" in p
    ]

final_score, explanation = calculate_user_score(all_user_posts)

# === Save the new user score ===
if output_target == "db":
    update_user_score(username, final_score, explanation)
else:
    users = load_users_from_json()
    updated = False
    for u in users:
        if u.get("username") == username:
            u["radical_score"] = final_score
            u["explanation"] = explanation
            updated = True
            break
    if not updated:
        users.append({
            "username": username,
            "radical_score": final_score,
            "explanation": explanation,
            "created_utc": None,
            "total_posts": None,
            "prompt_id": None,
            "notes": None
        })
    save_users_to_json(users)

print(f"✅ Finished scoring user '{username}' → radical_score: {final_score}")
