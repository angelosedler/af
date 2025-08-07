import json
from core.db import (
    get_all_users,
    get_posts_by_username,
    update_post_score,
    update_user_score
)
from core.json_storage import (
    load_users_from_json,
    load_posts_from_json,
    save_users_to_json,
    save_posts_to_json
)
from core.llm_scoring import score_post_with_llm
from core.user_scoring import calculate_user_score

# Load input config
with open("input.json", "r", encoding="utf-8") as f:
    config = json.load(f)

params = config.get("score_all_users", {})
input_source = params.get("input", "json")
output_target = params.get("output", "json")
limit = params.get("limit", 50)

# Load users
if input_source == "db":
    users = get_all_users(limit=limit)
else:
    users = load_users_from_json()[:limit]

if not users:
    print("⚠️ No users found to score.")
    exit()

print(f"🔍 Scoring up to {len(users)} users...")

# Load all posts if using JSON
if input_source == "json":
    all_posts = load_posts_from_json()

updated_users = []
updated_posts = []

for user in users:
    username = user.get("username")
    if not username:
        continue

    # Get user's posts
    if input_source == "db":
        posts = get_posts_by_username(username)
    else:
        posts = [p for p in all_posts if p.get("username") == username]

    if not posts:
        print(f"⚠️ No posts found for user '{username}'")
        continue

    total = len(posts)
    unscored = [p for p in posts if p.get("explanation") == "Not yet scored"]

    print(f"\n🔍 Processing user '{username}' ({total} posts total, {len(unscored)} unscored)...")

    # Score unscored posts
    for post in unscored:
        try:
            score, explanation = score_post_with_llm(post)
            post["radical_score"] = score
            post["explanation"] = explanation

            if output_target == "db":
                update_post_score(post["post_id"], score, explanation)
            else:
                updated_posts.append(post)

            print(f"✅ Post {post['post_id']} scored: {score}")
        except Exception as e:
            print(f"⚠️ Failed to score post {post.get('post_id', 'unknown')}: {e}")

    # Recalculate radical_score for the user using ALL posts
    try:
        final_score, explanation = calculate_user_score(posts)
        user["radical_score"] = final_score
        user["explanation"] = explanation

        if output_target == "db":
            update_user_score(username, final_score, explanation)
        else:
            updated_users.append(user)

        print(f"✅ User scored: {final_score} → {explanation}")
    except Exception as e:
        print(f"❌ Failed to score user '{username}': {e}")

# Save updated data
if output_target == "json":
    print("\n💾 Saving updated users and posts to JSON...")
    save_users_to_json(updated_users)
    save_posts_to_json(updated_posts)

print("\n✅ All users processed.")
