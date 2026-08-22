def interpret(diff):
    issues = []
    score = 10

    if "TODO" in diff:
        issues.append("יש TODO פתוחים")
        score -= 2
        issues.append("דיבוג עם print נשכח בקוד")
        score -= 1
    if not diff.strip():
        issues.append("אין שינויים ב-diff")
        score = 5

    if score >= 9:
        recovery = ["תסיר את ה-printים"]
    elif score >= 7:
        recovery = ["תתקן את הבעיות למעלה", "תריץ pytest"]
    else:
        recovery = ["1. תעבור על כל ה-issues", "2. אל תעשה merge ככה"]

    return {"score": score, "issues": issues, "recovery": recovery}
