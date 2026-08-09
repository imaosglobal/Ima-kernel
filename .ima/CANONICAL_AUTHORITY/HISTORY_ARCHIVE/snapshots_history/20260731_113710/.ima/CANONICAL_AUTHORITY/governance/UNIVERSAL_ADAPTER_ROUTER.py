from pathlib import Path
from urllib.parse import urlparse
import json


class UniversalAdapterRouter:

    def __init__(self, registry_path):
        self.registry_path = Path(registry_path)
        self.registry = json.loads(
            self.registry_path.read_text()
        )

    def resolve(self, target):
        parsed = urlparse(str(target))
        scheme = parsed.scheme.lower()

        if not scheme:
            return {
                "status": "no_scheme",
                "scheme": None,
                "target": str(target)
            }

        config = self.registry.get(
            "schemes", {}
        ).get(scheme)

        if config is None:
            return {
                "status": "unsupported_scheme",
                "scheme": scheme,
                "target": str(target)
            }

        if not config.get("enabled", False):
            return {
                "status": "disabled_scheme",
                "scheme": scheme,
                "adapter": config.get("adapter"),
                "target": str(target)
            }

        adapter_name = config.get("adapter")

        adapter = None
        if adapter_name in ("network", "http_api"):
            from governance.adapters.http_api_adapter import HTTPAPIAdapter
            adapter = HTTPAPIAdapter()

            return {
                "status": "resolved",
                "scheme": scheme,
                "adapter": adapter,
                "adapter_name": config.get("adapter"),
                "target": str(target)
            }

        return {
            "status": "resolved",
            "scheme": scheme,
            "adapter": adapter_name,
            "target": str(target)
        }

    def execute(self, target, action=None, payload=None):
        resolved = self.resolve(target)

        if isinstance(action, str):
            action = {"url": action}
        elif action is None:
            action = {"url": str(target)}

        if resolved.get("status") != "resolved":
            return resolved

        adapter = resolved.get("adapter")

        if hasattr(adapter, "execute"):
            result = adapter.execute(action, payload)
            verified = adapter.verify(result)

            return {
                "status": "executed" if verified else "verification_failed",
                "target": str(target),
                "result": result,
                "verified": verified
            }

        return {
            "status": "adapter_not_executable",
            "target": str(target)
        }
