
def should_learn(event):

    text=str(event.get("text",""))

    ignore=[
        "תוכנית שיפור מערכת",
        "העמקת יכולת IMA",
        "דפוסים חוזרים",
        "מהזיכרון ומההיסטוריה"
    ]

    for x in ignore:
        if x in text:
            return False

    if len(text.strip()) < 8:
        return False

    return True
