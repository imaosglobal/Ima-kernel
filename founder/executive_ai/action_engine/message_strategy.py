def generate_message(target, entity_type):

    if entity_type=="government":
        return (
            f"שלום {target}, "
            "IMA מציעה שיתוף פעולה בתחום AI "
            "לשיפור שירותים ציבוריים והגדלת השפעה לאזרחים."
        )

    if entity_type=="company":
        return (
            f"שלום {target}, "
            "IMA מזהה אפשרות לשיתוף פעולה אסטרטגי "
            "ליצירת יתרון באמצעות AI אישי ולמידה מתמשכת."
        )

    if entity_type=="nonprofit":
        return (
            f"שלום {target}, "
            "IMA יכולה לסייע בהגדלת השפעה חברתית "
            "באמצעות מערכות AI מותאמות."
        )

    return (
        f"שלום {target}, "
        "IMA מזהה אפשרות לשיתוף פעולה."
    )
