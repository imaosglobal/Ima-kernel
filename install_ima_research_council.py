from pathlib import Path
import json
import textwrap

ROOT = Path.cwd()

RESEARCH = ROOT / ".ima/research"
STATE = RESEARCH / "state"
AGENTS = RESEARCH / "agents"

RESEARCH.mkdir(parents=True, exist_ok=True)
STATE.mkdir(parents=True, exist_ok=True)
AGENTS.mkdir(parents=True, exist_ok=True)


# ============================================================
# 1. AGENT REGISTRY
# ============================================================

registry = {
    "version": "2.0",
    "architecture": "IMA_RESEARCH_COUNCIL",
    "auto_discovery": True,
    "agents": {
        "MEDA": {
            "enabled": True,
            "type": "local",
            "adapter": "meda_agent.py",
            "timeout": 30,
            "roles": [
                "constraint reasoning",
                "dynamical models",
                "model comparison",
                "scientific formalization"
            ]
        },

        "DEEP_RESEARCH": {
            "enabled": True,
            "type": "external_capability",
            "adapter": "deep_research_agent.py",
            "timeout": 120,
            "roles": [
                "broad research",
                "source discovery",
                "evidence synthesis",
                "current knowledge"
            ]
        },

        "LITERATURE": {
            "enabled": True,
            "type": "external_capability",
            "adapter": "literature_agent.py",
            "timeout": 120,
            "roles": [
                "scientific papers",
                "evidence retrieval",
                "contradictory evidence",
                "citations"
            ]
        },

        "HYPOTHESIS": {
            "enabled": True,
            "type": "local_reasoning",
            "adapter": "hypothesis_agent.py",
            "timeout": 30,
            "roles": [
                "hypothesis generation",
                "alternative explanations",
                "hypothesis comparison"
            ]
        },

        "CRITIC": {
            "enabled": True,
            "type": "local_reasoning",
            "adapter": "critic_agent.py",
            "timeout": 30,
            "roles": [
                "counterarguments",
                "falsification",
                "logical criticism",
                "uncertainty"
            ]
        },

        "EVOLUTIONARY_SEARCH": {
            "enabled": True,
            "type": "local_reasoning",
            "adapter": "evolutionary_agent.py",
            "timeout": 60,
            "roles": [
                "algorithmic search",
                "optimization",
                "candidate generation"
            ]
        }
    }
}

(RESEARCH / "agent_registry.json").write_text(
    json.dumps(registry, ensure_ascii=False, indent=2),
    encoding="utf-8"
)


# ============================================================
# 2. QUESTION DECOMPOSER
# ============================================================

question_engine = r'''
from pathlib import Path
import json


class QuestionEngine:

    def decompose(self, question):

        return {
            "primary_question": question,

            "subquestions": [
                {
                    "id": "empirical",
                    "question": (
                        "What observations or measurements can "
                        "actually bear on the question?"
                    ),
                    "agents": [
                        "DEEP_RESEARCH",
                        "LITERATURE"
                    ]
                },

                {
                    "id": "mechanism",
                    "question": (
                        "What mechanisms could explain the "
                        "observed phenomenon without assuming "
                        "the conclusion?"
                    ),
                    "agents": [
                        "MEDA",
                        "HYPOTHESIS"
                    ]
                },

                {
                    "id": "alternatives",
                    "question": (
                        "What competing explanations exist?"
                    ),
                    "agents": [
                        "HYPOTHESIS",
                        "DEEP_RESEARCH"
                    ]
                },

                {
                    "id": "criticism",
                    "question": (
                        "What are the strongest arguments against "
                        "each proposed explanation?"
                    ),
                    "agents": [
                        "CRITIC"
                    ]
                },

                {
                    "id": "testability",
                    "question": (
                        "What observations or experiments could "
                        "distinguish the competing hypotheses?"
                    ),
                    "agents": [
                        "MEDA",
                        "LITERATURE",
                        "CRITIC"
                    ]
                },

                {
                    "id": "unknowns",
                    "question": (
                        "What remains genuinely unknown?"
                    ),
                    "agents": [
                        "CRITIC",
                        "LITERATURE"
                    ]
                }
            ]
        }
'''


