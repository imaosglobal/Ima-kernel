TEMPLATES = {
    10: "מושלם {issues}",
    9: "כמעט שם {issues}",
    8: "יש פה עבודה {issues}",
    7: "צריך ליטוש {issues}",
    6: "בעייתי {issues}",
    5: "אל תעלה ככה {issues}",
}

def build_answer(result):
    score = result['score']
    issues = " - " + ", ".join(result['issues']) if result['issues'] else " - אין בעיות"
    template = TEMPLATES.get(score, TEMPLATES[5])
    return template.format(issues=issues), result['recovery']
