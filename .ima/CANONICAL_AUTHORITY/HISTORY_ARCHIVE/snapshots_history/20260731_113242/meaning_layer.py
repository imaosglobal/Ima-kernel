def explain_relation(text):

    explanations = {
        "emotion->music":
            "מוזיקה היא דרך לבטא ולעבד רגשות דרך יצירה.",
        "identity->psychology":
            "זהות קשורה להבנה פסיכולוגית של האדם את עצמו.",
        "learning->decision":
            "למידה משפיעה על קבלת החלטות והתאמה למצבים חדשים.",
        "inventory->business":
            "ניהול משאבים ומלאי הוא חלק ממערכת עסקית."
    }

    for key,value in explanations.items():
        if key in text:
            return value

    return None


def humanize(results):
    output=[]

    for r in results:
        explanation=explain_relation(r)
        if explanation:
            output.append(explanation)

    return output
