"""First-party proof adapter used to verify the capability factory itself."""
from __future__ import annotations

import importlib.util
from pathlib import Path

_FACTORY_PATH = Path(__file__).resolve().parent / "capability_factory.py"
_spec = importlib.util.spec_from_file_location("ima_capability_factory_selftest", _FACTORY_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError("capability factory module spec unavailable")
_factory = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_factory)

CapabilityAdapter = _factory.CapabilityAdapter
verify_adapter = _factory.verify_adapter


def run_factory_self_test() -> bool:
    adapter = CapabilityAdapter(
        id="ima-capability-factory-self-test",
        provider="IMA",
        capabilities=["adapter_lifecycle"],
    )
    result = verify_adapter(
        adapter,
        lambda: True,
        source="local:first-party-self-test",
        timestamp="runtime",
    )
    return bool(result) and adapter.is_verified()


if __name__ == "__main__":
    raise SystemExit(0 if run_factory_self_test() else 1)