(RESEARCH / "question_engine.py").write_text(
    question_engine,
    encoding="utf-8"
)


# ============================================================
# 3. MEDA ADAPTER
# ============================================================

meda_agent = r'''
from pathlib import Path
import subprocess
import sys
import json
import time
import uuid


class MEDAAgent:

    name = "MEDA"

    def __init__(self, root=None, timeout=30):

        self.root = Path(root or Path.cwd()).resolve()
        self.timeout = timeout

        self.meda = (
            self.root /
            "external/MEDA"
        )

        self.main = (
            self.meda /
            "skills/meda/scripts/main.py"
        )

        self.session = (
            self.meda /
            "sessions/ima_universe_intelligence"
        )

    def investigate(self, question):

        setup = self.session / "setup.yaml"
        problem = self.session / "problem.json"

        output = (
            self.session /
            f"council_{uuid.uuid4().hex[:8]}.json"
        )

        started = time.time()

        try:

            p = subprocess.run(
                [
                    sys.executable,
                    str(self.main),
                    "--mode",
                    "constraint_only",
                    "--setup",
                    str(setup),
                    "--problem",
                    str(problem),
                    "--output",
                    str(output),
                ],
                cwd=str(self.meda),
                text=True,
                capture_output=True,
                timeout=self.timeout
            )

            duration = round(
                time.time() - started,
                3
            )

            if p.returncode == 0 and output.exists():

                try:
                    data = json.loads(
                        output.read_text(
                            encoding="utf-8"
                        )
                    )

                    return {
                        "agent": self.name,
                        "status": "ANSWER_READY",
                        "duration": duration,
                        "answer": data
                    }

                except Exception as e:

                    return {
                        "agent": self.name,
                        "status": "INVALID_OUTPUT",
                        "duration": duration,
                        "error": repr(e)
                    }

            return {
                "agent": self.name,
                "status": "FAILED",
                "duration": duration,
                "returncode": p.returncode,
                "stderr": p.stderr[-10000:]
            }

        except subprocess.TimeoutExpired:

            return {
                "agent": self.name,
                "status": "TIMEOUT",
                "duration": round(
                    time.time() - started,
                    3
                ),
                "scientific_failure": False,
                "meaning": (
                    "Execution timeout only. "
                    "Not a scientific conclusion."
                )
            }

        except Exception as e:

            return {
                "agent": self.name,
                "status": "EXCEPTION",
                "duration": round(
                    time.time() - started,
                    3
                ),
                "error": repr(e)
            }
'''


(AGENTS / "meda_agent.py").write_text(
    meda_agent,
    encoding="utf-8"
)


# ============================================================
# 4. LOCAL HYPOTHESIS ENGINE
# ============================================================

hypothesis_agent = r'''
class HypothesisAgent:

    name = "HYPOTHESIS"

    def investigate(self, question):

        return {
            "agent": self.name,
            "status": "READY",
            "question": question,
            "instruction": (
                "Generate multiple competing hypotheses "
                "without selecting one prematurely."
            )
        }
'''


(AGENTS / "hypothesis_agent.py").write_text(
    hypothesis_agent,
    encoding="utf-8"
)


# ============================================================
# 5. CRITIC
# ============================================================

critic_agent = r'''
class CriticAgent:

    name = "CRITIC"

    def investigate(self, question, evidence=None):

        return {
            "agent": self.name,
            "status": "READY",
            "question": question,
            "instruction": (
                "Search for contradictions, hidden assumptions, "
                "alternative explanations, and falsification tests."
            ),
            "evidence_received": bool(evidence)
        }
'''


(AGENTS / "critic_agent.py").write_text(
    critic_agent,
    encoding="utf-8"
)


# ============================================================
# 6. EXTERNAL RESEARCH CAPABILITY CONTRACTS
# ============================================================

deep_research_agent = r'''
class DeepResearchAgent:

    name = "DEEP_RESEARCH"

    def investigate(self, question):

        return {
            "agent": self.name,
            "status": "CAPABILITY_PENDING",
            "question": question,
            "requires": [
                "connected deep-research provider"
            ],
            "contract": (
                "Return sourced research, competing evidence, "
                "uncertainty and citations."
            )
        }
'''


