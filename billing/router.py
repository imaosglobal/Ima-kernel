import json
from pathlib import Path

REGISTRY = Path(__file__).parent / "registry" / "providers.json"


def providers():
    return json.loads(
        REGISTRY.read_text(encoding="utf-8")
    )["providers"]


def available(platform=None, capability=None, provider_type=None):
    result = providers()

    if platform:
        result = [
            p for p in result
            if platform in p.get("platforms", [])
        ]

    if capability:
        result = [
            p for p in result
            if capability in p.get("capabilities", [])
        ]

    if provider_type:
        result = [
            p for p in result
            if p.get("type") == provider_type
        ]

    return result


def choose(platform, capability, provider_type="psp"):
    matches = available(
        platform=platform,
        capability=capability,
        provider_type=provider_type,
    )

    if not matches:
        raise RuntimeError(
            f"No provider for "
            f"platform={platform}, "
            f"capability={capability}, "
            f"type={provider_type}"
        )

    return matches[0]


if __name__ == "__main__":
    print("WEB PSP:")
    for p in available("web", "cards", "psp"):
        print(" -", p["id"])

    print("\nANDROID SUBSCRIPTIONS:")
    for p in available("android", "subscriptions"):
        print(" -", p["id"])

    print("\nGOOGLE PAY PSP:")
    for p in available("web", "google_pay", "psp"):
        print(" -", p["id"])

    print("\nWALLETS:")
    for p in available(provider_type="wallet"):
        print(" -", p["id"])

    print("\nPLATFORM BILLING:")
    for p in available(provider_type="platform"):
        print(" -", p["id"])
