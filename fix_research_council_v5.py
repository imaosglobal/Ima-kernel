from pathlib import Path
from datetime import datetime
import shutil
import py_compile

ROOT = Path.cwd()
RESEARCH = ROOT / ".ima" / "research"
COUNCIL = RESEARCH / "ima_research_council.py"
AGENTS = RESEARCH / "agents"

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

if not COUNCIL.exists():
    raise SystemExit(f"ERROR: {COUNCIL} not found")

# ------------------------------------------------------------
# BACKUP
# ------------------------------------------------------------

backup_dir = RESEARCH / "backups"
backup_dir.mkdir(parents=True, exist_ok=True)

backup = backup_dir / f"ima_research_council_before_v5_{stamp}.py"
shutil.copy2(COUNCIL, backup)

text = COUNCIL.read_text(encoding="utf-8")

# ------------------------------------------------------------
# V4 -> V5
# ------------------------------------------------------------

old_count = text.count("IMA_RESEARCH_COUNCIL_V4")

text = text.replace(
    "IMA_RESEARCH_COUNCIL_V4",
    "IMA_RESEARCH_COUNCIL_V5"
)

# ------------------------------------------------------------
# Evidence Filter
# ------------------------------------------------------------

FILTER = RESEARCH / "evidence_filter.py"

FILTER.write_text(
r'''from typing import Any


class EvidenceFilter:

    name = "EVIDENCE_FILTER"

    def filter_sources(self, sources: list[dict[str, Any]]) -> dict[str, Any]:

        accepted = []
        rejected = []

        for source in sources or []:

            title = str(
                source.get("title", "")
            ).strip()

            if not title:
                rejected.append({
                    "source": source,
                    "reason": "missing_title",
                })
                continue

            source_type = str(
                source.get("type", "")
            ).lower()

            metadata_only = source_type in {
                "dataset",
                "book",
                "book-chapter",
                "posted-content",
                "reference-entry",
            }

            item = dict(source)

            item["metadata_only"] = metadata_only

            item["evidence_status"] = (
                "BIBLIOGRAPHIC_ONLY"
                if metadata_only
                else "CANDIDATE_EVIDENCE"
            )

            accepted.append(item)

        return {
            "accepted": accepted,
            "rejected": rejected,
            "accepted_count": len(accepted),
            "rejected_count": len(rejected),
        }
''',
encoding="utf-8"
)

# ------------------------------------------------------------
# Evidence Synthesizer
# ------------------------------------------------------------

SYNTH = RESEARCH / "evidence_synthesizer.py"

SYNTH.write_text(
r'''from collections import Counter


class EvidenceSynthesizer:

    name = "EVIDENCE_SYNTHESIZER"

    def synthesize(self, agent_results):

        successful = []
        unavailable = []
        statuses = Counter()

        for result in agent_results or []:

            status = result.get(
                "status",
                "UNKNOWN"
            )

            statuses[status] += 1

            if status in {
                "ANSWER_READY",
                "READY",
                "COMPLETE",
                "SUCCESS",
            }:
                successful.append(result)

            else:
                unavailable.append(result)

        return {
            "successful_results": len(successful),
            "failed_or_unavailable": len(unavailable),
            "status_counts": dict(statuses),
            "successful_agents": [
                r.get("agent")
                for r in successful
            ],
            "unavailable_agents": [
                r.get("agent")
                for r in unavailable
            ],
            "disagreement_policy": {
                "never_collapse_disagreement": True,
                "separate_evidence_from_inference": True,
                "preserve_competing_hypotheses": True,
            },
        }
''',
encoding="utf-8"
)

# ------------------------------------------------------------
# V5 imports / capabilities
# ------------------------------------------------------------

marker = """
# ============================================================
# IMA RESEARCH COUNCIL V5
# ============================================================

IMA_RESEARCH_COUNCIL_VERSION = "V5"
IMA_RESEARCH_COUNCIL_ARCHITECTURE = "IMA_RESEARCH_COUNCIL_V5"

try:
    from evidence_filter import EvidenceFilter
except Exception:
    EvidenceFilter = None

try:
    from evidence_synthesizer import EvidenceSynthesizer
except Exception:
    EvidenceSynthesizer = None

try:
    from agents.semantic_scholar_agent import SemanticScholarAgent
except Exception:
    SemanticScholarAgent = None

V5_ARCHITECTURE_FEATURES = [
    "parallel_agent_execution",
    "independent_timeouts",
    "evidence_filtering",
    "evidence_classification",
    "cross_agent_comparison",
    "disagreement_preservation",
    "next_question_generation",
    "automatic_agent_discovery",
    "semantic_scholar_literature",
]
"""

if "IMA_RESEARCH_COUNCIL_VERSION = \"V5\"" not in text:

    lines = text.splitlines(True)

    insert_at = 0

    for i, line in enumerate(lines):

        if line.startswith("import ") or line.startswith("from "):
            insert_at = i + 1

    lines.insert(
        insert_at,
        marker + "\n"
    )

    text = "".join(lines)

# ------------------------------------------------------------
# Write engine
# ------------------------------------------------------------

COUNCIL.write_text(
    text,
    encoding="utf-8"
)

# ------------------------------------------------------------
# Compile everything
# ------------------------------------------------------------

targets = [
    COUNCIL,
    FILTER,
    SYNTH,
]

S2 = AGENTS / "semantic_scholar_agent.py"

if S2.exists():
    targets.append(S2)

for path in targets:
    py_compile.compile(
        str(path),
        doraise=True
    )

# ------------------------------------------------------------
# Validation
# ------------------------------------------------------------

final = COUNCIL.read_text(
    encoding="utf-8"
)

required = [
    "IMA_RESEARCH_COUNCIL_V5",
    "SEMANTIC_SCHOLAR",
    "EvidenceFilter",
    "EvidenceSynthesizer",
]

missing = [
    x for x in required
    if x not in final
]

print("=" * 78)
print("IMA RESEARCH COUNCIL V5 ACTIVE ENGINE PATCH")
print("=" * 78)
print("BACKUP:", backup)
print("OLD V4 MARKERS REPLACED:", old_count)
print()

for item in required:

    print(
        f"{item}:",
        "PASS" if item in final
        else "MISSING"
    )

print()
print("COMPILE: PASS")

if missing:

    print("PATCH VALIDATION: FAIL")
    print("MISSING:", missing)
    raise SystemExit(2)

print("PATCH VALIDATION: PASS")
print("=" * 78)
