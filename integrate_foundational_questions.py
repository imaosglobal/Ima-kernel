from pathlib import Path
import json
import shutil
import time
import yaml

ROOT = Path.cwd()
MEDA = ROOT / "external/MEDA"
SESSION = MEDA / "sessions/ima_universe_intelligence"

PROBLEM = SESSION / "problem.json"
SETUP = SESSION / "setup.yaml"

BACKUP_DIR = SESSION / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

STAMP = time.strftime("%Y%m%d_%H%M%S")

PROBLEM_BACKUP = BACKUP_DIR / f"problem_{STAMP}.json"
SETUP_BACKUP = BACKUP_DIR / f"setup_{STAMP}.yaml"

print("=" * 78)
print("IMA <-> MEDA FOUNDATIONAL QUESTION INTEGRATION")
print("=" * 78)

# ============================================================
# 1. SANITY
# ============================================================

for path in [PROBLEM, SETUP]:
    if not path.exists():
        print("MISSING:", path)
        raise SystemExit(1)

print("PASS:", PROBLEM)
print("PASS:", SETUP)

# ============================================================
# 2. BACKUP
# ============================================================

shutil.copy2(PROBLEM, PROBLEM_BACKUP)
shutil.copy2(SETUP, SETUP_BACKUP)

print()
print("BACKUP:")
print(PROBLEM_BACKUP)
print(SETUP_BACKUP)

# ============================================================
# 3. LOAD
# ============================================================

problem = json.loads(
    PROBLEM.read_text(encoding="utf-8")
)

setup = yaml.safe_load(
    SETUP.read_text(encoding="utf-8")
) or {}

# ============================================================
# 4. ORIGINAL QUESTION
# ============================================================

original_question = problem.get("question", "")

# ============================================================
# 5. NEW QUESTIONS
# ============================================================

new_questions = [
    {
        "id": "ai_emergence_evidence",
        "question": (
            "האם העובדה שהיקום יצר בתוכו אדם המסוגל ליצור "
            "מחשבים, תוכנה ובינה מלאכותית היא ראיה כלשהי "
            "לאינטליגנציה של היקום עצמו?"
        ),
        "category": "cosmic_intelligence",
    },
    {
        "id": "universe_self_modeling",
        "question": (
            "האם IMA/MEDA יכולות להיחשב דוגמה לכך שהיקום "
            "נעשה מסוגל לבנות בתוכו מערכות שמדמות, חוקרות "
            "ומפרשות את היקום עצמו?"
        ),
        "category": "self_modeling_universe",
    },
    {
        "id": "contains_vs_generates",
        "question": (
            "האם יש הבדל עקרוני בין יקום שמכיל אינטליגנציה "
            "לבין יקום שמייצר ומרחיב אינטליגנציה?"
        ),
        "category": "emergence",
    },
    {
        "id": "artificial_intelligence_cosmic_evidence",
        "question": (
            "האם הופעת אינטליגנציה מלאכותית מתוך תהליכים "
            "טבעיים מחזקת או מחלישה את ההשערה של אינטליגנציה קוסמית?"
        ),
        "category": "artificial_intelligence",
    },
    {
        "id": "natural_explanation",
        "question": (
            "האם ניתן להסביר את כל השרשרת "
            "חומר → חיים → תודעה → אינטליגנציה → טכנולוגיה → AI "
            "ללא הנחת אינטליגנציה בסיסית במציאות?"
        ),
        "category": "naturalistic_explanation",
    },
    {
        "id": "universe_questioning_itself",
        "question": (
            "האם עצם העובדה שמערכת שנוצרה בתוך היקום יכולה לשאול "
            "את השאלה 'האם היקום אינטליגנטי?' היא תופעה שצריך "
            "להסביר במסגרת התיאוריה של מקור האינטליגנציה?"
        ),
        "category": "self_reference",
    },
    {
        "id": "recursive_intelligence",
        "question": (
            "האם יש משמעות למעבר שבו היקום אינו רק מכיל צופים, "
            "אלא מייצר צופים שמסוגלים לבנות מערכות אינטליגנטיות "
            "נוספות, אשר בעצמן מסוגלות לחקור את מקור המציאות?"
        ),
        "category": "recursive_intelligence",
    },
]

# ============================================================
# 6. ADD WITHOUT DUPLICATES
# ============================================================

existing = problem.get("additional_questions", [])

if not isinstance(existing, list):
    existing = []

existing_ids = {
    item.get("id")
    for item in existing
    if isinstance(item, dict)
}

added = []

for item in new_questions:
    if item["id"] not in existing_ids:
        existing.append(item)
        added.append(item["id"])

problem["additional_questions"] = existing

print()
print("NEW QUESTIONS ADDED:", len(added))

for item in added:
    print(" +", item)

# ============================================================
# 7. CREATE EXPLICIT RESEARCH AXIS
# ============================================================

