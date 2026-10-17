"""Bounded self-application planner for verified IMA capabilities."""
from __future__ import annotations
from dataclasses import dataclass
from .universal_learning_engine import Capability, CapabilityState

@dataclass(frozen=True)
class SelfApplicationPlan:
    capability: str
    target: str
    reason: str
    state: str = "PROPOSED"
    gates: tuple[str,...] = ("INSPECT","PLAN","CHANGE","TEST","VERIFY","CARRY_FORWARD")

def propose_self_application(capability: Capability, target: str, reason: str) -> SelfApplicationPlan:
    if capability.state != CapabilityState.VERIFIED_LIVE:
        raise ValueError("only VERIFIED_LIVE capabilities may enter self-application")
    return SelfApplicationPlan(capability.name,target,reason)

def can_apply(plan: SelfApplicationPlan, verification: bool) -> bool:
    return plan.state == "VERIFIED" and verification
