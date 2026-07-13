from pathlib import Path
import json

QUESTIONS = {
    "vision": [
        "האם הפעולה הזו מקרבת את IMA לחזון?",
        "איזו בעיה אנושית אמיתית אנחנו פותרים?"
    ],
    "product": [
        "מי המשתמש הראשון שמקבל ערך?",
        "מה ההוכחה הפשוטה ביותר לערך?"
    ],
    "technology": [
        "האם השינוי מוסיף ערך או רק מורכבות?",
        "מה יכול להישבר?"
    ],
    "business": [
        "מי הלקוח הראשון?",
        "למה שישלם?"
    ],
    "founder": [
        "מה ההחלטה החשובה ביותר כרגע?",
        "מה לא צריך לעשות עכשיו?"
    ]
}

def generate_questions():
    return QUESTIONS

if __name__ == "__main__":
    print(json.dumps(QUESTIONS, ensure_ascii=False, indent=2))
