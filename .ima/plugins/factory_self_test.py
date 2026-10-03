"""First-party proof adapter used to verify the capability factory itself."""
from .capability_factory import CapabilityAdapter, verify_adapter


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
