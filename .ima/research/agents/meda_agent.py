
from pathlib import Path
import subprocess
import sys
import json
import time
import uuid


class MEDAAgent:

    name = "MEDA"

    def __init__(self, root=None, timeout=180):

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
