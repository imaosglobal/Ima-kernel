"""Creative Bridge: turn gaps between domains into testable structures."""
from dataclasses import dataclass, field
from enum import Enum

class BridgeStatus(str, Enum):
    HYPOTHESIS = "HYPOTHESIS"
    CONNECTED = "CONNECTED"
    TESTED = "TESTED"
    VERIFIED = "VERIFIED"

@dataclass
class DomainGap:
    left: str
    right: str
    missing: str
    evidence: list[str] = field(default_factory=list)

@dataclass
class CreativeBridge:
    gap: DomainGap
    structure: str
    status: BridgeStatus = BridgeStatus.HYPOTHESIS
    tests: list[str] = field(default_factory=list)

    def connect(self):
        self.status = BridgeStatus.CONNECTED
        return self

    def add_test(self, test: str):
        if not test.strip():
            raise ValueError("test must not be empty")
        self.tests.append(test)

    def mark_tested(self, passed: bool):
        if not self.tests:
            raise ValueError("a test is required")
        self.status = BridgeStatus.TESTED if passed else BridgeStatus.HYPOTHESIS
        return self

    def verify(self, evidence):
        evidence = [x for x in evidence if x and x.strip()]
        if self.status != BridgeStatus.TESTED or not evidence:
            raise ValueError("verification requires passed tests and evidence")
        self.gap.evidence.extend(evidence)
        self.status = BridgeStatus.VERIFIED
        return self

def build_bridge(left: str, right: str, missing: str, structure: str):
    if not all(x and x.strip() for x in (left, right, missing, structure)):
        raise ValueError("all bridge fields are required")
    return CreativeBridge(DomainGap(left.strip(), right.strip(), missing.strip()), structure.strip())

def bridge_packet(bridge: CreativeBridge):
    return {"left": bridge.gap.left, "right": bridge.gap.right, "missing": bridge.gap.missing, "structure": bridge.structure, "status": bridge.status.value, "tests": list(bridge.tests), "evidence": list(bridge.gap.evidence)}
