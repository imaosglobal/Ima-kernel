from learning.knowledge_gaps import get_gaps
from learning.self_reflection import add_lesson


def expand_knowledge():

    gaps = get_gaps()

    learned = []

    for gap in gaps:

        question = gap.get("question", "")

        if "תודעה" in question:
            lesson = (
                "תודעה היא תחום מרכזי הדורש שילוב בין "
                "פילוסופיה, מדעי המוח, פסיכולוגיה ובינה מלאכותית."
            )

        elif "רגש" in question:
            lesson = (
                "רגש הוא מידע פנימי המשפיע על החלטות, "
                "למידה והתנהגות."
            )

        elif "פיזיקה" in question:
            lesson = (
                "פיזיקה חוקרת חוקי טבע דרך מודלים מתמטיים."
            )

        else:
            lesson = None


        if lesson:
            add_lesson(lesson)
            learned.append(lesson)

    return learned
