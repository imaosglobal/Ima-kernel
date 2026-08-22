#!/usr/bin/env python3
import subprocess
import sys
import os
import re

class IMAReviewer:
    def __init__(self):
        self.score = 8
        self.failures = []
        self.fixes = []

    def get_diff(self):
        try:
            result = subprocess.run(['git', 'diff', 'HEAD'], capture_output=True, text=True)
            return result.stdout
        except:
            return ""

    def check_prints(self, diff):
        if 'print(' in diff:
            self.score -= 1
            self.failures.append("[ ] אין print או קוד מיותר")
            self.fixes.append("הסר את כל ה-print(). השתמש ב-logger במקום.")
        else:
            self.failures.append("[x] אין print או קוד מיותר")

    def check_except(self, diff):
        if re.search(r'except:', diff) and not re.search(r'except Exception', diff):
            self.score -= 2
            self.failures.append("[ ] שימוש ב-except ריק")
            self.fixes.append("תחליף `except:` ב-`except Exception as e:` ותעשה log ל-error")
        else:
            self.failures.append("[x] טיפול בשגיאות תקין")

    def check_tests(self, diff):
        if 'test_' not in diff and 'Test' not in diff:
            self.score -= 1
            self.failures.append("[ ] הוספתי טסטים לשינוי שלי")
            self.fixes.append("תוסיף קובץ test_*.py שמכסה את השינוי")
        else:
            self.failures.append("[x] הוספתי טסטים לשינוי שלי")

    def check_commit_msg(self):
        result = subprocess.run(['git', 'log', '-1', '--pretty=%B'], capture_output=True, text=True)
        msg = result.stdout
        if not re.match(r'(feat|fix|docs|chore|refactor):', msg):
            self.score -= 1
            self.failures.append("[ ] הכותרת היא בפורמט: feat: / fix: / docs:")
            self.fixes.append("שנה את ה-commit ל: `feat: הוספת IMA Toolkit`")
        else:
            self.failures.append("[x] הכותרת היא בפורמט: feat: / fix: / docs:")

    def run(self):
        print("=== IMA PR REVIEWER - רמת מחמירות: 10/10 ===\n")
        diff = self.get_diff()

        self.check_prints(diff)
        self.check_except(diff)
        self.check_tests(diff)
        self.check_commit_msg(diff)

        print("[ ] יש לי issue פתוח ומקושר: Fixes #123")
        print("[ ] קראתי את CONTRIBUTING.md של הרפו")
        print("[ ] הרצתי linter: black, ruff, eslint")
        print("[ ] התיאור מסביר את ה-Why ולא רק את ה-What")
        print("[ ] בדקתי שלא שברתי שום דבר קיים")
        for f in self.failures:
            print(f)

        print(f"\n[ציון IMA]: {self.score}/8")

        if self.score < 8:
            print("\n[IMA]: עצור. לא מאשרים PR כזה.")
            print("[תוכנית שיקום ל-8/8]:")
            for i, fix in enumerate(self.fixes, 1):
                print(f"{i}. {fix}")
        else:
            print("\n[IMA]: PR מוכן לשליחה. זה ברמה של core maintainer.")

if __name__ == "__main__":
    IMAReviewer().run()
