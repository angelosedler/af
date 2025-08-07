import json
from core.db import get_unscored_posts, update_post_score
from core.json_storage import load_posts_from_json, save_posts_to_json
from core.llm_scoring import score_post_with_llm

# Read input
with open("input.json", "r", encoding="utf-8") as f:
    config = json.load(f)

params = config.get("score_all_posts", {})
input_source = params.get("input", "json")
output_target = params.get("output", "json")
limit = params.get("limit", 100)

# Load posts
if input_source == "db":
    posts = get_unscored_posts(limit=limit)
else:
    all_data = load_posts_from_json()
    posts = [p for p in all_data if p.get("explanation") == "Not yet scored"][:limit]

if not posts:
    print("⚠️ No unscored posts found.")
    exit()

print(f"🔍 Scoring {len(posts)} posts using LLM...")

for post in posts:
    try:
        score, explanation = score_post_with_llm(post)
        post["radical_score"] = score
        post["explanation"] = explanation

        if output_target == "db":
            update_post_score(post["post_id"], score, explanation)

        print(f"✅ Post {post['post_id']} scored: {score}")
    except Exception as e:
        print(f"⚠️ Error scoring post {post.get('post_id', 'unknown')}: {e}")

# Save to JSON if needed
if output_target == "json":
    print("💾 Saving updated posts to data/posts.json")
    save_posts_to_json(posts)

print("✅ Scoring complete.")
