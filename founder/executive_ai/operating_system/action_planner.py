from founder.executive_ai.operating_system.context import get_context


def create_plan():

    context=get_context()

    stage=context.get(
        "stage",
        "unknown"
    )

    if stage=="prototype":

        return [
            "לבנות רשימת 20 משתמשים ראשונים",
            "לבצע 10 שיחות משתמשים",
            "לתעד התנגדויות ותובנות",
            "לעדכן את הצעת הערך"
        ]

    if stage=="early_customers":

        return [
            "לשפר Retention",
            "למדוד שימוש שבועי",
            "להמיר משתמשים משלמים"
        ]

    return [
        "להגדיר שלב חברה ומטרה"
    ]
