
from learning.learning_memory import get_patterns


def suggest_improvements():

    patterns = get_patterns()

    suggestions=[]

    for item in patterns:
        name=item.get("pattern","")
        count=item.get("count",0)

        suggestions.append({
            "pattern": name,
            "strength": count,
            "suggestion": f"העמקת יכולת IMA בתחום {name}"
        })

    if not suggestions:
        suggestions.append({
            "pattern":"general",
            "strength":0,
            "suggestion":"לאסוף יותר אירועי למידה לפני הסקת מסקנות"
        })

    return {
        "suggestions": suggestions,
        "count": len(suggestions)
    }
