"""Safe deployment health contract migrated from imaosglobal/Ima-self-deploy.

The legacy scripts perform package installation, Docker mutation and process killing.
The canonical migration keeps only deterministic checks and leaves deployment execution
to the existing canonical CI/CD pipeline.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class HealthCheck:
    name: str
    ok: bool
    detail: str


def evaluate_runtime_contract(
    *,
    app_entrypoint_present: bool,
    requirements_present: bool,
    deployment_pipeline_present: bool,
) -> list[HealthCheck]:
    return [
        HealthCheck("app_entrypoint", app_entrypoint_present, "Application entrypoint presence"),
        HealthCheck("requirements", requirements_present, "Dependency manifest presence"),
        HealthCheck("canonical_pipeline", deployment_pipeline_present, "Canonical deployment pipeline presence"),
    ]


def healthy(checks: list[HealthCheck]) -> bool:
    return all(check.ok for check in checks)
