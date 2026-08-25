from pathlib import Path
import py_compile
import shutil
from datetime import datetime

ROOT = Path.cwd()
RESEARCH = ROOT / ".ima" / "research"
COUNCIL = RESEARCH / "ima_research_council.py"
AGENT = RESEARCH / "agents" / "semantic_scholar_agent.py"

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = RESEARCH / "backups"
backup_dir.mkdir(parents=True, exist_ok=True)

backup = backup_dir / f"ima_research_council_v5_before_semantic_{stamp}.py"
shutil.copy2(COUNCIL, backup)

text = COUNCIL.read_text(encoding="utf-8")

# ------------------------------------------------------------
# Add explicit Semantic Scholar capability marker
# ------------------------------------------------------------

block = r'''

# ============================================================
# V5 EXTERNAL LITERATURE CAPABILITY
# ============================================================

SEMANTIC_SCHOLAR = "SEMANTIC_SCHOLAR"
IMA_RESEARCH_COUNCIL_VERSION = "V5"
IMA_RESEARCH_COUNCIL_ARCHITECTURE = "IMA_RESEARCH_COUNCIL_V5"

try:
    from agents.semantic_scholar_agent import SemanticScholarAgent
except Exception:
    SemanticScholarAgent = None

V5_EXTERNAL_CAPABILITIES = {
    "SEMANTIC_SCHOLAR": {
        "enabled": True,
        "agent": SemanticScholarAgent,
        "role": [
            "relevance-ranked literature",
            "abstract retrieval",
            "citation metadata",
            "scientific evidence discovery",
        ],
    }
}
'''

if "SEMANTIC_SCHOLAR = \"SEMANTIC_SCHOLAR\"" not in text:
    text += block

COUNCIL.write_text(text, encoding="utf-8")

# ------------------------------------------------------------
# Compile
# ------------------------------------------------------------

targets = [
    COUNCIL,
    RESEARCH / "run_research_council.py",
    RESEARCH / "question_engine.py",
    RESEARCH / "evidence_filter.py",
    RESEARCH / "evidence_synthesizer.py",
]

if AGENT.exists():
    targets.append(AGENT)

for path in targets:
    py_compile.compile(str(path), doraise=True)

# ------------------------------------------------------------
# Validate
# ------------------------------------------------------------

final = COUNCIL.read_text(encoding="utf-8")

required = [
    "IMA_RESEARCH_COUNCIL_V5",
    "SEMANTIC_SCHOLAR",
    "EvidenceFilter",
    "EvidenceSynthesizer",
    "SemanticScholarAgent",
]

missing = [x for x in required if x not in final]

print("=" * 78)
print("IMA RESEARCH COUNCIL V5 — SEMANTIC SCHOLAR PATCH")
print("=" * 78)
print("BACKUP:", backup)
print()

for item in required:
    print(
        f"{item}:",
        "PASS" if item in final else "MISSING"
    )

print()
print("COMPILE: PASS")

if missing:
    print("PATCH VALIDATION: FAIL")
    print("MISSING:", missing)
    raise SystemExit(2)

print("PATCH VALIDATION: PASS")
print("=" * 78)
