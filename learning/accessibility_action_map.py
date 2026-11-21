"""Evidence-bounded accessibility-tree action mapping.

Converts an observed accessibility tree into stable action candidates.
It never clicks, types, submits, or mutates device state.
"""

from dataclasses import dataclass, asdict
from typing import Any, Iterable


@dataclass(frozen=True)
class ActionCandidate:
    ref: str
    role: str
    name: str
    action: str


def build_action_candidates(nodes: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[ActionCandidate] = []
    for node in nodes:
        ref = str(node.get("ref", "")).strip()
        role = str(node.get("role", "")).strip().lower()
        name = str(node.get("name", "")).strip()
        if not ref or not role or not name:
            continue
        if role in {"button", "link", "checkbox", "radio", "textbox", "combobox"}:
            action = {
                "button": "activate",
                "link": "activate",
                "checkbox": "toggle",
                "radio": "select",
                "textbox": "fill",
                "combobox": "select",
            }[role]
            out.append(ActionCandidate(ref, role, name, action))
    return [asdict(x) for x in out]
