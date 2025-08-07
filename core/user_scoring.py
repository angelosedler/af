def calculate_user_score(scored_posts: list[dict]) -> tuple[float, str]:
    """
    Calculates the radical_score of a user based on their posts.
    Gives stronger weight to the most extreme post while still considering overall behavior.

    Returns:
        final_score: float (0 to 100)
        explanation: str
    """
    scores = [p["radical_score"] for p in scored_posts if "radical_score" in p]

    if not scores:
        return 0.0, "No valid scored posts found."

    avg = sum(scores) / len(scores)
    max_score = max(scores)

    final_score = round((0.4 * avg) + (0.6 * max_score), 2)

    explanation = (
        f"User's average post score is {round(avg, 2)} "
        f"and their highest score is {max_score}. "
        f"The radical_score prioritizes the most extreme post, resulting in {final_score}."
    )

    return final_score, explanation
