
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
