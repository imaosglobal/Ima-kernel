from pathlib import Path
import subprocess
import json
import re
import sys
import time
import traceback

ROOT = Path.cwd()
MEDA = ROOT / "external/MEDA"
MAIN = MEDA / "skills/meda/scripts/main.py"

SESSION = MEDA / "sessions/ima_universe_intelligence"
SETUP = SESSION / "setup.yaml"
PROBLEM = SESSION / "problem.json"

SESSION.mkdir(parents=True, exist_ok=True)

REPORT = SESSION / "adaptive_diagnostic_report.json"
DIRECT = SESSION / "adaptive_direct.json"
RETRY = SESSION / "adaptive_retry.json"

FAST_TIMEOUT = 30
RETRY_TIMEOUT = 90
IMPORT_TIMEOUT = 10
FUNCTION_TIMEOUT = 15

results = {
    "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "root": str(ROOT),
    "session": str(SESSION),
    "steps": [],
    "decisions": [],
    "final_status": None,
}


def save():
    results["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    REPORT.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def section(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def record(name, **data):
    item = {
        "name": name,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        **data,
    }
    results["steps"].append(item)
    save()
    return item


def execute(cmd, timeout=30, cwd=ROOT, env=None):
    print("\n$ " + " ".join(map(str, cmd)), flush=True)

    started = time.time()

    try:
        p = subprocess.run(
            [str(x) for x in cmd],
            cwd=str(cwd),
            text=True,
            capture_output=True,
            timeout=timeout,
            env=env,
        )

        result = {
            "returncode": p.returncode,
            "stdout": p.stdout[-30000:],
            "stderr": p.stderr[-30000:],
            "timeout": False,
            "duration": round(time.time() - started, 3),
        }

    except subprocess.TimeoutExpired as e:
        result = {
            "returncode": None,
            "stdout": (
                e.stdout[-30000:]
                if isinstance(e.stdout, str)
                else ""
            ),
            "stderr": (
                e.stderr[-30000:]
                if isinstance(e.stderr, str)
                else ""
            ),
            "timeout": True,
            "duration": round(time.time() - started, 3),
        }

    except Exception as e:
        result = {
            "returncode": None,
            "stdout": "",
            "stderr": traceback.format_exc(),
            "timeout": False,
            "exception": repr(e),
            "duration": round(time.time() - started, 3),
        }

    print(
        f"RETURN={result['returncode']} "
        f"TIMEOUT={result['timeout']} "
        f"SECONDS={result['duration']}",
        flush=True,
    )

    if result["stderr"]:
        print("\nSTDERR:")
        print(result["stderr"][-8000:])

    return result


def meda_run(output, timeout):
    if output.exists():
        output.unlink()

    return execute(
        [
            sys.executable,
            str(MAIN),
            "--mode",
            "constraint_only",
            "--setup",
            str(SETUP.resolve()),
            "--problem",
            str(PROBLEM.resolve()),
            "--output",
            str(output.resolve()),
        ],
        timeout=timeout,
        cwd=MEDA,
    )


# ============================================================
# 1. FILE SANITY
# ============================================================

section("1. REQUIRED FILES")

required = [
    MAIN,
    ROOT / "connectors/meda/bridge.py",
    ROOT / "connectors/meda/receiver.py",
    ROOT / "connectors/meda/research_loop.py",
    SETUP,
    PROBLEM,
]

missing = []

for path in required:
    ok = path.exists()
    print(f"{'PASS' if ok else 'FAIL'}  {path}")

    if not ok:
        missing.append(str(path))

record(
    "file_sanity",
    ok=not missing,
    missing=missing,
)

if missing:
    results["decisions"].append("required_files_missing")
    results["final_status"] = "BLOCKED_NEEDS_MANUAL"
    save()
    sys.exit(1)


# ============================================================
# 2. CONFIG VALIDATION
# ============================================================

section("2. CONFIG VALIDATION")

try:
    import yaml

    setup = yaml.safe_load(
        SETUP.read_text(encoding="utf-8")
    ) or {}

    problem = json.loads(
        PROBLEM.read_text(encoding="utf-8")
    )

    print(
        json.dumps(
            {
                "research_type": setup.get("research_type"),
                "mode": setup.get("mode"),
                "output_format": setup.get("output_format"),
                "problem_type": problem.get("type"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    record(
        "config_validation",
        ok=True,
        setup=setup,
        problem=problem,
    )

except Exception as e:
    record(
        "config_validation",
        ok=False,
        error=repr(e),
    )

    results["decisions"].append(
        "configuration_invalid"
    )

    results["final_status"] = "FAIL_CONFIRMED"
    save()
    sys.exit(1)


# ============================================================
# 3. PYTHON COMPILE
# ============================================================

section("3. PYTHON COMPILE")

compile_targets = [
    MAIN,
    ROOT / "connectors/meda/bridge.py",
    ROOT / "connectors/meda/receiver.py",
    ROOT / "connectors/meda/research_loop.py",
]

compile_result = execute(
    [
        sys.executable,
        "-m",
        "py_compile",
        *map(str, compile_targets),
    ],
    timeout=30,
)

compile_ok = (
    not compile_result["timeout"]
    and compile_result["returncode"] == 0
)

record(
    "compile",
    ok=compile_ok,
    result=compile_result,
)

if not compile_ok:
    results["decisions"].append(
        "python_compile_failure"
    )

    results["final_status"] = "FAIL_CONFIRMED"
    save()
    sys.exit(1)


# ============================================================
# 4. STATIC MAIN ANALYSIS
# ============================================================

section("4. STATIC MEDA ANALYSIS")

main_text = MAIN.read_text(
    encoding="utf-8",
    errors="replace",
)

patterns = {
    "subprocess_run": r"subprocess\.run",
    "subprocess_popen": r"subprocess\.Popen",
    "os_system": r"os\.system",
    "while_true": r"while\s+True",
    "range_loop": r"for\s+\w+\s+in\s+range",
    "iteration": r"\biteration\b",
    "max_iterations": r"\bmax_iterations\b",
    "genetic_algorithm": r"\bGA\b|genetic",
    "formalizer": r"formalizer",
    "literature": r"literature",
    "constraint_only": r"constraint_only",
    "data_anchored": r"data_anchored",
    "human_answer": r"human_answer",
    "foundational": r"foundational_inquiry",
}

static_hits = {}

for name, pattern in patterns.items():
    count = len(
        re.findall(
            pattern,
            main_text,
            flags=re.I,
        )
    )

    static_hits[name] = count
    print(f"{name:25} {count}")

record(
    "static_analysis",
    hits=static_hits,
)


# ============================================================
# 5. ALL RELEVANT MEDA PYTHON FILES
# ============================================================

section("5. EXECUTION PATH SCAN")

scan_files = []

for path in MEDA.rglob("*.py"):
    if any(
        excluded in path.parts
        for excluded in [
            "__pycache__",
            ".git",
            ".venv",
            "venv",
        ]
    ):
        continue

    scan_files.append(path)

execution_candidates = []

for path in scan_files:
    try:
        text = path.read_text(
            encoding="utf-8",
            errors="replace",
        )
    except Exception:
        continue

    hits = {
        "while_true": len(
            re.findall(r"while\s+True", text)
        ),
        "subprocess": len(
            re.findall(r"subprocess\.", text)
        ),
        "iteration": len(
            re.findall(r"\biteration\b", text, re.I)
        ),
        "max_iterations": len(
            re.findall(
                r"\bmax_iterations\b",
                text,
                re.I,
            )
        ),
        "ga": len(
            re.findall(
                r"\bGA\b|genetic",
                text,
                re.I,
            )
        ),
    }

    score = (
        hits["while_true"] * 5
        + hits["subprocess"] * 3
        + hits["iteration"] * 2
        + hits["max_iterations"] * 3
        + hits["ga"]
    )

    if score:
        execution_candidates.append(
            {
                "file": str(
                    path.relative_to(ROOT)
                ),
                "score": score,
                **hits,
            }
        )

execution_candidates.sort(
    key=lambda x: x["score"],
    reverse=True,
)

for item in execution_candidates[:40]:
    print(item)

record(
    "execution_path_scan",
    files_scanned=len(scan_files),
    candidates=execution_candidates[:100],
)


# ============================================================
# 6. DIRECT MEDA EXECUTION
# ============================================================

section("6. DIRECT MEDA EXECUTION")

direct = meda_run(
    DIRECT,
    FAST_TIMEOUT,
)

direct_ok = (
    not direct["timeout"]
    and direct["returncode"] == 0
    and DIRECT.exists()
)

record(
    "direct_meda",
    ok=direct_ok,
    timeout=direct["timeout"],
    returncode=direct["returncode"],
    output_exists=DIRECT.exists(),
    duration=direct["duration"],
    stdout=direct["stdout"],
    stderr=direct["stderr"],
)

if direct_ok:

    section("7. DIRECT OUTPUT VALIDATION")

    try:
        data = json.loads(
            DIRECT.read_text(
                encoding="utf-8"
            )
        )

        record(
            "direct_output_validation",
            ok=True,
            json_type=type(data).__name__,
            keys=(
                list(data.keys())
                if isinstance(data, dict)
                else None
            ),
        )

        results["decisions"].append(
            "direct_execution_completed"
        )

        results["final_status"] = "PASS"
        save()

        print("\nFINAL STATUS: PASS")
        print("DIRECT MEDA COMPLETED.")
        print("REPORT:", REPORT)

        sys.exit(0)

    except Exception as e:

        record(
            "direct_output_validation",
            ok=False,
            error=repr(e),
        )

        results["decisions"].append(
            "direct_execution_returned_invalid_output"
        )


# ============================================================
# 7. TIMEOUT DIAGNOSIS
# ============================================================

if direct["timeout"]:

    section("7. TIMEOUT DETECTED")

    results["decisions"].append(
        "initial_meda_timeout"
    )

    suspicious = []

    for match in re.finditer(
        r"""
        subprocess\.(?:run|Popen|call|check_call|check_output)
        |while\s+True
        |max_iterations
        |\biteration\b
        |\bGA\b
        |genetic
        """,
        main_text,
        flags=re.I | re.X,
    ):

        start = max(
            0,
            match.start() - 250,
        )

        end = min(
            len(main_text),
            match.end() + 500,
        )

        suspicious.append(
            {
                "match": match.group(0),
                "context": main_text[start:end],
            }
        )

    print(
        "Suspicious execution locations:",
        len(suspicious),
    )

    record(
        "timeout_static_diagnosis",
        suspicious_count=len(suspicious),
        suspicious=suspicious[:50],
    )


# ============================================================
# 8. IMPORT ISOLATION
# ============================================================

section("8. IMPORT ISOLATION")

modules = [
    "equations",
    "ga",
    "report_baseline",
    "sindy_screen",
    "term_parser",
]

import_results = {}

scripts_dir = MEDA / "skills/meda/scripts"

for module in modules:

    code = f"""
import sys
sys.path.insert(0, r'{scripts_dir}')
import {module}
print('IMPORT_OK:{module}')
"""

    result = execute(
        [
            sys.executable,
            "-c",
            code,
        ],
        timeout=IMPORT_TIMEOUT,
        cwd=MEDA,
    )

    ok = (
        not result["timeout"]
        and result["returncode"] == 0
    )

    import_results[module] = {
        "ok": ok,
        "timeout": result["timeout"],
        "returncode": result["returncode"],
        "stdout": result["stdout"],
        "stderr": result["stderr"],
    }

    print(
        f"{module:20}",
        "PASS" if ok else "FAIL",
    )

record(
    "import_isolation",
    results=import_results,
)

failed_imports = [
    name
    for name, item in import_results.items()
    if not item["ok"]
]


# ============================================================
# 9. INDIVIDUAL SCRIPT EXECUTION TEST
# ============================================================

section("9. INDIVIDUAL SCRIPT EXECUTION")

script_tests = {}

test_scripts = [
    "equations.py",
    "ga.py",
    "report_baseline.py",
    "sindy_screen.py",
    "term_parser.py",
]

for filename in test_scripts:

    path = scripts_dir / filename

    if not path.exists():
        script_tests[filename] = {
            "exists": False,
            "ok": False,
        }
        continue

    result = execute(
        [
            sys.executable,
            "-m",
            "py_compile",
            str(path),
        ],
        timeout=FUNCTION_TIMEOUT,
        cwd=MEDA,
    )

    ok = (
        not result["timeout"]
        and result["returncode"] == 0
    )

    script_tests[filename] = {
        "exists": True,
        "ok": ok,
        "timeout": result["timeout"],
        "returncode": result["returncode"],
        "stderr": result["stderr"],
    }

    print(
        f"{filename:25}",
        "PASS" if ok else "FAIL",
    )

record(
    "individual_script_validation",
    results=script_tests,
)


# ============================================================
# 10. CONTROLLED RETRY
# ============================================================

section("10. CONTROLLED MEDA RETRY")

retry = meda_run(
    RETRY,
    RETRY_TIMEOUT,
)

retry_ok = (
    not retry["timeout"]
    and retry["returncode"] == 0
    and RETRY.exists()
)

record(
    "controlled_retry",
    ok=retry_ok,
    timeout=retry["timeout"],
    returncode=retry["returncode"],
    output_exists=RETRY.exists(),
    duration=retry["duration"],
    stdout=retry["stdout"],
    stderr=retry["stderr"],
)

if retry_ok:

    section("11. RETRY OUTPUT VALIDATION")

    try:

        retry_data = json.loads(
            RETRY.read_text(
                encoding="utf-8"
            )
        )

        record(
            "retry_output_validation",
            ok=True,
            json_type=type(retry_data).__name__,
            keys=(
                list(retry_data.keys())
                if isinstance(retry_data, dict)
                else None
            ),
        )

        results["decisions"].append(
            "initial_timeout_but_retry_completed"
        )

        results["final_status"] = "PASS"

    except Exception as e:

        record(
            "retry_output_validation",
            ok=False,
            error=repr(e),
        )

        results["decisions"].append(
            "retry_completed_with_invalid_output"
        )

        results["final_status"] = "FAIL_CONFIRMED"


else:

    # ========================================================
    # 11. FAILURE CLASSIFICATION
    # ========================================================

    section("11. FAILURE CLASSIFICATION")

    if failed_imports:

        results["decisions"].append(
            "import_failure_confirmed"
        )

        results["final_status"] = (
            "FAIL_CONFIRMED"
        )

    elif retry["timeout"]:

        results["decisions"].append(
            "persistent_execution_timeout"
        )

        results["final_status"] = (
            "FAIL_CONFIRMED"
        )

    elif retry["returncode"] != 0:

        results["decisions"].append(
            "persistent_process_failure"
        )

        results["final_status"] = (
            "FAIL_CONFIRMED"
        )

    else:

        results["decisions"].append(
            "failure_cause_undetermined"
        )

        results["final_status"] = (
            "BLOCKED_NEEDS_MANUAL"
        )


# ============================================================
# 12. FINAL DIAGNOSTIC SUMMARY
# ============================================================

section("12. FINAL DIAGNOSTIC SUMMARY")

if results["final_status"] == "PASS":
    summary = (
        "MEDA completed successfully after adaptive diagnostics."
    )

elif results["final_status"] == "FAIL_CONFIRMED":
    summary = (
        "MEDA failure was empirically reproduced after "
        "diagnostic isolation/retry."
    )

else:
    summary = (
        "The diagnostic chain could not uniquely identify "
        "the failure automatically."
    )

results["summary"] = summary

save()

print("\n" + "=" * 78)
print("FINAL STATUS:", results["final_status"])
print("=" * 78)

print("\nDECISIONS:")

for decision in results["decisions"]:
    print(" -", decision)

print("\nREPORT:")
print(REPORT)

print("\nDIRECT:")
print(DIRECT)

print("\nRETRY:")
print(RETRY)

save()
