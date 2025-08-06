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

