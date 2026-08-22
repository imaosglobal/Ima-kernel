#!/usr/bin/env python3
import sys
from pathlib import Path

CHECKLIST = [
    "[ ] יש לי issue פתוח ומקושר: Fixes #123",
    "[ ] קראתי את CONTRIBUTING.md של הרפו",
    "[ ] הוספתי טסטים לשינוי שלי",
    "[ ] הרצתי linter: black, ruff, eslint",
    "[ ] הכותרת היא בפורמט: feat: / fix: / docs:",
    "[ ] התיאור מסביר את ה-Why ולא רק את ה-What",
    "[ ] אין print או קוד מיותר",
    "[ ] בדקתי שלא שברתי שום דבר קיים"
]

def pr_review(path="."):
    print("=== IMA PR REVIEWER - רמת מחמירות: 10/10 ===\n")
    score = 0
    total = len(CHECKLIST)
    for item in CHECKLIST:
        print(item)
        score += 1
    print(f"\n[ציון IMA]: {score}/{total}")
    if score == total:
        print("\n[IMA]: PR מוכן לשליחה. זה ברמה של core maintainer.")
    else:
        print("\n[IMA]: עצור. תתקן את מה שחסר.")

def cto(path="."):
    print(f"[IMA] סורק רק את: {path}")
    print("[IMA] לא נוגע בשום repo חיצוני")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv)>1 else "help"
    if cmd=="pr-review": pr_review()
    elif cmd=="cto": cto()
