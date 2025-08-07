import os
os.environ["LLAMA_METAL"] = "1"

from llama_cpp import Llama

MODEL_PATH = "models/zephyr-7b-alpha.Q4_K_M.gguf"

# Load model once when this file is imported
# llm = Llama(
#     model_path=MODEL_PATH,
#     n_ctx=2048,
#     n_threads=8,  # ajustá según tu CPU
#     verbose=False
# )

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
    Uses a local Zephyr LLM to analyze a post and return (score, explanation)
    """
    prompt = f"""
You are a content moderation AI specialized in detecting antisemitic content.

Analyze the following Reddit post and assign a radicalization score between 0 and 100,
based on hate speech, threats, antisemitic stereotypes, Holocaust denial, or Nazi comparisons.

Post Title:
{post_data['title']}

Post Text:
{post_data['selftext']}

Respond in this format:
Score: <number>
Explanation: <short explanation>
"""

    output = llm(prompt, max_tokens=128, stop=["</s>"])
    text = output["choices"][0]["text"].strip()

    score = 0
    explanation = "Could not parse response"

    for line in text.splitlines():
        if line.lower().startswith("score:"):
            try:
                score = float(line.split(":")[1].strip())
            except:
                pass
        elif line.lower().startswith("explanation:"):
            explanation = line.split(":", 1)[1].strip()

    return score, explanation
