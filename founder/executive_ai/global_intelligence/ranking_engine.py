def ranker(items=None):

    if items is None:
        return []

    ranked = []

    for item in items:
        score = 0

        if isinstance(item, dict):
            score += item.get("priority", 0)
            score += item.get("importance", 0)
            score += item.get("relevance", 0)

            ranked.append({
                **item,
                "rank_score": score
            })

    return sorted(
        ranked,
        key=lambda x: x.get("rank_score", 0),
        reverse=True
    )


def rank_opportunities(items=None):
    return ranker(items)
