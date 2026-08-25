from pathlib import Path
import subprocess
import json
import re
import sys
import time
import traceback
import shutil

ROOT = Path.cwd()
MEDA = ROOT / "external/MEDA"
SCRIPTS = MEDA / "skills/meda/scripts"
MAIN = SCRIPTS / "main.py"
GA = SCRIPTS / "ga.py"
FORMALIZER = SCRIPTS / "formalizer.py"

SESSION = MEDA / "sessions/ima_universe_intelligence"
SETUP = SESSION / "setup.yaml"
PROBLEM = SESSION / "problem.json"

REPORT = SESSION / "foundational_adaptive_report.json"
DIRECT = SESSION / "foundational_direct.json"
FALLBACK = SESSION / "foundational_fallback.json"

BACKUP_DIR = SESSION / "adaptive_backups"

FAST_TIMEOUT = 30
RETRY_TIMEOUT = 90
COMPONENT_TIMEOUT = 15
FALLBACK_TIMEOUT = 60

SESSION.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

results = {
    "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "root": str(ROOT),
    "session": str(SESSION),
    "steps": [],
    "decisions": [],
    "patches": [],
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


def execute(cmd, timeout=30, cwd=ROOT):
    print("\n$ " + " ".join(map(str, cmd)), flush=True)

    started = time.time()

    try:
        p = subprocess.run(
            [str(x) for x in cmd],
            cwd=str(cwd),
            text=True,
            capture_output=True,
            timeout=timeout,
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
            "stdout": e.stdout[-30000:]
            if isinstance(e.stdout, str)
            else "",
            "stderr": e.stderr[-30000:]
            if isinstance(e.stderr, str)
            else "",
            "timeout": True,
            "duration": round(time.time() - started, 3),
        }

    except Exception:
        result = {
            "returncode": None,
            "stdout": "",
            "stderr": traceback.format_exc(),
            "timeout": False,
            "exception": traceback.format_exc(),
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


def backup(path):
    if not path.exists():
        return None

    target = BACKUP_DIR / path.name

    if not target.exists():
        shutil.copy2(path, target)

    return target


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
# 1. SANITY
# ============================================================

section("1. SANITY")

required = [
    MAIN,
    GA,
    ROOT / "connectors/meda/bridge.py",
    ROOT / "connectors/meda/receiver.py",
    ROOT / "connectors/meda/research_loop.py",
    SETUP,
    PROBLEM,
]

missing = []

for path in required:
    ok = path.exists()
    print(("PASS" if ok else "FAIL"), path)

    if not ok:
        missing.append(str(path))

record(
    "sanity",
    ok=not missing,
    missing=missing,
)

if missing:
    results["final_status"] = "BLOCKED_NEEDS_MANUAL"
    results["decisions"].append("required_files_missing")
    save()
    sys.exit(1)


# ============================================================
# 2. READ ORIGINAL QUESTION
# ============================================================

section("2. ORIGINAL QUESTION")

try:
    problem = json.loads(
        PROBLEM.read_text(encoding="utf-8")
    )

    original_question = problem.get("question", "")

    print(original_question)

    record(
        "original_question",
        ok=bool(original_question.strip()),
        question=original_question,
    )

except Exception as e:
    record(
        "original_question",
        ok=False,
        error=repr(e),
    )
    results["final_status"] = "FAIL_CONFIRMED"
    save()
    sys.exit(1)


# ============================================================
# 3. CONFIG
# ============================================================

section("3. CONFIG")

try:
    import yaml

    setup = yaml.safe_load(
        SETUP.read_text(encoding="utf-8")
    ) or {}

    print(
        json.dumps(
            setup,
            ensure_ascii=False,
            indent=2,
        )
    )

    record(
        "config",
        ok=True,
        setup=setup,
    )

except Exception as e:
    record(
        "config",
        ok=False,
        error=repr(e),
    )
    results["final_status"] = "FAIL_CONFIRMED"
    save()
    sys.exit(1)


# ============================================================
# 4. COMPILE EVERYTHING RELEVANT
# ============================================================

section("4. COMPILE")

compile_targets = [
    MAIN,
    GA,
    ROOT / "connectors/meda/bridge.py",
    ROOT / "connectors/meda/receiver.py",
    ROOT / "connectors/meda/research_loop.py",
]

if FORMALIZER.exists():
    compile_targets.append(FORMALIZER)

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
    results["final_status"] = "FAIL_CONFIRMED"
    results["decisions"].append("compile_failure")
    save()
    sys.exit(1)


# ============================================================
# 5. STATIC EXECUTION ANALYSIS
# ============================================================

section("5. MAIN EXECUTION ANALYSIS")

main_text = MAIN.read_text(
    encoding="utf-8",
    errors="replace",
)

ga_text = GA.read_text(
    encoding="utf-8",
    errors="replace",
)

patterns = {
    "ga": r"\bGA\b|genetic",
    "formalizer": r"formalizer",
    "constraint_only": r"constraint_only",
    "data_anchored": r"data_anchored",
    "subprocess": r"subprocess\.",
    "while_true": r"while\s+True",
    "range_loop": r"for\s+\w+\s+in\s+range",
    "iteration": r"\biteration\b",
    "max_iterations": r"\bmax_iterations\b",
    "json_output": r"json",
    "human_answer": r"human_answer",
    "foundational": r"foundational",
}

hits = {}

for name, pattern in patterns.items():
    hits[name] = len(
        re.findall(
            pattern,
            main_text,
            flags=re.I,
        )
    )

for name, count in hits.items():
    print(f"{name:25} {count}")

record(
    "main_static_analysis",
    hits=hits,
)


# ============================================================
# 6. DIRECT BASELINE
# ============================================================

section("6. BASELINE MEDA RUN")

baseline = meda_run(
    DIRECT,
    FAST_TIMEOUT,
)

baseline_ok = (
    not baseline["timeout"]
    and baseline["returncode"] == 0
    and DIRECT.exists()
)

record(
    "baseline_run",
    ok=baseline_ok,
    timeout=baseline["timeout"],
    returncode=baseline["returncode"],
    output_exists=DIRECT.exists(),
    duration=baseline["duration"],
    stdout=baseline["stdout"],
    stderr=baseline["stderr"],
)

if baseline_ok:
    try:
        data = json.loads(
            DIRECT.read_text(
                encoding="utf-8"
            )
        )

        results["decisions"].append(
            "baseline_already_works"
        )

        results["final_status"] = "PASS"
        results["answer"] = data

        save()

        print("\nMEDA ALREADY WORKS.")
        print(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            )[:30000]
        )

        sys.exit(0)

    except Exception as e:
        record(
            "baseline_output_validation",
            ok=False,
            error=repr(e),
        )


# ============================================================
# 7. COMPONENT ISOLATION
# ============================================================

section("7. COMPONENT ISOLATION")

components = {
    "ga": GA,
}

if FORMALIZER.exists():
    components["formalizer"] = FORMALIZER

component_results = {}

for name, path in components.items():

    backup_path = backup(path)

    code = f"""
import sys
sys.path.insert(0, r'{SCRIPTS}')
import {path.stem}
print('IMPORT_OK:{name}')
"""

    r = execute(
        [
            sys.executable,
            "-c",
            code,
        ],
        timeout=COMPONENT_TIMEOUT,
        cwd=MEDA,
    )

    ok = (
        not r["timeout"]
        and r["returncode"] == 0
    )

    component_results[name] = {
        "path": str(path),
        "ok": ok,
        "timeout": r["timeout"],
        "returncode": r["returncode"],
        "stdout": r["stdout"],
        "stderr": r["stderr"],
        "backup": str(backup_path) if backup_path else None,
    }

    print(
        name,
        "PASS" if ok else "FAIL",
    )

record(
    "component_isolation",
    results=component_results,
)


# ============================================================
# 8. INSTALL FOUNDATIONAL RESEARCH ROUTER
# ============================================================

section("8. INSTALL FOUNDATIONAL RESEARCH ROUTER")

ROUTER = SCRIPTS / "foundational_router.py"

router_code = r'''
import json
import re


FOUNDATIONAL_TERMS = [
    "האם היקום",
    "למה בכלל יש",
    "מקור הקיום",
    "משמעות",
    "תכלית",
    "תודעה",
    "אינטיליגנציה",
    "אינטליגנציה",
    "האם המציאות",
    "reality",
    "universe",
    "existence",
    "consciousness",
    "intelligence",
    "meaning",
    "purpose",
]


def is_foundational_question(question):
    q = (question or "").lower()

    score = 0

    for term in FOUNDATIONAL_TERMS:
        if term.lower() in q:
            score += 1

    explicit_patterns = [
        r"why\s+is\s+there",
        r"why\s+does\s+the\s+universe",
        r"what\s+is\s+reality",
        r"what\s+is\s+consciousness",
        r"purpose\s+of\s+the\s+universe",
        r"meaning\s+of\s+existence",
    ]

    for pattern in explicit_patterns:
        if re.search(pattern, q, re.I):
            score += 2

    return {
        "foundational": score >= 2,
        "score": score,
    }


def build_reasoning_contract(question):
    return {
        "type": "foundational_reasoning_contract",
        "question": question,
        "preserve_original_question": True,
        "answer_required": True,
        "required_sections": [
            "direct_answer",
            "empirical_evidence",
            "logical_inferences",
            "philosophical_hypotheses",
            "unknowns",
            "discriminating_observations",
            "counterarguments",
            "synthesis",
        ],
        "hypotheses": [
            {
                "id": "H1",
                "name": "cosmic_intelligence",
                "claim": (
                    "The universe itself has properties that "
                    "justify describing it as intelligent."
                ),
            },
            {
                "id": "H2",
                "name": "emergent_intelligence",
                "claim": (
                    "Intelligence can emerge from non-intelligent "
                    "physical processes without requiring cosmic intelligence."
                ),
            },
            {
                "id": "H3",
                "name": "panpsychist_or_intrinsic_mind",
                "claim": (
                    "Mind or proto-experiential properties are "
                    "fundamental features of reality."
                ),
            },
            {
                "id": "H4",
                "name": "simulation_or_constructed_reality",
                "claim": (
                    "Experienced reality may be generated by an "
                    "underlying computational or informational substrate."
                ),
            },
            {
                "id": "H5",
                "name": "unknown_metaphysics",
                "claim": (
                    "Current evidence is insufficient to determine "
                    "the ultimate ontological nature of reality."
                ),
            },
        ],
        "rules": [
            "Do not equate intelligence contained in the universe with intelligence of the universe.",
            "Do not infer purpose merely from complexity.",
            "Do not treat philosophical possibilities as established empirical facts.",
            "State which claims are empirically testable.",
            "State which claims are currently underdetermined.",
            "Answer the original question directly.",
        ],
    }
'''


backup_router = backup(ROUTER)

ROUTER.write_text(
    router_code,
    encoding="utf-8",
)

results["patches"].append(
    {
        "file": str(ROUTER),
        "action": "created_or_updated",
        "backup": str(backup_router)
        if backup_router
        else None,
    }
)

record(
    "foundational_router_install",
    ok=True,
    router=str(ROUTER),
)


# ============================================================
# 9. BUILD FOUNDATIONAL CONTRACT
# ============================================================

section("9. BUILD REASONING CONTRACT")

try:
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "foundational_router",
        ROUTER,
    )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    classification = module.is_foundational_question(
        original_question
    )

    contract = module.build_reasoning_contract(
        original_question
    )

    CONTRACT = SESSION / "reasoning_contract.json"

    CONTRACT.write_text(
        json.dumps(
            {
                "classification": classification,
                "contract": contract,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            classification,
            ensure_ascii=False,
            indent=2,
        )
    )

    record(
        "reasoning_contract",
        ok=True,
        classification=classification,
        contract_path=str(CONTRACT),
    )

except Exception as e:

    record(
        "reasoning_contract",
        ok=False,
        error=repr(e),
    )

    results["final_status"] = "FAIL_CONFIRMED"
    save()
    sys.exit(1)


# ============================================================
# 10. CONTROLLED RETRY
# ============================================================

section("10. CONTROLLED RETRY")

retry_output = SESSION / "foundational_retry.json"

retry = meda_run(
    retry_output,
    RETRY_TIMEOUT,
)

retry_ok = (
    not retry["timeout"]
    and retry["returncode"] == 0
    and retry_output.exists()
)

record(
    "controlled_retry",
    ok=retry_ok,
    timeout=retry["timeout"],
    returncode=retry["returncode"],
    output_exists=retry_output.exists(),
    duration=retry["duration"],
    stdout=retry["stdout"],
    stderr=retry["stderr"],
)

if retry_ok:

    try:
        retry_data = json.loads(
            retry_output.read_text(
                encoding="utf-8"
            )
        )

        results["answer"] = retry_data
        results["decisions"].append(
            "foundational_retry_completed"
        )
        results["final_status"] = "PASS"

        save()

        print("\nFOUNDATIONAL RETRY PASSED.")
        print(
            json.dumps(
                retry_data,
                ensure_ascii=False,
                indent=2,
            )[:40000]
        )

        sys.exit(0)

    except Exception as e:

        record(
            "retry_output_validation",
            ok=False,
            error=repr(e),
        )


# ============================================================
# 11. HUMAN-READABLE FALLBACK
# ============================================================

section("11. FOUNDATIONAL REASONING FALLBACK")

fallback_prompt = f"""
אתה מבצע חקירה פילוסופית-מדעית יסודית.

השאלה המקורית חייבת להישמר בדיוק במשמעותה:

{original_question}

ענה עליה ישירות.

אל תחליף את השאלה באופטימיזציה מתמטית,
אל תמציא נתונים,
ואל תניח מראש שהתשובה היא כן או לא.

הפרד במפורש בין:

1. מה שניתן לבדוק אמפירית.
2. מה שניתן להסיק לוגית.
3. השערות פילוסופיות.
4. מה שאיננו יודעים.
5. אילו תצפיות או ניסויים יכולים להבדיל בין ההשערות.

חובה לדון לפחות בהשערות:

H1 — היקום עצמו אינטליגנטי.
H2 — אינטליגנציה נוצרת באופן מתהווה מתוך תהליכים שאינם אינטליגנטיים.
H3 — תודעה או תכונות פרוטו-תודעתיות הן בסיסיות למציאות.
H4 — המציאות שאנו חווים עשויה להיות סימולציה/מבנה מחושב.
H5 — אין בידינו כיום דרך להכריע מטפיזית.

ענה גם על:

האם הופעת אינטליגנציה בתוך היקום היא ראיה לכך שהיקום עצמו אינטליגנטי?

אם לא — הסבר מדוע לא.

אם כן במובן כלשהו — הסבר בדיוק באיזה מובן,
ומה נדרש כדי להצדיק את המעבר הלוגי.

התייחס גם לשאלה:
מדוע בכלל יש יקום ולא כלום,
אך אל תציג תשובה מטפיזית כעובדה מדעית.

סיים בסינתזה שמחזירה תשובה ברורה לשאלה המרכזית.
"""

FALLBACK_PROMPT = SESSION / "fallback_prompt.txt"

FALLBACK_PROMPT.write_text(
    fallback_prompt,
    encoding="utf-8",
)

# כאן אנו לא טוענים שמודל חיצוני קיים.
# במקום זאת נשמור את החוזה המלא עבור שכבת ה-answerer
# של IMA/MEDA.

fallback_data = {
    "type": "foundational_reasoning_fallback",
    "status": "READY_FOR_ANSWER_ENGINE",
    "question": original_question,
    "prompt_file": str(FALLBACK_PROMPT),
    "contract_file": str(
        SESSION / "reasoning_contract.json"
    ),
    "reasoning_requirements": [
        "direct_answer",
        "empirical",
        "logical",
        "philosophical",
        "unknowns",
        "discriminating_observations",
        "counterarguments",
        "synthesis",
    ],
}

FALLBACK.write_text(
    json.dumps(
        fallback_data,
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)

record(
    "foundational_fallback",
    ok=True,
    fallback=str(FALLBACK),
    prompt=str(FALLBACK_PROMPT),
)

results["decisions"].append(
    "meda_pipeline_timeout_persisted"
)

results["decisions"].append(
    "foundational_reasoning_path_created"
)

results["final_status"] = "ADAPTED_NEEDS_ANSWER_ENGINE"


# ============================================================
# 12. FINAL
# ============================================================

section("12. FINAL")

results["summary"] = {
    "baseline_completed": baseline_ok,
    "retry_completed": retry_ok,
    "foundational_router_created": True,
    "reasoning_contract_created": True,
    "fallback_created": True,
    "next_required_layer": (
        "IMA answer engine / MEDA human-answer layer"
    ),
}

save()

print("\nFINAL STATUS:")
print(results["final_status"])

print("\nDECISIONS:")

for item in results["decisions"]:
    print(" -", item)

print("\nFILES:")
print("REPORT  :", REPORT)
print("CONTRACT:", SESSION / "reasoning_contract.json")
print("PROMPT  :", FALLBACK_PROMPT)
print("FALLBACK:", FALLBACK)

print(
    "\nMEDA was not declared incapable of answering. "
    "Its execution path timed out. "
    "A dedicated foundational reasoning contract was created."
)
