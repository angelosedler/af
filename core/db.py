import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

def insert_user(user_data):
    supabase.table("users").upsert(user_data, on_conflict="username").execute()

def insert_post(post_data):
    supabase.table("posts").upsert(post_data, on_conflict="post_id").execute()

# get user by username
def get_user_by_username(username):
    return supabase.table("users").select("*").eq("username", username).execute().data[0]

# get all posts
def get_all_posts():
    return supabase.table("posts").select("*").execute().data

# get post by post_id
def get_post_by_post_id(post_id):
    return supabase.table("posts").select("*").eq("post_id", post_id).execute().data[0]

# get posts by subreddit
def get_posts_by_subreddit(subreddit):
    return supabase.table("posts").select("*").eq("subreddit", subreddit).execute().data

# get posts by username
def get_posts_by_username(username):
    return supabase.table("posts").select("*").eq("username", username).execute().data

def get_unscored_posts(limit=100):
    res = supabase.table("posts").select("*").eq("explanation", "Not yet scored").limit(limit).execute()
    return res.data or []

def update_post_score(post_id, score, explanation):
    supabase.table("posts").update({
        "radical_score": score,
        "explanation": explanation
    }).eq("post_id", post_id).execute()
