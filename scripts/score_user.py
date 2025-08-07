import json
from core.db import (
    get_unscored_posts_by_user,
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

# Leer input
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

# Cargar posts
if input_source == "db":
    posts = get_unscored_posts_by_user(username, limit)
else:
    all_posts = load_posts_from_json()
    posts = [p for p in all_posts if p.get("username") == username and p.get("explanation") == "Not yet scored"][:limit]

if not posts:
    print(f"⚠️ No unscored posts found for user '{username}'.")
    exit()

print(f"🔍 Scoring {len(posts)} posts for user '{username}'...")

scored_posts = []

for post in posts:
    try:
        score, explanation = score_post_with_llm(post)
        post["radical_score"] = score
        post["explanation"] = explanation

        if output_target == "db":
            update_post_score(post["post_id"], score, explanation)

        scored_posts.append(post)
        print(f"✅ Scored post {post['post_id']}: {score}")
    except Exception as e:
        print(f"⚠️ Error scoring post {post['post_id']}: {e}")

# Guardar posts actualizados
if output_target == "json":
    print("💾 Saving updated posts to data/posts.json")
    save_posts_to_json(posts_to_merge=scored_posts)

# Calcular score promedio de usuario
scores = [p["radical_score"] for p in scored_posts]
avg_score = sum(scores) / len(scores)
user_explanation = f"Average score from {len(scores)} posts: {round(avg_score, 2)}"

# Actualizar user
if output_target == "db":
    update_user_score(username, avg_score, user_explanation)
else:
    users = load_users_from_json()
    updated = False
    for u in users:
        if u.get("username") == username:
            u["radical_score"] = avg_score
            u["explanation"] = user_explanation
            updated = True
            break
    if not updated:
        print(f"⚠️ User '{username}' not found in users.json — creating new entry.")
        users.append({
            "username": username,
            "radical_score": avg_score,
            "explanation": user_explanation,
            "created_utc": None,
            "total_posts": None,
            "prompt_id": None,
            "notes": None
        })
    save_users_to_json(users)

print(f"✅ Finished scoring user '{username}' with avg score: {round(avg_score, 2)}")