(AGENTS / "deep_research_agent.py").write_text(
    deep_research_agent,
    encoding="utf-8"
)


literature_agent = r'''
class LiteratureAgent:

    name = "LITERATURE"

    def investigate(self, question):

        return {
            "agent": self.name,
            "status": "CAPABILITY_PENDING",
            "question": question,
            "requires": [
                "literature/search provider"
            ],
            "contract": (
                "Return scientific papers, evidence, "
                "contradictions and source metadata."
            )
        }
'''


(AGENTS / "literature_agent.py").write_text(
    literature_agent,
    encoding="utf-8"
)


evolutionary_agent = r'''
class EvolutionaryAgent:

    name = "EVOLUTIONARY_SEARCH"

    def investigate(self, question):

        return {
            "agent": self.name,
            "status": "READY",
            "question": question,
            "instruction": (
                "Search candidate explanations or models "
                "algorithmically."
            )
        }
'''


(AGENTS / "evolutionary_agent.py").write_text(
    evolutionary_agent,
    encoding="utf-8"
)


# ============================================================
# 7. MAIN COUNCIL
# ============================================================

council = r'''
from pathlib import Path
import json
import time
import uuid
import importlib.util


ROOT = Path.cwd()
RESEARCH = ROOT / ".ima/research"
STATE = RESEARCH / "state"
AGENTS = RESEARCH / "agents"

REGISTRY = RESEARCH / "agent_registry.json"


class IMAResearchCouncil:

    def __init__(self, root=None):

        self.root = Path(
            root or ROOT
        ).resolve()

        self.registry = json.loads(
            REGISTRY.read_text(
                encoding="utf-8"
            )
        )

    def _load(self, filename, classname):

        path = AGENTS / filename

        spec = importlib.util.spec_from_file_location(
            classname,
            path
        )

        module = importlib.util.module_from_spec(
            spec
        )

        spec.loader.exec_module(module)

        return getattr(module, classname)

    def _agent(self, name):

        cfg = self.registry["agents"][name]

        adapter = cfg["adapter"]

        mapping = {
            "meda_agent.py": "MEDAAgent",
            "hypothesis_agent.py": "HypothesisAgent",
            "critic_agent.py": "CriticAgent",
            "deep_research_agent.py": "DeepResearchAgent",
            "literature_agent.py": "LiteratureAgent",
            "evolutionary_agent.py": "EvolutionaryAgent"
        }

        cls = self._load(
            adapter,
            mapping[adapter]
        )

        return cls(
            root=self.root
        ) if name == "MEDA" else cls()

    def investigate(self, question):

        started = time.time()

        record = {
            "id": (
                time.strftime("%Y%m%d_%H%M%S")
                + "_"
                + uuid.uuid4().hex[:6]
            ),

            "original_question": question,

            "architecture": (
                "IMA_RESEARCH_COUNCIL"
            ),

            "agent_results": [],

            "subquestions": [],

            "disagreements": [],

            "open_questions": [],

            "next_research_questions": []
        }

        # ----------------------------------------------------
        # DECOMPOSITION
        # ----------------------------------------------------

        from question_engine import QuestionEngine

        decomposition = QuestionEngine().decompose(
            question
        )

        record["subquestions"] = (
            decomposition["subquestions"]
        )

        # ----------------------------------------------------
        # PARALLEL-ROLE RESEARCH
        # ----------------------------------------------------

        for sub in record["subquestions"]:

            subquestion = sub["question"]

            for agent_name in sub["agents"]:

                cfg = self.registry["agents"].get(
                    agent_name
                )

                if not cfg or not cfg.get("enabled"):
                    continue

                try:

                    agent = self._agent(
                        agent_name
                    )

                    if agent_name == "CRITIC":

                        result = agent.investigate(
                            subquestion,
                            record["agent_results"]
                        )

                    else:

                        result = agent.investigate(
                            subquestion
                        )

                    result["subquestion_id"] = (
                        sub["id"]
                    )

                    record["agent_results"].append(
                        result
                    )

                except Exception as e:

                    record["agent_results"].append({
                        "agent": agent_name,
                        "status": "EXCEPTION",
                        "subquestion_id": sub["id"],
                        "error": repr(e)
                    })

        # ----------------------------------------------------
        # CROSS-CHECK
        # ----------------------------------------------------

        successful = [
            r for r in record["agent_results"]
            if r.get("status")
            in [
                "ANSWER_READY",
                "READY"
            ]
        ]

        timed_out = [
            r for r in record["agent_results"]
            if r.get("status") == "TIMEOUT"
        ]

        record["cross_check"] = {
            "successful_agents": [
                r.get("agent")
                for r in successful
            ],
            "timeouts": [
                r.get("agent")
                for r in timed_out
            ],
            "timeout_is_not_scientific_failure": True
        }

        # ----------------------------------------------------
        # GENERATE NEXT QUESTIONS
        # ----------------------------------------------------

        record["next_research_questions"] = [
            (
                "Which conclusion is independently supported "
                "by more than one research method?"
            ),
            (
                "Which hypothesis currently has the strongest "
                "evidence against it?"
            ),
            (
                "What observation would most strongly "
                "distinguish the remaining hypotheses?"
            ),
            (
                "Which unanswered question has the highest "
                "information value?"
            )
        ]

        record["duration"] = round(
            time.time() - started,
            3
        )

        record["status"] = (
            "RESEARCH_CYCLE_COMPLETE"
        )

        path = STATE / (
            record["id"] + ".json"
        )

        path.write_text(
            json.dumps(
                record,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        record["result_file"] = str(path)

        return record
'''


