from supabase import create_client
from dotenv import load_dotenv
import os
import time
from core.llm_scoring import score_post_with_llm

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def get_posts(filter_type: str, value: str):
    """
    Returns all posts matching the given filter (subreddit or username)
    """
    if filter_type == "subreddit":
        result = supabase.table("posts").select("*").eq("subreddit", value).execute()
    elif filter_type == "username":
        result = supabase.table("posts").select("*").eq("username", value).execute()
    else:
        raise ValueError("Invalid filter_type. Use 'subreddit' or 'username'.")

    return result.data if result.data else []

def score_posts_from(filter_type: str, value: str):
    batch_start_time = time.time()
    posts = get_posts(filter_type, value)
    if not posts:
        print(f"⚠️ No posts found for {filter_type}: {value}")
        return

    print(f"🔎 Scoring {len(posts)} posts from {filter_type} = {value}")
    
    processed_posts = 0
    total_post_time = 0

    for post in posts:
        try:
            post_start_time = time.time()
            
            post_input = {
                "title": post.get("title", ""),
                "selftext": post.get("selftext", "")
            }

            score, explanation = score_post_with_llm(post_input)

            update_data = {
                "radical_score": score,
                "explanation": explanation
            }

            supabase.table("posts").update(update_data).eq("post_id", post["post_id"]).execute()
            
            post_time = time.time() - post_start_time
            total_post_time += post_time
            processed_posts += 1
            
            print(f"✅ Updated post {post['post_id']} with score {score} (took {post_time:.2f}s)")

        except Exception as e:
            print(f"⚠️ Failed to process post {post.get('post_id', 'unknown')}: {e}")

    # Print final statistics
    total_time = time.time() - batch_start_time
    avg_time = total_post_time / processed_posts if processed_posts > 0 else 0
    
    print(f"\n📊 Batch Processing Statistics:")
    print(f"   Total time: {total_time:.2f} seconds")
    print(f"   Posts processed: {processed_posts}")
    print(f"   Average time per post: {avg_time:.2f} seconds")
    print(f"   Database overhead: {(total_time - total_post_time):.2f} seconds")


score_posts_from("subreddit", "ShitpostBR")
