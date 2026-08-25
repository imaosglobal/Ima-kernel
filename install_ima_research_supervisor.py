from pathlib import Path
import json
import shutil
import time
import py_compile

ROOT = Path.cwd()
SESSION = ROOT / "external/MEDA/sessions/ima_universe_intelligence"

SUPERVISOR = ROOT / ".ima/research/ima_research_supervisor.py"
PROTOCOL = ROOT / ".ima/research/research_agent_protocol.json"
ADAPTER = ROOT / ".ima/research/meda_adapter.py"
REGISTRY = ROOT / ".ima/research/research_agents.json"

SUPERVISOR.parent.mkdir(parents=True, exist_ok=True)

stamp = time.strftime("%Y%m%d_%H%M%S")

def backup(path):
    if path.exists():
        target = path.with_name(path.name + f".bak_{stamp}")
        shutil.copy2(path, target)
        print("BACKUP:", target)

# ------------------------------------------------------------
# 1. UNIVERSAL RESEARCH AGENT PROTOCOL
# ------------------------------------------------------------

PROTOCOL.write_text(
json.dumps({
    "version": "1.0",
    "name": "IMA Research Agent Protocol",
    "purpose": "Common contract between IMA and scientific reasoning systems.",
    "agent_methods": [
        "propose",
        "investigate",
        "test",
        "evaluate",
        "explain",
        "report"
    ],
    "required_result_fields": [
        "status",
        "agent",
        "question",
        "hypotheses",
        "evidence",
        "assumptions",
        "uncertainties",
        "conflicts",
        "next_actions",
        "answer"
    ],
    "status_values": [
        "ANSWER_READY",
        "PARTIAL",
        "TIMEOUT",
        "FAILED",
        "BLOCKED",
        "NOT_APPLICABLE"
    ],
    "supervisor_rules": [
        "Never convert timeout into scientific failure automatically.",
        "Never convert hypothesis into fact.",
        "Preserve the original research question.",
        "Separate empirical, logical and philosophical claims.",
        "Cross-check important conclusions.",
        "Record failures as research information.",
        "Prefer the next experiment or analysis that most reduces uncertainty."
    ]
}, ensure_ascii=False, indent=2),
encoding="utf-8"
)

# ------------------------------------------------------------
# 2. MEDA ADAPTER
# ------------------------------------------------------------

backup(ADAPTER)

