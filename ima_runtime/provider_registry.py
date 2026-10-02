"""Auditable registry for external knowledge/tool providers.

The registry describes integrations that IMA may use. It never claims that a
provider was consulted; execution must be supplied by a real adapter/provider.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ProviderSpec:
    provider_id: str
    kind: str
    purpose: str
    requires_connection: bool = True
    read_only_by_default: bool = True


PROVIDERS: tuple[ProviderSpec, ...] = (
    ProviderSpec("web", "external_knowledge", "current public information and independent sources", False),
    ProviderSpec("github", "project_source", "code, issues, pull requests, workflows and provenance"),
    ProviderSpec("dropbox", "document_source", "user-authorized documents and project files"),
    ProviderSpec("render", "runtime_source", "deployments, services, logs and operational state"),
    ProviderSpec("posthog", "analytics_source", "product analytics, errors and experiments"),
    ProviderSpec("stripe", "payments_source", "payment documentation and authorized payment state"),
    ProviderSpec("human", "human_perspective", "explicitly provided human expertise or testimony", False),
    ProviderSpec("independent_model", "independent_reasoning", "an independently produced analysis", True),
)


def available(provider_ids: Iterable[str]) -> tuple[ProviderSpec, ...]:
    wanted = set(provider_ids)
    return tuple(p for p in PROVIDERS if p.provider_id in wanted)


def self_test() -> bool:
    ids = {p.provider_id for p in PROVIDERS}
    return {"web", "github", "human", "independent_model"}.issubset(ids)
