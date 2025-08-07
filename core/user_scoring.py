def calculate_user_score(scored_posts: list[dict]) -> tuple[float, str]:
    """
    Calculates the radical_score of a user based on their posts.
    Penalizes users who have many high-risk posts (score >= 60).
    Returns: (final_score: float, explanation: str)
    """
    scores = [p["radical_score"] for p in scored_posts if "radical_score" in p]

    if not scores:
        return 0.0, "No valid scored posts found."

    avg = sum(scores) / len(scores)
    high_risk = len([s for s in scores if s >= 60])
    total = len(scores)

    multiplier = 1 + (high_risk / total)
    final_score = min(round(avg * multiplier, 2), 100)

    explanation = (
        f"Avg: {round(avg, 2)}, flagged posts: {high_risk}/{total} → "
        f"Adjusted score: {final_score}"
    )

    return final_score, explanation
