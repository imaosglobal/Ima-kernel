#!/usr/bin/env python3

import json
import subprocess
import sys
import time
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DIAGNOSTICS_DIR = BASE_DIR / ".ima" / "diagnostics"

MAX_RETRIES = 3

REPORT_PATH = None


# ============================================================
# LOGGING
# ============================================================

def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


# ============================================================
# FIND DIAGNOSTIC ENGINE
# ============================================================

def find_diagnostic_engine():

    candidates = [
        BASE_DIR / "IMA_PRODUCT_DIAGNOSTIC_ENGINE.py",
        BASE_DIR / "product_diagnostic.py",
        BASE_DIR / ".ima" / "diagnostics" / "IMA_PRODUCT_DIAGNOSTIC_ENGINE.py",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    discovered = list(BASE_DIR.rglob("IMA_PRODUCT_DIAGNOSTIC_ENGINE.py"))

    if discovered:
        return discovered[0]

    discovered = list(BASE_DIR.rglob("product_diagnostic.py"))

    if discovered:
        return discovered[0]

    return None


# ============================================================
# FIND REPAIR ENGINE
# ============================================================

def find_repair_engine():

    candidates = [
        BASE_DIR / ".ima" / "agi_evolution" / "runtime" / "repair_engine.py",
        BASE_DIR / "repair_engine.py",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    discovered = list(BASE_DIR.rglob("repair_engine.py"))

    if discovered:
        return discovered[0]

    return None


# ============================================================
# JSON LOADER
# ============================================================

def load_report():

    global REPORT_PATH

    if REPORT_PATH is None:
        return None

    if not REPORT_PATH.exists():
        return None

    try:
        with REPORT_PATH.open("r", encoding="utf-8") as file:
            return json.load(file)

    except Exception as exc:
        log(f"[ERROR] Cannot load report: {exc}")
        return None


# ============================================================
# FIND VALUES RECURSIVELY
# ============================================================

def find_values(obj, key):

    found = []

    if isinstance(obj, dict):

        if key in obj:
            found.append(obj[key])

        for value in obj.values():
            found.extend(find_values(value, key))

    elif isinstance(obj, list):

        for item in obj:
            found.extend(find_values(item, key))

    return found


# ============================================================
# FIND FAILED CHECKS
# ============================================================

def find_failed_checks(obj):

    failures = []

    if isinstance(obj, dict):

        name = obj.get("name")
        ok = obj.get("ok")

        if name is not None and ok is False:
            failures.append(obj)

        for value in obj.values():
            failures.extend(find_failed_checks(value))

    elif isinstance(obj, list):

        for item in obj:
            failures.extend(find_failed_checks(item))

    return failures


# ============================================================
# FIND PARTIAL STAGES
# ============================================================

def find_partial_stages(obj):

    partials = []

    if isinstance(obj, dict):

        status = obj.get("status")

        if status == "PARTIAL":
            partials.append(obj)

        for value in obj.values():
            partials.extend(find_partial_stages(value))

    elif isinstance(obj, list):

        for item in obj:
            partials.extend(find_partial_stages(item))

    return partials


# ============================================================
# VALIDATE REPORT
# ============================================================

def validate_report(report):
    problems = []

    if not isinstance(report, dict):
        return ["report is not a JSON object"]

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    summaries = find_values(report, "summary")

    structured_summaries = []

    for value in summaries:
        if isinstance(value, dict):
            structured_summaries.append(value)

    if structured_summaries:

        summary = structured_summaries[-1]

        def safe_int(value):
            try:
                return int(value or 0)
            except (TypeError, ValueError):
                return 0

        failed = safe_int(summary.get("FAILED", 0))
        missing = safe_int(summary.get("MISSING", 0))
        partial = safe_int(summary.get("PARTIAL", 0))

        if failed > 0:
            problems.append(f"FAILED={failed}")

        if missing > 0:
            problems.append(f"MISSING={missing}")

        if partial > 0 and failed == 0 and missing == 0:
            log(
                f"[INFO] PARTIAL={partial} detected "
                "but treated as NON-FATAL."
            )

    else:
        log(
            "[WARN] No structured summary dictionary found."
        )

    # --------------------------------------------------------
    # EXPLICIT VALIDATION FLAGS
    # --------------------------------------------------------

    validation_values = find_values(
        report,
        "validation_ok"
    )

    for value in validation_values:

        if value is False:
            problems.append(
                "validation_ok=false"
            )

    # --------------------------------------------------------
    # FAILED CHECKS
    # --------------------------------------------------------

    failed_checks = find_failed_checks(report)

    for check in failed_checks:

        problems.append(
            "failed check: "
            + str(
                check.get(
                    "name",
                    "unknown"
                )
            )
        )

    # --------------------------------------------------------
    # REQUIRED VALIDATION MARKERS
    # --------------------------------------------------------

    report_text = json.dumps(
        report,
        ensure_ascii=False
    )

    required_markers = [
        "VALIDATION_OK",
        "HASH VERIFIED",
        "CANONICAL REGISTRY VERIFIED",
    ]

    for marker in required_markers:

        if marker not in report_text:

            problems.append(
                f"{marker} marker missing"
            )

    return problems


def find_latest_report():

    if not DIAGNOSTICS_DIR.exists():

        return None


    reports = list(
        DIAGNOSTICS_DIR.glob(
            "product_diagnostic_*.json"
        )
    )


    if not reports:

        return None


    return max(
        reports,
        key=lambda path: path.stat().st_mtime
    )


# ============================================================
# RUN REPAIR
# ============================================================

def run_repair():

    repair_engine = find_repair_engine()


    if repair_engine is None:

        log(
            "[INFO] No repair engine found."
        )

        log(
            "[INFO] No automatic repair required."
        )

        return True


    log(
        f"[REPAIR] Running: {repair_engine}"
    )


    result = subprocess.run(

        [
            sys.executable,
            str(repair_engine)
        ],

        cwd=str(BASE_DIR),

        text=True,

        capture_output=True

    )


    if result.stdout:

        print(
            result.stdout
        )


    if result.stderr:

        print(
            result.stderr,
            file=sys.stderr
        )


    if result.returncode != 0:

        log(
            "[ERROR] Repair engine failed."
        )

        log(
            f"[ERROR] Exit code: {result.returncode}"
        )

        return False


    log(
        "[OK] Repair completed successfully."
    )


    return True


# ============================================================
# RUN DIAGNOSTIC
# ============================================================

def run_diagnostic():

    diagnostic_engine = find_diagnostic_engine()


    if diagnostic_engine is None:

        log(
            "[ERROR] Diagnostic engine not found."
        )

        return False


    log(
        f"[DIAGNOSTIC] Running detected script: "
        f"{diagnostic_engine}"
    )


    result = subprocess.run(

        [
            sys.executable,
            str(diagnostic_engine)
        ],

        cwd=str(BASE_DIR),

        text=True,

        capture_output=True

    )


    if result.stdout:

        print(
            result.stdout
        )


    if result.stderr:

        print(
            result.stderr,
            file=sys.stderr
        )


    # --------------------------------------------------------
    # IMPORTANT:
    #
    # The diagnostic engine returns 1 for PARTIAL.
    #
    # We DO NOT treat this alone as a real failure.
    # The actual JSON report decides.
    # --------------------------------------------------------

    if result.returncode not in (0, 1):

        log(
            "[ERROR] Diagnostic crashed."
        )

        log(
            f"[ERROR] Exit code: {result.returncode}"
        )

        return False


    if result.returncode == 1:

        log(
            "[INFO] Diagnostic returned 1."
        )

        log(
            "[INFO] This may represent PARTIAL status."
        )

        log(
            "[INFO] JSON report will be used for final validation."
        )


    return True


# ============================================================
# MAIN
# ============================================================

def main():

    global REPORT_PATH


    log(
        "============================================================"
    )

    log(
        "IMA DIAGNOSTIC VALIDATOR / AUTO REPAIR"
    )

    log(
        "============================================================"
    )


    REPORT_PATH = find_latest_report()


    if REPORT_PATH:

        log(
            f"[INFO] Initial report: {REPORT_PATH}"
        )


    for attempt in range(
        1,
        MAX_RETRIES + 1
    ):


        log("")

        log(
            f"================ ATTEMPT "
            f"{attempt}/{MAX_RETRIES} ================"
        )


        # ----------------------------------------------------
        # LOAD CURRENT REPORT
        # ----------------------------------------------------

        REPORT_PATH = find_latest_report()

        report = load_report()


        if report is not None:

            problems = validate_report(
                report
            )


            if not problems:

                log(
                    "[OK] REPORT VALIDATION PASSED"
                )

                log(
                    "[OK] FAILED=0"
                )

                log(
                    "[OK] MISSING=0"
                )

                log(
                    "[OK] PARTIAL STATUS ACCEPTED"
                )

                log(
                    "[OK] SYSTEM IS READY"
                )

                return 0


            log(
                "[WARN] REPORT HAS REAL PROBLEMS:"
            )


            for problem in problems:

                log(
                    f"       - {problem}"
                )


        else:

            log(
                "[WARN] No valid report found."
            )


        # ----------------------------------------------------
        # REPAIR
        # ----------------------------------------------------

        log(
            "[ACTION] Starting repair procedure..."
        )


        repaired = run_repair()


        if not repaired:

            log(
                "[ERROR] Repair failed."
            )


        # ----------------------------------------------------
        # RERUN DIAGNOSTIC
        # ----------------------------------------------------

        log(
            "[ACTION] Re-running diagnostic..."
        )


        diagnostic_ok = run_diagnostic()


        if not diagnostic_ok:

            log(
                "[ERROR] Diagnostic execution failed."
            )

            continue


        # ----------------------------------------------------
        # LOAD NEW REPORT
        # ----------------------------------------------------

        time.sleep(1)


        REPORT_PATH = find_latest_report()


        if REPORT_PATH:

            log(
                f"[INFO] Newest report detected:"
            )

            log(
                f"       {REPORT_PATH}"
            )


            report = load_report()


            if report is not None:

                problems = validate_report(
                    report
                )


                if not problems:

                    log(
                        "[OK] REPORT VALIDATION PASSED"
                    )

                    log(
                        "[OK] PARTIAL STATUS ACCEPTED"
                    )

                    log(
                        "[OK] SYSTEM IS READY"
                    )

                    return 0


    # ========================================================
    # FINAL VALIDATION
    # ========================================================

    log("")

    log(
        "============================================================"
    )

    log(
        "FINAL VALIDATION"
    )

    log(
        "============================================================"
    )


    REPORT_PATH = find_latest_report()

    report = load_report()


    if report is None:

        log(
            "[FAILED] No valid report available."
        )

        return 1


    problems = validate_report(
        report
    )


    if problems:

        log(
            "[FAILED] REPORT STILL HAS REAL PROBLEMS:"
        )


        for problem in problems:

            log(
                f"         - {problem}"
            )


        return 1


    log(
        "[OK] FINAL VALIDATION PASSED"
    )

    log(
        "[OK] REPORT IS ACCEPTED"
    )

    log(
        "[OK] PARTIAL STATUS IS NON-FATAL"
    )

    return 0


if __name__ == "__main__":

    sys.exit(
        main()
    )

