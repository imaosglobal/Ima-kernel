from pathlib import Path
import py_compile
from datetime import datetime
import shutil

ROOT = Path(".ima/research")
COUNCIL = ROOT / "ima_research_council.py"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = ROOT / "backups"
backup_dir.mkdir(parents=True, exist_ok=True)

backup = backup_dir / f"ima_research_council_before_routing_v51_{timestamp}.py"
shutil.copy2(COUNCIL, backup)

text = COUNCIL.read_text(encoding="utf-8")

# ------------------------------------------------------------
# 1. Fix runtime architecture banner
# ------------------------------------------------------------

old_banner = 'self.log("IMA RESEARCH COUNCIL V4")'
new_banner = 'self.log("IMA RESEARCH COUNCIL V5.1")'

if old_banner in text:
    text = text.replace(old_banner, new_banner, 1)

# ------------------------------------------------------------
# 2. Route Semantic Scholar into every Literature subquestion
# ------------------------------------------------------------
#
# The registry alone is insufficient.
# Jobs are created exclusively from sub["agents"].
#
# Therefore whenever LITERATURE is assigned to a subquestion,
# SEMANTIC_SCHOLAR must also be assigned unless already present.
# ------------------------------------------------------------

anchor = '''        record["subquestions"] = (
            decomposition["subquestions"]
        )
'''

insertion = '''        record["subquestions"] = (
            decomposition["subquestions"]
        )

        # ====================================================
        # V5.1 LITERATURE ROUTING
        # ====================================================
        # Registry enablement does not create jobs by itself.
        # The job graph is built from subquestion["agents"].
        #
        # Route Semantic Scholar alongside LITERATURE so that
        # bibliographic evidence has an independent provider.
        # ====================================================

        for sub in record["subquestions"]:
            agents = sub.setdefault("agents", [])

            if (
                "LITERATURE" in agents
                and "SEMANTIC_SCHOLAR" not in agents
            ):
                agents.append("SEMANTIC_SCHOLAR")
'''

if anchor not in text:
    raise SystemExit(
        "ERROR: subquestion routing insertion point not found"
    )

if "V5.1 LITERATURE ROUTING" not in text:
    text = text.replace(anchor, insertion, 1)

# ------------------------------------------------------------
# 3. Write
# ------------------------------------------------------------

COUNCIL.write_text(text, encoding="utf-8")

# ------------------------------------------------------------
# 4. Compile
# ------------------------------------------------------------

targets = [
    COUNCIL,
    ROOT / "agents" / "semantic_scholar_agent.py",
]

for path in targets:
    py_compile.compile(str(path), doraise=True)

# ------------------------------------------------------------
# 5. Validation
# ------------------------------------------------------------

final = COUNCIL.read_text(encoding="utf-8")

checks = {
    "ARCHITECTURE_V5.1_BANNER":
        "IMA RESEARCH COUNCIL V5.1" in final,

    "SEMANTIC_SCHOLAR_IMPORT":
        "from agents.semantic_scholar_agent import SemanticScholarAgent"
        in final,

    "SEMANTIC_SCHOLAR_ROUTING":
        '"SEMANTIC_SCHOLAR" not in agents' in final,

    "LITERATURE_ROUTING_BLOCK":
        "V5.1 LITERATURE ROUTING" in final,

    "V5.1_ARCHITECTURE":
        '"architecture": "IMA_RESEARCH_COUNCIL_V5"' in final,
}

print("=" * 78)
print("IMA RESEARCH COUNCIL V5.1 — ORCHESTRATION ROUTING PATCH")
print("=" * 78)
print("BACKUP:", backup)
print()

for name, ok in checks.items():
    print(
        f"{name}:",
        "PASS" if ok else "FAIL"
    )

print()
print("COMPILE: PASS")

if not all(checks.values()):
    print("VALIDATION: FAIL")
    raise SystemExit(2)

print("VALIDATION: PASS")
print("=" * 78)
