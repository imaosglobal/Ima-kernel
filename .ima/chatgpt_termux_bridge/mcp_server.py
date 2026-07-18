import json
import os
import sys
import time
from pathlib import Path

BASE = Path.home() / "ima_kernel"

if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

BRIDGE = BASE / ".ima" / "chatgpt_termux_bridge"

def runtime_status():
    result = {
        "bridge": "IMA Termux Bridge",
        "status": "online",
        "time": time.time(),
        "termux": True,
        "ollama": False,
        "runtime": False
    }

    try:
        import ima_master_runtime
        result["runtime"] = True
        result["runtime_module"] = str(
            Path(ima_master_runtime.__file__).resolve()
        )
    except Exception as e:
        result["runtime_error"] = str(e)

    return result


def ima_ask(message):
    if not isinstance(message, str):
        message = str(message)

    try:
        import ima_master_runtime

        result = ima_master_runtime.ask(message)

        return {
            "status": "ok",
            "source": "ima_master_runtime",
            "result": result
        }

    except Exception as e:
        return {
            "status": "error",
            "source": "ima_master_runtime",
            "error": str(e)
        }


def read_file(path):
    path = Path(path).expanduser().resolve()

    allowed_roots = [
        BASE.resolve()
    ]

    if not any(
        str(path).startswith(str(root))
        for root in allowed_roots
    ):
        return {
            "status": "denied",
            "error": "path outside IMA kernel"
        }

    try:
        return {
            "status": "ok",
            "path": str(path),
            "content": path.read_text(
                encoding="utf-8",
                errors="replace"
            )
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def main():
    print(
        json.dumps(
            {
                "name": "IMA Termux Bridge",
                "status": "ready",
                "transport": "stdio",
                "time": time.time()
            },
            ensure_ascii=False
        ),
        flush=True
    )

    for line in sys.stdin:
        line = line.strip()

        if not line:
            continue

        try:
            request = json.loads(line)
        except Exception as e:
            print(
                json.dumps(
                    {
                        "status": "error",
                        "error": f"invalid json: {e}"
                    },
                    ensure_ascii=False
                ),
                flush=True
            )
            continue

        method = request.get("method")
        params = request.get("params", {})

        if method == "health":
            response = runtime_status()

        elif method == "ima_ask":
            response = ima_ask(
                params.get("message", "")
            )

        elif method == "read_file":
            response = read_file(
                params.get("path", "")
            )

        else:
            response = {
                "status": "error",
                "error": f"unknown method: {method}"
            }

        print(
            json.dumps(
                response,
                ensure_ascii=False
            ),
            flush=True
        )


if __name__ == "__main__":
    main()
