from llama_cpp import Llama
import os
import re

MODEL_PATH = "models/zephyr-7b-alpha.Q4_K_M.gguf"
os.environ["LLAMA_METAL"] = "1"

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=6,
    n_batch=512,
    use_mlock=True,
    use_mmap=True,
    verbose=False
)

def score_post_with_llm(post_data):
    title = post_data.get("title", "").strip()
    text = post_data.get("selftext", "").strip()

    if not title and not text:
        return 0.0, "Post contains no text to analyze."

    prompt = f"""
You are a content moderation assistant trained to detect antisemitic content on Reddit.

Analyze the following Reddit post and assign a radicalization score between 0 and 100 based on antisemitic content.

If there is no clear evidence of antisemitic content, return a score of 0 and an explanation saying "Not antisemitic".

Antisemitic content includes:
- Hate speech or slurs against Jewish people
- Holocaust denial or distortion
- Comparisons of Jews or Israel to Nazis
- Conspiracy theories that blame Jews for controlling media, banks, or governments
- Calls for violence or dehumanization of Jewish people
- Terms like "Zionist", "JQ", "Zionist conspiracy", "ZOG", etc.


Now analyze the following Reddit post.

Title:
{title}

Text:
{text}

Respond in this format:
Score: <number>
Explanation: <short explanation>
"""

    output = llm(prompt, max_tokens=128, stop=["</s>"])
    raw_text = output["choices"][0]["text"].strip()

    # Robust parsing
    score = 0.0
    explanation = "Could not parse response."

    score_match = re.search(r"score[:=\-]?\s*([0-9]{1,3})", raw_text, re.IGNORECASE)
    if score_match:
        try:
            score = float(score_match.group(1))
        except:
            score = 0.0

    explanation_match = re.search(r"explanation[:=\-]?\s*(.+)", raw_text, re.IGNORECASE)
    if explanation_match:
        explanation = explanation_match.group(1).strip()

    return score, explanation