"""Canonical adapter for the public IMA MCP distribution contract.

Provenance: imaosglobal/Ima-server/mcp.js.
Only read-only public metadata is represented here. Private memory, secrets and
external side effects are intentionally excluded.
"""


def public_status() -> dict:
    return {
        "name": "IMA",
        "status": "verified_public_runtime",
        "privacy": "public-runtime-only",
    }


def public_learning_policy() -> dict:
    return {
        "question": "What can IMA improve today?",
        "policy": "evidence-based; no fabricated learning",
    }


def public_distribution() -> dict:
    return {
        "canonical": "imaosglobal/Ima-kernel",
        "protocol": "MCP",
        "distribution": "opt-in",
        "human_approval_required_for_connection": True,
    }
