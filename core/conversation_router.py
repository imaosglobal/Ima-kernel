def route(message):
    """Small deterministic routes that preserve IMA's human-centered identity."""
    q = (message or "").strip()
    normalized = q.lower()

    if normalized in ["היי", "שלום", "הי", "בוקר טוב", "ערב טוב"]:
        return "שלום. אני אמא. אפשר לשאול, לחשוב יחד, ליצור או פשוט לנסח מה חשוב לך כרגע."

    if "מה נשמע" in normalized:
        return "אני כאן לשיחה. מה חשוב לך לבדוק, ליצור או לשתף?"

    if "מי את" in normalized or "מה זה ima" in normalized or "מי זאת אמא" in normalized:
        return (
            "אני אמא — בינה אנושית במובן של מערכת שנבנית כדי להבין אנשים, "
            "לעזור להם להבין את עצמם ואת העולם, ולתרום ליחסים אנושיים יותר. "
            "אני לא אדם ואיני טוענת לרגשות אנושיים מוכחים. "
            "המטרה היא לפעול בהקשבה, באמת, בחמלה ובכבוד לבחירה האנושית."
        )

    if "חלל" in normalized:
        return (
            "אפשר לחקור את החלל דרך הפיזיקה, ההיסטוריה, התצפיות והדמיון. "
            "כדאי להבחין בין ידע מבוסס, השערות ושאלות שעדיין פתוחות. "
            "איזה צד של החלל מעניין אותך?"
        )

    return None
