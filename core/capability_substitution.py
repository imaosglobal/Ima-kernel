"""Capability substitution and provider-independence layer for IMA."""
from __future__ import annotations
from dataclasses import dataclass, field
from .universal_learning_engine import Capability, CapabilityState

@dataclass
class CapabilityRegistry:
    capabilities: dict[str, Capability] = field(default_factory=dict)
    def register(self, capability: Capability) -> None: self.capabilities[capability.name] = capability
    def best_available(self, name: str) -> Capability | None: return self.capabilities.get(name)
    def promote(self, name: str, state: CapabilityState) -> Capability:
        capability = self.capabilities[name]
        order = [CapabilityState.PLANNED, CapabilityState.DISCOVERED, CapabilityState.CONNECTED,
                 CapabilityState.TESTED, CapabilityState.DEPLOYED, CapabilityState.VERIFIED_LIVE]
        if state != CapabilityState.BLOCKED and order.index(state) < order.index(capability.state):
            raise ValueError("capability state cannot regress through promotion")
        capability.state = state
        return capability
    def unresolved(self) -> list[Capability]:
        return [c for c in self.capabilities.values() if c.state != CapabilityState.VERIFIED_LIVE]
