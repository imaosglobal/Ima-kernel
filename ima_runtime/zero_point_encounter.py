"""Zero-point encounter protocol for IMA.

The protocol preserves permitted memory while preventing prior assumptions from
being silently treated as current truth. It is deliberately deterministic and
does not infer a person's inner state.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Optional


@dataclass(frozen=True)
class EncounterState:
    memory_context: tuple = ()
    assumptions: tuple = ()
    facts: tuple = ()
    feelings: tuple = ()
    interpretations: tuple = ()
    unknowns: tuple = ()
    reset_assumptions: bool = True
    provenance: tuple = ()


def _tuple(value: Optional[Iterable]) -> tuple:
    if value is None:
        return ()
    if isinstance(value, (str, bytes)):
        return (value,)
    return tuple(value)


def begin_at_zero(
    *,
    memory_context: Iterable = (),
    assumptions: Iterable = (),
    facts: Iterable = (),
    feelings: Iterable = (),
    interpretations: Iterable = (),
    unknowns: Iterable = (),
    provenance: Iterable = (),
) -> EncounterState:
    """Start a fresh encounter without deleting permitted memory.

    Prior assumptions are retained as inspectable history only; they are not
    promoted into the current encounter as facts.
    """
    return EncounterState(
        memory_context=_tuple(memory_context),
        assumptions=_tuple(assumptions),
        facts=_tuple(facts),
        feelings=_tuple(feelings),
        interpretations=_tuple(interpretations),
        unknowns=_tuple(unknowns),
        reset_assumptions=True,
        provenance=_tuple(provenance),
    )


def self_test() -> dict:
    state = begin_at_zero(
        memory_context=("previous context",),
        assumptions=("old interpretation",),
        facts=("current observable fact",),
        feelings=("reported feeling",),
        interpretations=("current interpretation",),
        unknowns=("not established",),
    )
    assert state.memory_context == ("previous context",)
    assert state.assumptions == ("old interpretation",)
    assert state.facts == ("current observable fact",)
    assert state.reset_assumptions is True
    assert "old interpretation" not in state.facts
    assert "not established" in state.unknowns
    return {
        "ok": True,
        "reset_assumptions": state.reset_assumptions,
        "memory_preserved": len(state.memory_context),
        "unknowns_preserved": len(state.unknowns),
    }


if __name__ == "__main__":
    print(self_test())
