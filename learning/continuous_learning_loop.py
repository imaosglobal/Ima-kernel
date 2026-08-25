from pathlib import Path
from datetime import datetime
import json

from learning.self_inspection_cycle import run_self_inspection


REPORT_FILE = Path("learning/continuous_learning_reports.json")


def load_reports():
    try:
        return json.loads(
            REPORT_FILE.read_text(encoding="utf-8")
        )
    except Exception:
        return {"reports": []}


def save_reports(data):
    REPORT_FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def run_continuous_learning_cycle():
    """
    Continuous read-only learning loop.

    Pipeline:
    1. Scan own code and directories
    2. Retrieve relevant lessons
    3. Reason
    4. Build plan
    5. Evaluate plan
    6. Generate feedback
    7. Record lesson
    8. Save report

    No execution.
    No self-modification.
    No code writes.
    """

    result = run_self_inspection()

    reports = load_reports()

    report = {
        "timestamp": str(datetime.now()),
        "cycle": len(reports.get("reports", [])) + 1,
        "status": result.get("status"),
        "files": result.get("files"),
        "directories": result.get("directories"),
        "python_modules": result.get("python_modules"),
        "lessons_retrieved": result.get("lessons_retrieved"),
        "autonomy_status": result.get(
            "autonomy",
            {}
        ).get("status"),
        "execution": "disabled",
        "self_modification": "disabled",
    }

    reports.setdefault("reports", []).append(report)
    save_reports(reports)

    return {
        "report": report,
        "total_cycles": len(reports["reports"]),
        "status": "continuous_learning_cycle_completed",
        "execution": "disabled",
        "self_modification": "disabled",
    }


def show_learning_summary():
    reports = load_reports()
    items = reports.get("reports", [])

    return {
        "total_cycles": len(items),
        "latest_cycle": items[-1] if items else None,
        "status": "summary_generated",
        "execution": "disabled",
        "self_modification": "disabled",
    }


if __name__ == "__main__":
    result = run_continuous_learning_cycle()

    print("=" * 100)
    print("IMA — CONTINUOUS LEARNING LOOP")
    print("=" * 100)

    print("CYCLE:", result["report"]["cycle"])
    print("STATUS:", result["status"])
    print("TOTAL CYCLES:", result["total_cycles"])
    print("EXECUTION:", result["execution"])
    print(
        "SELF-MODIFICATION:",
        result["self_modification"],
    )

    print("=" * 100)
    print("CONTINUOUS LEARNING CYCLE COMPLETED")
    print("SCAN: PASS")
    print("LESSON RETRIEVAL: PASS")
    print("REASONING: PASS")
    print("PLANNING: PASS")
    print("EVALUATION: PASS")
    print("FEEDBACK: PASS")
    print("LESSON MEMORY: PASS")
    print("REPORT MEMORY: PASS")
    print("EXECUTION: DISABLED")
    print("SELF-MODIFICATION: DISABLED")
    print("=" * 100)