problem["research_axes"] = [
    "cosmic_intelligence",
    "emergence_of_intelligence",
    "artificial_intelligence",
    "universe_self_modeling",
    "recursive_intelligence",
    "naturalistic_explanation",
    "observer_reality",
    "cosmic_purpose",
    "existence_itself",
]

problem["required_comparison"] = {
    "H1": (
        "היקום עצמו אינטליגנטי במובן מהותי או מערכתי."
    ),
    "H2": (
        "אינטליגנציה היא תופעה מתהווה של מערכות מקומיות "
        "בתוך יקום שאינו אינטליגנטי."
    ),
    "H3": (
        "תודעה או תכונות פרוטו-תודעתיות הן בסיסיות למציאות."
    ),
    "H4": (
        "המציאות היא סימולציה, חישוב או מבנה מידע עמוק יותר."
    ),
    "H5": (
        "אין כיום אפשרות מדעית להכריע בין ההשערות המטפיזיות."
    ),
}

# ============================================================
# 8. CRITICAL LOGICAL TEST
# ============================================================

problem["critical_logical_test"] = {
    "question": (
        "האם הופעת אינטליגנציה בתוך היקום מהווה ראיה "
        "לאינטליגנציה של היקום עצמו?"
    ),
    "must_distinguish": [
        "היקום מכיל אינטליגנציה",
        "היקום מאפשר אינטליגנציה",
        "היקום מייצר אינטליגנציה",
        "היקום דורש אינטליגנציה כדי להסביר את האינטליגנציה",
        "היקום עצמו הוא ישות אינטליגנטית",
    ],
    "fallacy_to_avoid": (
        "אין להסיק אוטומטית מהופעת אינטליגנציה בתוך מערכת "
        "שהמערכת כולה אינטליגנטית."
    ),
    "counterpoint_to_test": (
        "עם זאת, יש לבדוק האם היכולת של היקום לייצר שוב ושוב "
        "מערכות שמייצרות מודלים של המציאות, טכנולוגיה ובינה "
        "מלאכותית דורשת הסבר עמוק יותר מהסבר מקומי של מוח יחיד."
    ),
}

# ============================================================
# 9. ADD EMPIRICAL PROGRAM
# ============================================================

problem["empirical_program"] = [
    {
        "test": "emergence_of_complexity",
        "goal": (
            "לבדוק האם מורכבות ואינטליגנציה יכולות להופיע "
            "באופן עקבי מתהליכים שאינם מכילים תכנון מודע."
        ),
    },
    {
        "test": "artificial_evolution",
        "goal": (
            "לבדוק האם מערכות אבולוציוניות מייצרות "
            "התנהגות אינטליגנטית ללא מתכנן אינטליגנטי."
        ),
    },
    {
        "test": "self_modeling",
        "goal": (
            "לבדוק האם מערכות טבעיות/מלאכותיות יכולות לפתח "
            "מודלים של עצמן ושל הסביבה באופן ספונטני."
        ),
    },
    {
        "test": "cosmological_information_structure",
        "goal": (
            "לבדוק האם קיימות תבניות אוניברסליות שאינן מוסברות "
            "מספיק על ידי דינמיקה פיזיקלית מוכרת."
        ),
    },
    {
        "test": "artificial_intelligence_emergence",
        "goal": (
            "לחקור האם יצירת מערכות AI מתוך תהליכים טבעיים "
            "ומלאכותיים משנה את הראיות בעד או נגד אינטליגנציה קוסמית."
        ),
    },
]

# ============================================================
# 10. PRESERVE QUESTION EXACTLY
# ============================================================

problem["preserve_original_question"] = True
problem["original_question_hash_basis"] = original_question

# ============================================================
# 11. WRITE PROBLEM
# ============================================================

