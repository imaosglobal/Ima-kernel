"""Executable capability-gap queue manager.

Provider-neutral: it reads the canonical gap queue and never authenticates
against external providers or marks a capability verified without evidence.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .capability_factory import GAP_STATES


PRIORITY = {"critical": 0, "high": 1, "medium": 2, "low": 3}


class CapabilityGapQueue:
    def __init__(self, path: Optional[Path] = None) -> None:
        self.path = path or Path(__file__).resolve().parents[2] / "integrations" / "IMA_CAPABILITY_GAPS.json"

    def load(self) -> Dict[str, Any]:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def gaps(self) -> List[Dict[str, Any]]:
        return list(self.load().get("gaps", []))

    def next_gap(self) -> Optional[Dict[str, Any]]:
        open_gaps = [g for g in self.gaps() if g.get("state") != "reassessed"]
        if not open_gaps:
            return None
        return sorted(
            open_gaps,
            key=lambda g: (PRIORITY.get(g.get("priority", "low"), 3),
                           GAP_STATES.index(g.get("state", "detected")),
                           g.get("id", "")),
        )[0]

    def snapshot(self) -> Dict[str, Any]:
        gaps = self.gaps()
        counts = {state: 0 for state in GAP_STATES}
        for gap in gaps:
            state = gap.get("state")
            if state in counts:
                counts[state] += 1
        return {
            "schema": self.load().get("schema"),
            "policy": self.load().get("policy"),
            "total": len(gaps),
            "by_state": counts,
            "next": self.next_gap(),
        }
