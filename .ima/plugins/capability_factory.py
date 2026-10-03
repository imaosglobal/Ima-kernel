"""Executable IMA capability-gap lifecycle primitives.

Provider-neutral only: no automatic third-party authentication or bypass.
"""
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

GAP_STATES: Tuple[str, ...] = (
    "detected", "specified", "scaffolded", "implemented", "tested",
    "verified", "published", "monitored", "reassessed",
)
TRUTH_STATES: Tuple[str, ...] = (
    "discovered", "connected", "authenticated", "executable",
    "tested", "verified", "generalized",
)


@dataclass
class CapabilityEvidence:
    state: str
    source: str
    detail: str
    timestamp: str

    def __post_init__(self) -> None:
        if self.state not in TRUTH_STATES:
            raise ValueError(f"unknown truth state: {self.state}")
        for name, value in (("source", self.source), ("detail", self.detail),
                            ("timestamp", self.timestamp)):
            if not value or not value.strip():
                raise ValueError(f"{name} is required")


@dataclass
class CapabilityAdapter:
    id: str
    provider: str
    capabilities: List[str]
    execute: Optional[Callable[..., Any]] = None
    evidence: List[CapabilityEvidence] = field(default_factory=list)
    limits: Dict[str, Any] = field(default_factory=dict)
    commercial: Dict[str, Any] = field(default_factory=dict)

    def record(self, evidence: CapabilityEvidence) -> None:
        self.evidence.append(evidence)

    def is_verified(self) -> bool:
        return any(item.state == "verified" for item in self.evidence)

    def health(self) -> Dict[str, Any]:
        return {
            "id": self.id, "provider": self.provider,
            "capabilities": self.capabilities,
            "verified": self.is_verified(),
            "evidence_count": len(self.evidence),
        }


@dataclass
class CapabilityGap:
    id: str
    capability: str
    description: str
    state: str = "detected"
    evidence: List[CapabilityEvidence] = field(default_factory=list)
    providers: List[str] = field(default_factory=list)

    def advance(self, state: str) -> None:
        if state not in GAP_STATES:
            raise ValueError(f"unknown gap state: {state}")
        if GAP_STATES.index(state) < GAP_STATES.index(self.state):
            raise ValueError(f"cannot move gap backwards: {self.state} -> {state}")
        self.state = state

    def add_provider(self, provider: str) -> None:
        if provider and provider not in self.providers:
            self.providers.append(provider)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "id": self.id, "capability": self.capability,
            "description": self.description, "state": self.state,
            "providers": self.providers,
            "evidence_count": len(self.evidence),
        }


def verify_adapter(adapter: CapabilityAdapter, test: Callable[[], Any],
                   source: str, timestamp: str) -> Any:
    result = test()
    adapter.record(CapabilityEvidence(
        state="tested", source=source,
        detail="execution test completed", timestamp=timestamp,
    ))
    if result is False:
        return result
    adapter.record(CapabilityEvidence(
        state="verified", source=source,
        detail="execution test returned non-false result", timestamp=timestamp,
    ))
    return result
