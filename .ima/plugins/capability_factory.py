"""IMA first-party capability-factory primitives.

This module is deliberately provider-neutral. It defines the evidence-bearing
adapter contract and gap lifecycle; it does not bypass provider authentication
or automatically connect third-party accounts.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List


GAP_STATES = (
    "detected",
    "specified",
    "scaffolded",
    "implemented",
    "tested",
    "verified",
    "published",
    "monitored",
    "reassessed",
)

TRUTH_STATES = (
    "discovered",
    "connected",
    "authenticated",
    "executable",
    "tested",
    "verified",
    "generalized",
)


@dataclass
class CapabilityEvidence:
    state: str
    source: str
    detail: str
    timestamp: str


@dataclass
class CapabilityAdapter:
    id: str
    provider: str
    capabilities: List[str]
    execute: Callable[..., Any] | None = None
    evidence: List[CapabilityEvidence] = field(default_factory=list)
    limits: Dict[str, Any] = field(default_factory=dict)
    commercial: Dict[str, Any] = field(default_factory=dict)

    def record(self, evidence: CapabilityEvidence) -> None:
        if evidence.state not in TRUTH_STATES:
            raise ValueError(f"unknown truth state: {evidence.state}")
        self.evidence.append(evidence)

    def is_verified(self) -> bool:
        return any(item.state == "verified" for item in self.evidence)

    def health(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "provider": self.provider,
            "capabilities": self.capabilities,
            "verified": self.is_verified(),
            "evidence_count": len(self.evidence),
        }
