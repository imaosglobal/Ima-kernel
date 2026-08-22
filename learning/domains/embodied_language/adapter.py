
"""
IMA Embodied Language Domain Adapter

This adapter exposes the existing embodied_language domain
to IMA's learning/knowledge infrastructure without creating
a second learning engine.
"""

from pathlib import Path
import json
import time

ROOT = Path.home() / "ima_kernel"
IMA = ROOT / ".ima"
DATA = IMA / "research" / "embodied_language"

OBSERVATIONS = DATA / "observations.jsonl"
HYPOTHESES = DATA / "hypotheses.jsonl"


def get_domain():
    from .domain import load_domain
    return load_domain()


def observe(
    source,
    language,
    expression,
    body_concept=None,
    target_concept=None,
    mapping=None,
    evidence=None,
    confidence=None,
    relation_type="observation",
):
    """
    Store one normalized observation.

    Important:
    similarity is never treated as etymological proof.
    """

    item = {
        "timestamp": time.time(),
        "domain": "embodied_language",
        "type": "observation",
        "source": source,
        "language": language,
        "expression": expression,
        "body_concept": body_concept,
        "target_concept": target_concept,
        "mapping": mapping,
        "evidence": evidence or [],
        "confidence": confidence,
        "relation_type": relation_type,
        "status": "unverified",
    }

    OBSERVATIONS.parent.mkdir(parents=True, exist_ok=True)

    with OBSERVATIONS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

    return item


def hypothesize(
    statement,
    supporting_observations=None,
    competing_explanations=None,
    confidence=0.1,
):
    """
    Store a hypothesis separately from established knowledge.
    """

    item = {
        "timestamp": time.time(),
        "domain": "embodied_language",
        "type": "hypothesis",
        "statement": statement,
        "supporting_observations": supporting_observations or [],
        "competing_explanations": competing_explanations or [],
        "confidence": confidence,
        "status": "hypothesis",
        "validation_required": True,
    }

    HYPOTHESES.parent.mkdir(parents=True, exist_ok=True)

    with HYPOTHESES.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

    return item


def domain_capabilities():
    d = get_domain()

    return {
        "domain": d["domain"],
        "languages": d["languages"],
        "concepts": d["concepts"],
        "mapping_layers": d["mapping_layers"],
        "rules": d["rules"],
        "capabilities": [
            "cross_linguistic_comparison",
            "embodied_mapping",
            "metaphor_analysis",
            "concept_mapping",
            "hypothesis_generation",
            "evidence_tracking",
            "uncertainty_tracking",
            "historical_etymology_separation",
        ],
    }


if __name__ == "__main__":
    c = domain_capabilities()
