from pathlib import Path
import json
import shutil
import time
import py_compile

ROOT = Path.cwd()
RESEARCH = ROOT / ".ima/research"
AGENTS = RESEARCH / "agents"
BACKUPS = RESEARCH / "backups"

BACKUPS.mkdir(parents=True, exist_ok=True)

def backup(path):
    if path.exists():
        dst = BACKUPS / f"{path.name}.{time.strftime('%Y%m%d_%H%M%S')}.bak"
        shutil.copy2(path, dst)
        return str(dst)
    return None

# ============================================================
# 1. SEMANTIC SCHOLAR AGENT
# ============================================================

S2 = AGENTS / "semantic_scholar_agent.py"
s2_backup = backup(S2)

S2.write_text(r'''
import json
import urllib.parse
import urllib.request
import urllib.error


class SemanticScholarAgent:

    name = "SEMANTIC_SCHOLAR"

    def investigate(self, question):

        base = "https://api.semanticscholar.org/graph/v1/paper/search"

        params = urllib.parse.urlencode({
            "query": question,
            "limit": 10,
            "fields": (
                "title,abstract,year,authors,url,"
                "citationCount,venue,publicationTypes"
            ),
        })

        url = base + "?" + params

        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "IMA-Research-Council/5.0"
                },
            )

            with urllib.request.urlopen(req, timeout=20) as response:
                payload = json.loads(
                    response.read().decode("utf-8")
                )

            papers = []

            for item in payload.get("data", []):
                papers.append({
                    "title": item.get("title"),
                    "abstract": item.get("abstract"),
                    "year": item.get("year"),
                    "authors": [
                        a.get("name")
                        for a in item.get("authors", [])
                    ],
                    "url": item.get("url"),
                    "citation_count": item.get(
                        "citationCount"
                    ),
                    "venue": item.get("venue"),
                    "publication_types": item.get(
                        "publicationTypes"
                    ),
                })

            return {
                "agent": self.name,
                "status": "ANSWER_READY",
                "question": question,
                "provider": "Semantic Scholar",
                "papers": papers,
                "count": len(papers),
                "evidence_type": [
                    "scientific literature",
                    "bibliographic metadata",
                ],
                "limitations": [
                    "Search relevance is not proof of truth.",
                    "Citation count is not evidence quality.",
                    "Individual papers require independent evaluation.",
                ],
            }

        except Exception as e:

            return {
                "agent": self.name,
                "status": "ERROR",
                "question": question,
                "provider": "Semantic Scholar",
                "error": repr(e),
            }
''',
encoding="utf-8"
)

# ============================================================
# 2. EVIDENCE FILTER
# ============================================================

FILTER = RESEARCH / "evidence_filter.py"

FILTER.write_text(r'''
import re


class EvidenceFilter:

    def __init__(self, minimum_score=0.20):
        self.minimum_score = minimum_score

    def score(self, question, item):

        q = set(
            re.findall(
                r"\w+",
                question.lower()
            )
        )

        text = " ".join([
            str(item.get("title") or ""),
            str(item.get("abstract") or ""),
        ]).lower()

        words = set(
            re.findall(r"\w+", text)
        )

        if not q:
            return 0.0

        overlap = len(q & words) / len(q)

        title = str(
            item.get("title") or ""
        ).lower()

        title_bonus = 0.20 if any(
            w in title for w in q
        ) else 0.0

        return min(
            1.0,
            overlap + title_bonus
        )

    def filter(self, question, items):

        accepted = []
        rejected = []

        for item in items:

            score = self.score(
                question,
                item
            )

            item = dict(item)
            item["relevance_score"] = round(
                score,
                4
            )

            if score >= self.minimum_score:
                item["evidence_class"] = (
                    "RELEVANT_CANDIDATE"
                )
                accepted.append(item)
            else:
                item["evidence_class"] = (
                    "LOW_RELEVANCE"
                )
                rejected.append(item)

        accepted.sort(
            key=lambda x:
            x.get("relevance_score", 0),
            reverse=True
        )

        return {
            "accepted": accepted,
            "rejected": rejected,
        }
''',
encoding="utf-8"
)

# ============================================================
# 3. SYNTHESIS ENGINE
# ============================================================

SYNTH = RESEARCH / "evidence_synthesis.py"

SYNTH.write_text(r'''
class EvidenceSynthesis:

    def synthesize(self, agent_results):

        successful = []
        unavailable = []
        sources = []

        for result in agent_results:

            status = result.get("status")

            if status in (
                "ANSWER_READY",
                "READY"
            ):
                successful.append(result)

            elif status in (
                "TIMEOUT",
                "CAPABILITY_PENDING",
                "ERROR",
                "EXCEPTION"
            ):
                unavailable.append(result)

            for paper in result.get(
                "papers", []
            ):
                sources.append(paper)

            for paper in result.get(
                "results", []
            ):
                sources.append(paper)

        return {
            "successful_results": len(
                successful
            ),
            "unavailable_results": len(
                unavailable
            ),
            "source_count": len(sources),
            "sources": sources,
            "principles": [
                "A retrieved source is not automatically evidence.",
                "Relevance does not establish truth.",
                "Citation count does not establish correctness.",
                "Separate empirical evidence from interpretation.",
                "Preserve competing hypotheses.",
                "Preserve unresolved disagreement.",
            ],
        }
''',
encoding="utf-8"
)

# ============================================================
# 4. REGISTRY
# ============================================================

REGISTRY = RESEARCH / "agent_registry.json"
registry_backup = backup(REGISTRY)

registry = json.loads(
    REGISTRY.read_text(
        encoding="utf-8"
    )
)

registry["version"] = "5.0"
registry["architecture"] = (
    "IMA_RESEARCH_COUNCIL_V5"
)

registry["agents"]["SEMANTIC_SCHOLAR"] = {
    "enabled": True,
    "type": "external_capability",
    "adapter": "semantic_scholar_agent.py",
    "timeout": 30,
    "roles": [
        "relevance-ranked literature",
        "abstract retrieval",
        "citation metadata",
        "scientific evidence discovery",
    ],
}

registry["architecture_features"] = [
    "parallel_agent_execution",
    "independent_timeouts",
    "evidence_filtering",
    "evidence_classification",
    "cross_agent_comparison",
    "disagreement_preservation",
    "next_question_generation",
    "automatic_agent_discovery",
]

REGISTRY.write_text(
    json.dumps(
        registry,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)

# ============================================================
# 5. COMPILE
# ============================================================

targets = [
    S2,
    FILTER,
    SYNTH,
    RESEARCH / "ima_research_council.py",
    RESEARCH / "run_research_council.py",
    RESEARCH / "question_engine.py",
]

targets.extend(
    AGENTS.glob("*.py")
)

for path in targets:
    py_compile.compile(
        str(path),
        doraise=True
    )

print("=" * 78)
print("IMA RESEARCH COUNCIL V5 INSTALLED")
print("=" * 78)
print("BACKUP REGISTRY:", registry_backup)
print("BACKUP S2:", s2_backup)
print()
print("SEMANTIC SCHOLAR: ENABLED")
print("EVIDENCE FILTER: ENABLED")
print("EVIDENCE SYNTHESIS: ENABLED")
print("PARALLEL EXECUTION: ENABLED")
print("INDEPENDENT TIMEOUTS: ENABLED")
print("DISAGREEMENT PRESERVATION: ENABLED")
print("NEXT QUESTION GENERATION: ENABLED")
print()
print("COMPILE: PASS")
print("=" * 78)
