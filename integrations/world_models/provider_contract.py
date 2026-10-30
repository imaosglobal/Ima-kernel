"""Provider-neutral contract for connecting IMA to a verified interactive world model.

No provider is assumed. A real adapter must implement this contract and pass the
verification gates before being exposed as a live IMA capability.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol


@dataclass(frozen=True)
class WorldModelRequest:
    prompt: str
    duration_seconds: int = 30
    seed: int | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class WorldModelResult:
    provider: str
    environment: Any
    provenance: Mapping[str, Any]
    simulation_only: bool = True


class WorldModelProvider(Protocol):
    provider_name: str
    capabilities: tuple[str, ...]

    def generate(self, request: WorldModelRequest) -> WorldModelResult:
        """Generate one bounded simulation through an authenticated provider."""


def verify_provider_contract(provider: WorldModelProvider) -> dict[str, Any]:
    return {
        "provider": provider.provider_name,
        "authenticated_adapter_present": callable(getattr(provider, "generate", None)),
        "capabilities": list(getattr(provider, "capabilities", ())),
        "simulation_only": True,
        "live_verified": False,
        "status": "ADAPTER_PRESENT_PENDING_LIVE_VERIFICATION",
    }
