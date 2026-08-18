def ranker(items=None):
    """
    Canonical ranking interface.

    Every ranked item receives the same public score field:
        score

    rank_score is retained as an internal/backward-compatible alias.
    """

    if items is None:
        return []

    ranked = []

    for item in items:
        if not isinstance(item, dict):
            continue

        score = (
            item.get("priority", 0)
            + item.get("importance", 0)
            + item.get("relevance", 0)
        )

        # Preserve an explicitly supplied score when no component
        # fields were supplied.
        if score == 0 and "score" in item:
            score = item.get("score", 0)

        try:
            score = float(score)
        except (TypeError, ValueError):
            score = 0

        normalized = {
            **item,
            "score": score,
            "rank_score": score,
        }

        ranked.append(normalized)

    return sorted(
        ranked,
        key=lambda x: x.get("score", 0),
        reverse=True,
    )


def rank_opportunities(items=None):
    return ranker(items)
