"""Provider-independent universal learning contract for IMA."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Iterable

class EvidenceLevel(str, Enum):
    PRIMARY_SOURCE="PRIMARY_SOURCE"; PEER_REVIEWED="PEER_REVIEWED"; OFFICIAL="OFFICIAL"
    SECONDARY="SECONDARY"; TERTIARY="TERTIARY"; COMMUNITY="COMMUNITY"
    USER_REPORT="USER_REPORT"; MODEL_INFERENCE="MODEL_INFERENCE"; HYPOTHESIS="HYPOTHESIS"

class CapabilityState(str, Enum):
    PLANNED="PLANNED"; DISCOVERED="DISCOVERED"; CONNECTED="CONNECTED"
    TESTED="TESTED"; DEPLOYED="DEPLOYED"; VERIFIED_LIVE="VERIFIED_LIVE"; BLOCKED="BLOCKED"

@dataclass(frozen=True)
class Source:
    title: str
    locator: str
    evidence: EvidenceLevel
    language: str | None = None
    original: bool = False

@dataclass
class Domain:
    name: str
    definition: str
    parent_domains: list[str] = field(default_factory=list)
    subdomains: list[str] = field(default_factory=list)
    people: list[str] = field(default_factory=list)
    sources: list[Source] = field(default_factory=list)
    methods: list[str] = field(default_factory=list)
    disputes: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    connections: list[str] = field(default_factory=list)

@dataclass
class Capability:
    name: str
    purpose: str
    state: CapabilityState
    provider: str | None = None
    alternatives: list[str] = field(default_factory=list)
    cost_class: str = "UNKNOWN"
    license: str = "UNKNOWN"
    privacy_reviewed: bool = False
    evidence: list[Source] = field(default_factory=list)
    fallback: str | None = None

@dataclass
class EmergingFieldProposal:
    name: str
    definition: str
    parent_domains: list[str]
    provenance: list[Source]
    questions: list[str]
    status: str = "PROPOSAL"

def propose_field(name: str, definition: str, parent_domains: Iterable[str],
                  provenance: Iterable[Source], questions: Iterable[str]) -> EmergingFieldProposal:
    return EmergingFieldProposal(name.strip(), definition.strip(), list(parent_domains), list(provenance), list(questions))

def connect_domains(a: Domain, b: Domain) -> None:
    if b.name not in a.connections: a.connections.append(b.name)
    if a.name not in b.connections: b.connections.append(a.name)

def knowledge_packet(domain: Domain) -> dict:
    data = asdict(domain)
    data["status_rule"] = "facts require evidence; uncertainty and disagreement remain visible"
    return data

def capability_packet(capability: Capability) -> dict:
    data = asdict(capability); data["state"] = capability.state.value
    data["promotion_rule"] = "PLANNED -> DISCOVERED -> CONNECTED -> TESTED -> DEPLOYED -> VERIFIED_LIVE"
    return data
