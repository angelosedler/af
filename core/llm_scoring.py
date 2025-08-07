from llama_cpp import Llama
import os

MODEL_PATH = "models/zephyr-7b-alpha.Q4_K_M.gguf"
os.environ["LLAMA_METAL"] = "1"

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,
    n_threads=6,
    n_batch=512,
    use_mlock=True,
    use_mmap=True,
    verbose=False
)

def score_post_with_llm(post_data):
    """
    Analyze the post using a hardcoded moderation prompt and return (score, explanation).
    """

    title = post_data.get("title", "").strip()
    text = post_data.get("selftext", "").strip()

    if not title and not text:
        return 0.0, "Post contains no text to analyze."

    prompt = f"""
You are a content moderation assistant trained to detect antisemitic content on Reddit.

Analyze the following Reddit post and assign a radicalization score between 0 and 100,
based on hate speech, stereotypes, Holocaust denial, or Nazi comparisons.

Title:
{title}

Text:
{text}

Respond in this format:
Score: <number>
Explanation: <short explanation>
"""

    output = llm(prompt, max_tokens=128, stop=["</s>"])
    text = output["choices"][0]["text"].strip()

    score = 0.0
    explanation = "Could not parse response."

    for line in text.splitlines():
        if line.lower().startswith("score:"):
            try:
                score = float(line.split(":")[1].strip())
            except:
                score = 0.0
        elif line.lower().startswith("explanation:"):
            explanation = line.split(":", 1)[1].strip()

    return score, explanation
