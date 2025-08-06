import pandas as pd
from db import supabase

def export_posts_to_csv():
    response = supabase.table("posts").select("*").limit(1000).execute()
    data = response.data
    df = pd.DataFrame(data)
    df.to_csv("reddit_posts.csv", index=False)
    print("✅ Exportado a reddit_posts.csv")
