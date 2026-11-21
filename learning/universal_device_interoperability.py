"""Canonical device-agnostic IMA interoperability contract.

IMA is designed as a portable intelligence layer, not as a device-specific app.
Device adapters expose capabilities to the canonical runtime; they do not become
independent brains or memory authorities.
"""

from dataclasses import dataclass, asdict


DEVICE_CLASSES = (
    "phone", "tablet", "computer", "browser", "smart_tv", "smart_mirror",
    "refrigerator", "vehicle", "drone", "robot_home", "robot_industrial",
    "wearable", "camera", "speaker", "smart_home", "aircraft", "spacecraft",
    "accessibility_device", "future_unknown",
)


@dataclass(frozen=True)
class DeviceAdapterContract:
    device_class: str
    capabilities: tuple[str, ...]
    transport: str
    identity_scope: str = "user_authorized"
    memory_authority: str = "canonical_ima_only"
    status: str = "ADAPTER_CONTRACT"


def register_adapter(device_class: str, capabilities: tuple[str, ...], transport: str) -> dict:
    if device_class not in DEVICE_CLASSES:
        device_class = "future_unknown"
    return asdict(DeviceAdapterContract(
        device_class=device_class,
        capabilities=capabilities,
        transport=transport,
    ))
