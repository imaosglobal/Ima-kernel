from dataclasses import dataclass, field
from typing import Any
@dataclass(frozen=True)
class Capability:
    id: str; category: str; provider: str; action: str; description: str; risk: str="low"; enabled: bool=True
@dataclass
class ActionRequest:
    goal: str; action: str; target: Any=None; context: dict=field(default_factory=dict); require_confirmation: bool=False
@dataclass
class ActionResult:
    ok: bool; capability_id: str; status: str; output: Any=None; evidence: dict=field(default_factory=dict); error: str|None=None
