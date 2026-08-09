#!/usr/bin/env python3

import sys
import json
import subprocess
from pathlib import Path


# =========================
# הגדרות
# =========================

REPORT_SCRIPT = "run_report.py"
OUTPUT_FILE = "report_output.json"
DETECTOR_FILE = "output_detector.py"

MAX_RETRIES = 3


# =========================
# בדיקת קיום קבצים
# =========================

def check_required_files():

    if not Path(REPORT_SCRIPT).exists():

        print(f"[ERROR] לא נמצא קובץ הדוח: {REPORT_SCRIPT}")
        return False

    return True


# =========================
# יצירת מנגנון זיהוי
# =========================

def ensure_detector():

    detector = Path(DETECTOR_FILE)

    if detector.exists():

        print("[OK] מנגנון זיהוי כבר קיים")
        return

    print("[INFO] מנגנון זיהוי לא קיים")
    print("[INFO] יוצר מנגנון זיהוי חדש...")

    detector.write_text(
        '''#!/usr/bin/env python3

import json
from pathlib import Path


def detect_output(output_file):

    path = Path(output_file)

    if not path.exists():
        return False

    if path.stat().st_size == 0:
        return False

    try:

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return bool(data)

    except Exception:

        return False
''',
        encoding="utf-8"
    )

    print("[OK] מנגנון זיהוי נוצר")


# =========================
# בדיקת פלט
# =========================

def validate_output():

    output = Path(OUTPUT_FILE)

    if not output.exists():

        return False, "קובץ הפלט לא נוצר"

    if output.stat().st_size == 0:

        return False, "קובץ הפלט ריק"

    try:

        with open(output, "r", encoding="utf-8") as f:

            data = json.load(f)

        if not data:

            return False, "הפלט ריק"

        return True, "הפלט תקין"

    except json.JSONDecodeError:

        return False, "הפלט אינו JSON תקין"

    except Exception as e:

        return False, f"שגיאה בקריאת הפלט: {e}"


# =========================
# הרצת הדוח
# =========================

def run_report():

    print()
    print("[INFO] מריץ את הדוח...")
    print()

    result = subprocess.run(
        [sys.executable, REPORT_SCRIPT],
        capture_output=True,
        text=True
    )

    if result.stdout:

        print("----- OUTPUT -----")
        print(result.stdout)

    if result.stderr:

        print("----- ERRORS -----")
        print(result.stderr)

    if result.returncode != 0:

        print("[ERROR] הדוח הסתיים עם שגיאה")

        return False

    print("[OK] הדוח הסתיים")

    return True


# =========================
# תיקון אוטומטי
# =========================

def repair():

    print()
    print("[REPAIR] מתחיל תיקון...")

    output = Path(OUTPUT_FILE)

    if output.exists():

        try:

            output.unlink()

            print("[REPAIR] פלט פגום נמחק")

        except Exception as e:

            print(f"[WARNING] לא ניתן למחוק את הפלט: {e}")

    ensure_detector()

    print("[REPAIR] התיקון הסתיים")


# =========================
# תהליך ראשי
# =========================

def main():

    print("=" * 60)
    print("מערכת אוטומטית לבדיקת פלט והרצה מחדש")
    print("=" * 60)

    if not check_required_files():

        return 1

    ensure_detector()

    for attempt in range(1, MAX_RETRIES + 1):

        print()
        print("=" * 60)
        print(f"ניסיון {attempt} מתוך {MAX_RETRIES}")
        print("=" * 60)

        run_report()

        valid, message = validate_output()

        print()
        print(f"[CHECK] {message}")

        if valid:

            print()
            print("=" * 60)
            print("[SUCCESS] הפלט התקבל בהצלחה")
            print("[SUCCESS] הדוח הסתיים בהצלחה")
            print("=" * 60)

            return 0

        print()
        print("[WARNING] הפלט לא תקין או לא התקבל")

        if attempt < MAX_RETRIES:

            repair()

            print("[INFO] מריץ את הדוח מחדש...")

        else:

            print()
            print("=" * 60)
            print("[ERROR] כל ניסיונות התיקון נכשלו")
            print("=" * 60)

            return 1


if __name__ == "__main__":

    sys.exit(main())

