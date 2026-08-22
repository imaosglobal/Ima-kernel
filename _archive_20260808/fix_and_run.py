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

        return False

    return True


# =========================
# יצירת מנגנון זיהוי
# =========================

def ensure_detector():

    detector = Path(DETECTOR_FILE)

    if detector.exists():

        return


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


    result = subprocess.run(
        [sys.executable, REPORT_SCRIPT],
        capture_output=True,
        text=True
    )

    if result.stdout:


    if result.stderr:


    if result.returncode != 0:


        return False


    return True


# =========================
# תיקון אוטומטי
# =========================

def repair():


    output = Path(OUTPUT_FILE)

    if output.exists():

        try:

            output.unlink()


        except Exception as e:


    ensure_detector()



# =========================
# תהליך ראשי
# =========================

def main():


    if not check_required_files():

        return 1

    ensure_detector()

    for attempt in range(1, MAX_RETRIES + 1):


        run_report()

        valid, message = validate_output()


        if valid:


            return 0


        if attempt < MAX_RETRIES:

            repair()


        else:


            return 1


if __name__ == "__main__":

    sys.exit(main())

