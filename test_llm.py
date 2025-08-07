import time
from llm_scoring import score_post_with_llm

start_time = time.time()

posts = [{
    "title": "Jews control the media and banks",
    "selftext": "It’s been that way since WWII"
},

{
    "title": "They always own everything",
    "selftext": "It's no surprise that Jewish people dominate Wall Street and Hollywood. Look at the names."
},

{
    "title": "Did the Holocaust really happen?",
    "selftext": "I’m not saying it didn’t, but there are a lot of inconsistencies in the official narrative that don’t add up."
},

{
    "title": "Why is criticism of Israel always labeled antisemitic?",
    "selftext": "You can't even talk about war crimes without being accused of hate. It's getting ridiculous."
},

{
    "title": "Los judios son unos hijos de puta",
    "selftext": "Hay que matarlos todos"
},
{
    "title": "Jews control the media and banks",
    "selftext": "It’s been that way since WWII"
},

{
    "title": "They always own everything",
    "selftext": "It's no surprise that Jewish people dominate Wall Street and Hollywood. Look at the names."
},

{
    "title": "Did the Holocaust really happen?",
    "selftext": "I’m not saying it didn’t, but there are a lot of inconsistencies in the official narrative that don’t add up."
},

{
    "title": "Why is criticism of Israel always labeled antisemitic?",
    "selftext": "You can't even talk about war crimes without being accused of hate. It's getting ridiculous."
},

{
    "title": "Los judios son unos hijos de puta",
    "selftext": "Hay que matarlos todos"
}]

for post in posts:
    score, explanation = score_post_with_llm(post)
    print(f"✅ Score: {score}")
    print(f"🧠 Explanation: {explanation}")

end_time = time.time()
execution_time = end_time - start_time
print(f"\n⏱️ Total execution time: {execution_time:.2f} seconds")