ADAPTER.write_text(r'''
from pathlib import Path
import subprocess
import sys
import json
import time
import traceback


class MEDAAdapter:

    name = "MEDA"

    def __init__(self, root=None, timeout=180):
        self.root = Path(root or Path.cwd()).resolve()
        self.meda = self.root / "external/MEDA"
        self.main = self.meda / "skills/meda/scripts/main.py"
        self.session = (
            self.meda /
            "sessions/ima_universe_intelligence"
        )
        self.timeout = timeout

    def investigate(self, question=None):

        started = time.time()

        result = {
            "status": "FAILED",
            "agent": self.name,
            "question": question,
            "hypotheses": [],
            "evidence": [],
            "assumptions": [],
            "uncertainties": [],
            "conflicts": [],
            "next_actions": [],
            "answer": None,
            "duration": None,
            "returncode": None,
            "stderr": "",
            "stdout": "",
        }

        try:

            self.session.mkdir(
                parents=True,
                exist_ok=True
            )

            problem = self.session / "problem.json"
            setup = self.session / "setup.yaml"
            output = (
                self.session /
                "ima_supervised_meda_result.json"
            )

            if not self.main.exists():
                result["status"] = "BLOCKED"
                result["uncertainties"].append(
                    "MEDA main.py does not exist."
                )
                return result

            if not problem.exists():
                result["status"] = "BLOCKED"
                result["uncertainties"].append(
                    "MEDA problem.json does not exist."
                )
                return result

            if not setup.exists():
                result["status"] = "BLOCKED"
                result["uncertainties"].append(
                    "MEDA setup.yaml does not exist."
                )
                return result

            if output.exists():
                output.unlink()

            cmd = [
                sys.executable,
                str(self.main),
                "--mode",
                "constraint_only",
                "--setup",
                str(setup.resolve()),
                "--problem",
                str(problem.resolve()),
                "--output",
                str(output.resolve()),
            ]

            process = subprocess.run(
                cmd,
                cwd=str(self.meda),
                text=True,
                capture_output=True,
                timeout=self.timeout,
            )

            result["returncode"] = process.returncode
            result["stdout"] = process.stdout[-30000:]
            result["stderr"] = process.stderr[-30000:]
            result["duration"] = round(
                time.time() - started,
                3
            )

            if (
                process.returncode == 0
                and output.exists()
            ):
                try:
                    data = json.loads(
                        output.read_text(
                            encoding="utf-8"
                        )
                    )

                    result["status"] = "ANSWER_READY"
                    result["answer"] = data

                    if isinstance(data, dict):
                        result["hypotheses"] = data.get(
                            "hypotheses", []
                        )
                        result["evidence"] = data.get(
                            "evidence", []
                        )
                        result["uncertainties"] = data.get(
                            "uncertainties",
                            []
                        )

                    return result

                except Exception as e:
                    result["status"] = "FAILED"
                    result["uncertainties"].append(
                        "MEDA produced an unreadable output."
                    )
                    result["uncertainties"].append(
                        repr(e)
                    )
                    return result

            result["status"] = "FAILED"

            if process.stderr:
                result["uncertainties"].append(
                    "MEDA process returned non-zero status."
                )

            return result

        except subprocess.TimeoutExpired as e:

            result["status"] = "TIMEOUT"
            result["duration"] = round(
                time.time() - started,
                3
            )

            result["stdout"] = (
                e.stdout[-30000:]
                if isinstance(e.stdout, str)
                else ""
            )

            result["stderr"] = (
                e.stderr[-30000:]
                if isinstance(e.stderr, str)
                else ""
            )

            result["uncertainties"].append(
                "MEDA execution exceeded supervisor timeout."
            )

            result["next_actions"].extend([
                "Diagnose MEDA execution path.",
                "Try isolated components.",
                "Route question to another research agent.",
                "Do not classify timeout as scientific disproof."
            ])

            return result

        except Exception:

            result["status"] = "FAILED"
            result["duration"] = round(
                time.time() - started,
                3
            )
            result["uncertainties"].append(
                traceback.format_exc()
            )

            return result
''',
encoding="utf-8"
)

# ------------------------------------------------------------
# 3. IMA RESEARCH SUPERVISOR
# ------------------------------------------------------------

backup(SUPERVISOR)

SUPERVISOR.write_text(r'''
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

            from .meda_adapter import MEDAAdapter

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
''',
encoding="utf-8"
)

# ------------------------------------------------------------
# 4. REGISTRY
# ------------------------------------------------------------

backup(REGISTRY)

REGISTRY.write_text(
json.dumps({
    "version": "1.0",
    "supervisor": "IMAResearchSupervisor",
    "agents": {
        "MEDA": {
            "enabled": True,
            "adapter": ".ima/research/meda_adapter.py",
            "role": [
                "constraint reasoning",
                "dynamical models",
                "model comparison"
            ]
        },
        "literature": {
            "enabled": False,
            "role": [
                "literature search",
                "evidence retrieval"
            ],
            "status": "ADAPTER_PENDING"
        },
        "hypothesis": {
            "enabled": False,
            "role": [
                "hypothesis generation",
                "hypothesis comparison"
            ],
            "status": "ADAPTER_PENDING"
        },
        "critic": {
            "enabled": False,
            "role": [
                "counterarguments",
                "falsification",
                "independent review"
            ],
            "status": "ADAPTER_PENDING"
        },
        "evolutionary_search": {
            "enabled": False,
            "role": [
                "algorithmic search",
                "optimization"
            ],
            "status": "ADAPTER_PENDING"
        }
    }
}, ensure_ascii=False, indent=2),
encoding="utf-8"
)

# ------------------------------------------------------------
# 5. COMPILE
# ------------------------------------------------------------

targets = [
    SUPERVISOR,
    ADAPTER,
]

for path in targets:
    py_compile.compile(
        str(path),
        doraise=True
    )

print()
print("=" * 78)
print("IMA RESEARCH SUPERVISOR INSTALLED")
print("=" * 78)
print("SUPERVISOR :", SUPERVISOR)
print("PROTOCOL   :", PROTOCOL)
print("MEDA       :", ADAPTER)
print("REGISTRY   :", REGISTRY)
print()
print("Next: run the integrated test.")
