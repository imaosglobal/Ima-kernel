from founder.executive_ai.memory.founder_timeline import build_timeline
from founder.executive_ai.memory.memory_consolidator import consolidate
from founder.executive_ai.memory.pattern_analyzer import analyze_patterns


def generate_insights():

    timeline = build_timeline()

    consolidated = consolidate(
        timeline
    )

    patterns = analyze_patterns(
        consolidated
    )

    recommendations=[]

    for item in patterns.get("insights", []):

        recommendations.append({
            "issue": item["pattern"],
            "priority": item["strength"],
            "next_question":
                "איזה ניסוי או פעולה יכולים לתת תשובה?"
        })

    return {
        "patterns": patterns,
        "decision_questions": recommendations
    }