(RESEARCH / "ima_research_council.py").write_text(
    council,
    encoding="utf-8"
)


# ============================================================
# 8. RUNNER
# ============================================================

runner = r'''
import sys
import json

from ima_research_council import (
    IMAResearchCouncil
)


if len(sys.argv) < 2:

    print(
        'Usage: python3 run_research_council.py "question"'
    )

    raise SystemExit(2)


question = sys.argv[1]

council = IMAResearchCouncil()

result = council.investigate(
    question
)

print("=" * 78)
print("IMA RESEARCH COUNCIL")
print("=" * 78)

print(
    json.dumps(
        result,
        ensure_ascii=False,
        indent=2
    )
)
'''


(RESEARCH / "run_research_council.py").write_text(
    runner,
    encoding="utf-8"
)


# ============================================================
# 9. IMA HANDOFF CONTRACT
# ============================================================

handoff = {
    "version": "1.0",
    "direction": "RESEARCH_COUNCIL -> IMA",
    "return": [
        "answer",
        "evidence",
        "uncertainty",
        "disagreements",
        "open_questions",
        "next_research_questions"
    ],
    "principles": [
        "Never treat agent timeout as scientific evidence.",
        "Never collapse disagreement into false consensus.",
        "Preserve competing hypotheses.",
        "Separate evidence from inference.",
        "Generate new questions when evidence is insufficient.",
        "Allow new research agents to be discovered and registered."
    ]
}

(RESEARCH / "ima_handoff_contract.json").write_text(
    json.dumps(
        handoff,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)


# ============================================================
# 10. COMPILE EVERYTHING
# ============================================================

targets = [
    RESEARCH / "question_engine.py",
    RESEARCH / "ima_research_council.py",
    RESEARCH / "run_research_council.py",
    *AGENTS.glob("*.py")
]

import py_compile

for path in targets:
    py_compile.compile(
        str(path),
        doraise=True
    )

print("=" * 78)
print("IMA RESEARCH COUNCIL INSTALLED")
print("=" * 78)
print()
print("Registry :", RESEARCH / "agent_registry.json")
print("Council  :", RESEARCH / "ima_research_council.py")
print("Runner   :", RESEARCH / "run_research_council.py")
print("Handoff  :", RESEARCH / "ima_handoff_contract.json")
print()
print("Agents:")
for name, cfg in registry["agents"].items():
    print(
        " -",
        name,
        "| enabled=",
        cfg["enabled"],
        "|",
        cfg["type"]
    )

print()
print("COMPILE: PASS")
