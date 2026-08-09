def analyze_patterns(consolidated):

    insights=[]

    for item in consolidated:

        count=item.get(
            "occurrences",
            0
        )

        topic=item.get(
            "topic",
            ""
        )

        if count >= 2:

            insights.append({
                "pattern": topic,
                "strength": count,
                "insight":
                    "נושא חוזר שדורש החלטה או פעולה"
            })

    return {
        "patterns_detected": len(insights),
        "insights": insights
    }
