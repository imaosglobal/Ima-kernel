
from pathlib import Path
import json
import time
import traceback


class IMAResearchSupervisor:

    name = "IMA Research Supervisor"

    def __init__(self, root=None):
        self.root = Path(
            root or Path.cwd()
        ).resolve()

        self.state_dir = (
            self.root /
            ".ima/research/state"
        )

        self.state_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.registry = (
            self.root /
            ".ima/research/research_agents.json"
        )

    def _load_registry(self):

        if not self.registry.exists():
            return {}

        return json.loads(
            self.registry.read_text(
                encoding="utf-8"
            )
        )

    def _save(self, name, data):

        path = (
            self.state_dir /
            f"{name}.json"
        )

        path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8"
        )

    def _classify(self, question):

        q = question.lower()

        foundational = any(
            x in q
            for x in [
                "יקום",
                "אינטליג",
                "תודעה",
                "קיום",
                "למה יש",
                "מציאות",
                "consciousness",
                "universe",
                "intelligence",
                "existence",
            ]
        )

        if foundational:
            return "foundational"

        return "general"

    def _plan(self, question):

        kind = self._classify(question)

        if kind == "foundational":

            return {
                "research_type": "foundational",
                "required_axes": [
                    "empirical",
                    "logical",
                    "philosophical",
                    "unknowns",
                    "counterarguments",
                    "testable_predictions",
                ],
                "agents": [
                    "MEDA",
                    "literature",
                    "hypothesis",
                    "critic",
                ]
            }

        return {
            "research_type": "general",
            "required_axes": [
                "evidence",
                "hypotheses",
                "testing",
                "uncertainty",
            ],
            "agents": [
                "MEDA",
                "literature",
                "critic",
            ]
        }

    def _judge(self, results):

        ready = [
            r for r in results
            if r.get("status") == "ANSWER_READY"
        ]

        timeouts = [
            r for r in results
            if r.get("status") == "TIMEOUT"
        ]

        failures = [
            r for r in results
            if r.get("status") in [
                "FAILED",
                "BLOCKED",
            ]
        ]

        if ready:
            status = "PARTIAL"
        elif timeouts:
            status = "NEEDS_MORE_RESEARCH"
        else:
            status = "NO_ANSWER"

        return {
            "status": status,
            "successful_agents": len(ready),
            "timeouts": len(timeouts),
            "failures": len(failures),
            "agreement": None,
            "confidence": 0.0,
            "conflicts": [],
            "missing_evidence": [],
        }

    def investigate(self, question):

        started = time.time()

        plan = self._plan(question)

        record = {
            "id": time.strftime(
                "%Y%m%d_%H%M%S"
            ),
            "question": question,
            "original_question": question,
            "plan": plan,
            "agent_results": [],
            "judgement": None,
            "next_actions": [],
            "created_at": time.strftime(
                "%Y-%m-%dT%H:%M:%S"
            ),
        }

        # ----------------------------------------------------
        # MEDA
        # ----------------------------------------------------

        try:

            from meda_adapter import MEDAAdapter

            meda = MEDAAdapter(
                root=self.root,
                timeout=180,
            )

            meda_result = meda.investigate(
                question
            )

            record["agent_results"].append(
                meda_result
            )

        except Exception:

            record["agent_results"].append({
                "status": "FAILED",
                "agent": "MEDA",
                "question": question,
                "error": traceback.format_exc(),
            })

        # ----------------------------------------------------
        # Supervisor judgement
        # ----------------------------------------------------

        record["judgement"] = self._judge(
            record["agent_results"]
        )

        if record["judgement"]["status"] == "NEEDS_MORE_RESEARCH":

            record["next_actions"] = [
                "Do not treat MEDA timeout as scientific failure.",
                "Run literature research.",
                "Generate competing hypotheses.",
                "Run independent critic.",
                "Compare independent results.",
                "Return synthesis to IMA.",
            ]

        elif record["judgement"]["status"] == "PARTIAL":

            record["next_actions"] = [
                "Validate MEDA result independently.",
                "Search for contradictory evidence.",
                "Generate competing explanations.",
                "Estimate uncertainty.",
                "Produce synthesis.",
            ]

        else:

            record["next_actions"] = [
                "Select another research agent.",
                "Diagnose missing capability.",
            ]

        record["duration"] = round(
            time.time() - started,
            3
        )

        self._save(
            record["id"],
            record
        )

        return record


def investigate(question, root=None):

    supervisor = IMAResearchSupervisor(
        root=root
    )

    return supervisor.investigate(
        question
    )


if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:
        print(
            "Usage: python3 ima_research_supervisor.py "
            "\"question\""
        )
        raise SystemExit(2)

    result = investigate(
        sys.argv[1]
    )

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        )
    )
