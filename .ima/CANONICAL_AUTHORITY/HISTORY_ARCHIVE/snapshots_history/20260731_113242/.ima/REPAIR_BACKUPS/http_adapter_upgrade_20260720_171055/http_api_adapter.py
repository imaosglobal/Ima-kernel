from urllib.request import Request, urlopen
from urllib.parse import urlparse
import importlib.util
import subprocess
import socket
from pathlib import Path

_CONTRACT = Path(__file__).resolve().parents[1] / "UNIVERSAL_ADAPTER_CONTRACT.py"
_spec = importlib.util.spec_from_file_location("ima_universal_adapter_contract", _CONTRACT)
_contract = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_contract)
UniversalAdapter = _contract.UniversalAdapter

class HTTPAPIAdapter(UniversalAdapter):
    def discover(self):
        return {"type": "http_api", "status": "available"}

    def connect(self, config=None):
        return {"connected": True, "config": config or {}}

    def capabilities(self):
        return ["GET", "POST", "PUT", "PATCH", "DELETE"]

    def execute(self, action, payload=None):
        if not action or "url" not in action:
            return {"ok": False, "error": "url_required"}

        url = action["url"]

        cmd = [
            "curl",
            "--doh-url", "https://cloudflare-dns.com/dns-query",
            "-4", "-L",
            "--silent", "--show-error",
            "--max-time", "10",
            "-X", action.get("method", "GET"),
        ]

        for k, v in action.get("headers", {}).items():
            cmd += ["-H", f"{k}: {v}"]

        cmd.append(url)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=15,
            )

            return {
                "ok": result.returncode == 0,
                "status": result.returncode,
                "body": result.stdout,
                **({"error": result.stderr} if result.returncode != 0 else {}),
            }

        except Exception as e:
            return {"ok": False, "error": str(e)}

    def observe(self):
        return {"adapter": "http_api", "status": "ready"}

    def verify(self, result):
        return bool(result and result.get("ok") is True)

    def disconnect(self):
        return {"connected": False}
