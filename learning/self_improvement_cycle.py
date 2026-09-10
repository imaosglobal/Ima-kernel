"""
Compatibility wrapper.

Canonical self-development implementation:
    learning.self_improvement
"""

from learning.self_improvement import run_self_improvement as _run_self_improvement


def run_self_improvement(apply=False):
    """
    Backward-compatible entry point.

    The legacy `apply` argument is intentionally ignored.
    Self-development policy is controlled by the canonical engine.
    """
    return _run_self_improvement()


if __name__ == "__main__":
    import json
    print(json.dumps(run_self_improvement(), indent=2, ensure_ascii=False))
