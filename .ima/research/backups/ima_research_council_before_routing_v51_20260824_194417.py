from pathlib import Path
import json
import time
import uuid
import importlib.util
from concurrent.futures import ThreadPoolExecutor, as_completed

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



ROOT = Path.cwd()
RESEARCH = ROOT / ".ima/research"
STATE = RESEARCH / "state"
AGENTS = RESEARCH / "agents"
REGISTRY = RESEARCH / "agent_registry.json"

STATE.mkdir(parents=True, exist_ok=True)


class IMAResearchCouncil:

    def __init__(self, root=None, live_log=True):
        self.root = Path(root or ROOT).resolve()
        self.live_log = live_log

        self.registry = json.loads(
            REGISTRY.read_text(encoding="utf-8")
        )

    def log(self, message):
        if self.live_log:
            print(
                f"[{time.strftime('%H:%M:%S')}] {message}",
                flush=True
            )

    def _load(self, filename, classname):

        path = AGENTS / filename

        spec = importlib.util.spec_from_file_location(
            classname,
            path
        )

        module = importlib.util.module_from_spec(spec)
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

        if name == "MEDA":
            return cls(root=self.root)

        return cls()

    def _run_agent(
        self,
        agent_name,
        question,
        subquestion_id,
        previous_results
    ):

        started = time.time()

        self.log(
            f"START {agent_name} [{subquestion_id}]"
        )

        try:

            agent = self._agent(agent_name)

            if agent_name == "CRITIC":

                result = agent.investigate(
                    question,
                    previous_results
                )

            else:

                result = agent.investigate(
                    question
                )

            if not isinstance(result, dict):

                result = {
                    "agent": agent_name,
                    "status": "READY",
                    "answer": str(result)
                }

            result["agent"] = agent_name
            result["subquestion_id"] = subquestion_id
            result["duration"] = round(
                time.time() - started,
                3
            )

            self.log(
                f"DONE {agent_name} "
                f"[{subquestion_id}] "
                f"status={result.get('status')} "
                f"time={result['duration']}s"
            )

            return result

        except Exception as e:

            self.log(
                f"ERROR {agent_name} "
                f"[{subquestion_id}] "
                f"{repr(e)}"
            )

            return {
                "agent": agent_name,
                "subquestion_id": subquestion_id,
                "status": "EXCEPTION",
                "scientific_failure": False,
                "duration": round(
                    time.time() - started,
                    3
                ),
                "error": repr(e)
            }

    def _run_with_timeout(
        self,
        agent_name,
        question,
        subquestion_id,
        previous_results
    ):

        timeout = self.registry["agents"][
            agent_name
        ].get("timeout", 60)

        executor = ThreadPoolExecutor(
            max_workers=1
        )

        future = executor.submit(
            self._run_agent,
            agent_name,
            question,
            subquestion_id,
            previous_results
        )

        try:

            return future.result(
                timeout=timeout
            )

        except TimeoutError:

            self.log(
                f"TIMEOUT {agent_name} "
                f"[{subquestion_id}] "
                f"after {timeout}s "
                f"(not scientific failure)"
            )

            return {
                "agent": agent_name,
                "subquestion_id": subquestion_id,
                "timeout_limit": timeout,
                "status": "TIMEOUT",
                "scientific_failure": False,
                "duration": timeout,
                "error": (
                    f"Agent exceeded {timeout}s timeout."
                )
            }

        finally:

            executor.shutdown(
                wait=False,
                cancel_futures=True
            )

    def investigate(self, question):

        started = time.time()

        cycle_id = (
            time.strftime("%Y%m%d_%H%M%S")
            + "_"
            + uuid.uuid4().hex[:6]
        )

        self.log("=" * 78)
        self.log("IMA RESEARCH COUNCIL V4")
        self.log("=" * 78)

        self.log(
            f"QUESTION: {question}"
        )

        record = {
            "id": cycle_id,
            "original_question": question,
            "architecture": "IMA_RESEARCH_COUNCIL_V5",
            "status": "RUNNING",
            "agent_results": [],
            "subquestions": [],
            "disagreements": [],
            "open_questions": [],
            "next_research_questions": [],
            "events": []
        }

        # ====================================================
        # PHASE 1
        # ====================================================

        self.log(
            "PHASE 1/6 — QUESTION DECOMPOSITION"
        )

        from question_engine import QuestionEngine

        decomposition = QuestionEngine().decompose(
            question
        )

        record["subquestions"] = (
            decomposition["subquestions"]
        )

        for sub in record["subquestions"]:

            self.log(
                f"  SUBQUESTION {sub['id']} "
                f"→ {sub['question']}"
            )

        # ====================================================
        # PHASE 2
        # ====================================================

        self.log(
            "PHASE 2/6 — BUILDING RESEARCH JOBS"
        )

        jobs = []

        for sub in record["subquestions"]:

            for agent_name in sub["agents"]:

                cfg = self.registry[
                    "agents"
                ].get(agent_name)

                if not cfg:
                    continue

                if not cfg.get("enabled"):
                    continue

                jobs.append(
                    (
                        agent_name,
                        sub["question"],
                        sub["id"]
                    )
                )

        self.log(
            f"  {len(jobs)} research jobs queued"
        )

        # ====================================================
        # PHASE 3
        # ====================================================

        self.log(
            "PHASE 3/6 — PARALLEL AGENT EXECUTION"
        )

        previous_results = []

        with ThreadPoolExecutor(
            max_workers=max(
                1,
                len(jobs)
            )
        ) as pool:

            futures = {}

            for agent_name, q, sid in jobs:

                future = pool.submit(
                    self._run_with_timeout,
                    agent_name,
                    q,
                    sid,
                    previous_results
                )

                futures[future] = (
                    agent_name,
                    sid
                )

            for future in as_completed(
                futures
            ):

                agent_name, sid = (
                    futures[future]
                )

                try:

                    result = future.result()

                except Exception as e:

                    result = {
                        "agent": agent_name,
                        "subquestion_id": sid,
                        "status": "EXCEPTION",
                        "scientific_failure": False,
                        "error": repr(e)
                    }

                record[
                    "agent_results"
                ].append(result)

                previous_results.append(
                    result
                )

        # ====================================================
        # PHASE 4
        # ====================================================

        self.log(
            "PHASE 4/6 — EVIDENCE AGGREGATION"
        )

        successful = [
            r
            for r in record["agent_results"]
            if r.get("status")
            in [
                "ANSWER_READY",
                "READY"
            ]
        ]

        unavailable = [
            r
            for r in record["agent_results"]
            if r.get("status")
            in [
                "TIMEOUT",
                "CAPABILITY_PENDING",
                "EXCEPTION"
            ]
        ]

        record["evidence_map"] = {
            "successful_results": len(
                successful
            ),
            "failed_or_unavailable": len(
                unavailable
            ),
            "successful_agents": [
                r.get("agent")
                for r in successful
            ],
            "unavailable_agents": [
                r.get("agent")
                for r in unavailable
            ]
        }

        self.log(
            f"  successful={len(successful)} "
            f"unavailable={len(unavailable)}"
        )

        # ====================================================
        # PHASE 5
        # ====================================================

        self.log(
            "PHASE 5/6 — IMA SUPERVISION"
        )

        record[
            "disagreement_policy"
        ] = {
            "never_collapse_disagreement": True,
            "separate_evidence_from_inference": True,
            "preserve_competing_hypotheses": True
        }

        record[
            "open_questions"
        ] = [
            "What remains unresolved after independent research?",
            "Which claims require external evidence?",
            "Which claims are philosophical rather than empirically testable?"
        ]

        # ====================================================
        # PHASE 6
        # ====================================================

        self.log(
            "PHASE 6/6 — GENERATING NEXT RESEARCH QUESTIONS"
        )

        record[
            "next_research_questions"
        ] = [
            "Which conclusions are independently supported by multiple agents?",
            "Where do the agents disagree?",
            "Which hypothesis currently has the strongest evidence?",
            "Which hypothesis currently has the strongest counterevidence?",
            "What observation would distinguish the competing hypotheses?",
            "What important information is still missing?",
            "What new question should IMA ask next to reduce the greatest uncertainty?"
        ]

        for q in record[
            "next_research_questions"
        ]:

            self.log(
                f"  NEXT → {q}"
            )

        # ====================================================
        # FINALIZE
        # ====================================================

        record["duration"] = round(
            time.time() - started,
            3
        )

        record[
            "status"
        ] = "RESEARCH_CYCLE_COMPLETE"

        path = STATE / (
            cycle_id + ".json"
        )

        record[
            "result_file"
        ] = str(path)

        record[
            "ima_handoff"
        ] = {
            "ready": True,
            "original_question": question,
            "research_cycle": cycle_id,
            "agent_count": len(
                record["agent_results"]
            ),
            "successful_count": len(
                successful
            ),
            "unavailable_count": len(
                unavailable
            ),
            "next_questions": (
                record[
                    "next_research_questions"
                ]
            ),
            "instruction": (
                "IMA must synthesize evidence, "
                "preserve disagreement, distinguish "
                "fact from inference, and generate "
                "new questions when uncertainty remains."
            )
        }

        path.write_text(
            json.dumps(
                record,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        self.log("=" * 78)

        self.log(
            f"CYCLE COMPLETE "
            f"in {record['duration']}s"
        )

        self.log(
            f"RESULT → {path}"
        )

        self.log("=" * 78)

        return record


def investigate(question, root=None):

    return IMAResearchCouncil(
        root=root,
        live_log=True
    ).investigate(question)


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