PROBLEM.write_text(
    json.dumps(
        problem,
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)

print()
print("UPDATED PROBLEM:")
print(PROBLEM)

# ============================================================
# 12. UPDATE SETUP
# ============================================================

setup["research_type"] = "foundational_inquiry"
setup["mode"] = "constraint_only"

setup["preserve_original_question"] = True
setup["require_human_answer"] = True
setup["compare_hypotheses"] = True
setup["separate_empirical_logical_philosophical"] = True
setup["require_counterarguments"] = True
setup["require_unknowns"] = True
setup["require_testable_predictions"] = True

setup["require_direct_answer"] = True
setup["require_synthesis"] = True
setup["return_to_ima"] = True

setup["answer_contract"] = {
    "direct_answer_first": True,
    "empirical_section": True,
    "logical_section": True,
    "philosophical_section": True,
    "unknowns_section": True,
    "discriminating_tests": True,
    "counterarguments": True,
    "final_synthesis": True,
    "preserve_question": True,
}

setup["handoff"] = {
    "producer": "MEDA",
    "consumer": "IMA",
    "artifact_type": "foundational_research_answer",
    "must_include": [
        "question",
        "answer",
        "hypotheses",
        "evidence",
        "logical_inferences",
        "unknowns",
        "tests",
        "counterarguments",
        "synthesis",
    ],
}

SETUP.write_text(
    yaml.safe_dump(
        setup,
        allow_unicode=True,
        sort_keys=False,
    ),
    encoding="utf-8",
)

print("UPDATED SETUP:")
print(SETUP)

# ============================================================
# 13. CREATE IMA HANDOFF CONTRACT
# ============================================================

HANDOFF = SESSION / "ima_handoff_contract.json"

handoff = {
    "type": "foundational_research_answer",
    "version": "1.0",
    "producer": "MEDA",
    "consumer": "IMA",
    "question": original_question,
    "additional_questions": new_questions,
    "instruction": (
        "MEDA must investigate the complete question set and "
        "return a human-readable answer to IMA."
    ),
    "answer_requirements": [
        "answer_the_actual_question",
        "do_not_replace_with_unrelated_math",
        "distinguish_evidence_from_inference",
        "compare_H1_H2_H3_H4_H5",
        "address_AI_as_evidence",
        "address_universe_self_modeling",
        "address_recursive_intelligence",
        "state_unknowns",
        "propose_discriminating_observations",
        "give_final_synthesis",
    ],
    "return_target": "IMA",
    "session": str(SESSION),
}

HANDOFF.write_text(
    json.dumps(
        handoff,
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)

# ============================================================
# 14. CREATE RUNNER THAT RETURNS RESULT TO IMA
# ============================================================

RUNNER = SESSION / "run_foundational_and_return_to_ima.py"

runner_code = r'''
from pathlib import Path
import json
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
MEDA = ROOT / "external/MEDA"
MAIN = MEDA / "skills/meda/scripts/main.py"

SESSION = MEDA / "sessions/ima_universe_intelligence"
SETUP = SESSION / "setup.yaml"
PROBLEM = SESSION / "problem.json"

OUTPUT = SESSION / "ima_foundational_answer.json"

print("=" * 78)
print("MEDA FOUNDATIONAL RESEARCH -> IMA")
print("=" * 78)

if OUTPUT.exists():
    OUTPUT.unlink()

started = time.time()

process = subprocess.run(
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
        str(OUTPUT.resolve()),
    ],
    cwd=str(MEDA),
    text=True,
    capture_output=True,
    timeout=180,
)

result = {
    "producer": "MEDA",
    "consumer": "IMA",
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "duration": round(time.time() - started, 3),
    "returncode": process.returncode,
    "stdout": process.stdout[-30000:],
    "stderr": process.stderr[-30000:],
    "output_exists": OUTPUT.exists(),
}

if OUTPUT.exists():
    try:
        result["answer"] = json.loads(
            OUTPUT.read_text(
                encoding="utf-8"
            )
        )
        result["status"] = "ANSWER_READY_FOR_IMA"
    except Exception as e:
        result["status"] = "INVALID_MEDА_OUTPUT"
        result["parse_error"] = repr(e)
else:
    result["status"] = "MEDA_NO_ANSWER"

HANDOFF_RESULT = SESSION / "ima_handoff_result.json"

HANDOFF_RESULT.write_text(
    json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)

print()
print("STATUS:", result["status"])
print("HANDOFF:", HANDOFF_RESULT)
print("ANSWER:", OUTPUT)

if result["status"] == "ANSWER_READY_FOR_IMA":
    print()
    print("MEDA ANSWER:")
    print(
        json.dumps(
            result["answer"],
            ensure_ascii=False,
            indent=2,
        )[:50000]
    )
'''

RUNNER.write_text(
    runner_code,
    encoding="utf-8",
)

# ============================================================
# 15. FINAL MANIFEST
# ============================================================

MANIFEST = SESSION / "integration_manifest.json"

manifest = {
    "status": "INTEGRATED",
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "original_question_preserved": True,
    "new_questions_added": added,
    "problem": str(PROBLEM),
    "setup": str(SETUP),
    "handoff_contract": str(HANDOFF),
    "runner": str(RUNNER),
    "backup_problem": str(PROBLEM_BACKUP),
    "backup_setup": str(SETUP_BACKUP),
    "next_step": (
        "run run_foundational_and_return_to_ima.py"
    ),
}

MANIFEST.write_text(
    json.dumps(
        manifest,
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)

# ============================================================
# 16. VALIDATE JSON/YAML
# ============================================================

json.loads(
    PROBLEM.read_text(encoding="utf-8")
)

yaml.safe_load(
    SETUP.read_text(encoding="utf-8")
)

print()
print("=" * 78)
print("INTEGRATION COMPLETE")
print("=" * 78)

print("Questions added:", len(added))
print("Problem:", PROBLEM)
print("Setup:", SETUP)
print("Handoff:", HANDOFF)
print("Runner:", RUNNER)
print("Manifest:", MANIFEST)

print()
print("NOW RUN:")
print(
    "python3 "
    "external/MEDA/sessions/"
    "ima_universe_intelligence/"
    "run_foundational_and_return_to_ima.py"
)
