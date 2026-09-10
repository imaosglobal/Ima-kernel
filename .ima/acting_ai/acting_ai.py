from __future__ import annotations

import hashlib
import importlib
import inspect
import json
import re
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / ".ima" / "acting_ai"
STATE = BASE / "state"
LOGS = BASE / "logs"

ACTION_MEMORY = STATE / "actions.jsonl"
CAPABILITY_REGISTRY = STATE / "capabilities.json"

STATE.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)


# ============================================================
# DATA
# ============================================================

@dataclass
class Capability:
    name: str
    module: str
    kind: str
    callable_name: str
    confidence: float = 1.0


@dataclass
class Action:
    action: str
    target: str
    goal: str

    @property
    def identity(self) -> str:
        raw = json.dumps(
            {
                "action": normalize(self.action),
                "target": normalize(self.target),
                "goal": normalize(self.goal),
            },
            ensure_ascii=False,
            sort_keys=True,
        )

        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()


# ============================================================
# NORMALIZATION
# ============================================================

def normalize(value: Any) -> str:
    return re.sub(
        r"\s+",
        " ",
        str(value or "").strip().lower(),
    )


# ============================================================
# LOGGING
# ============================================================

def log(event: str, **data: Any) -> None:
    record = {
        "timestamp": time.time(),
        "event": event,
        **data,
    }

    path = LOGS / "acting_ai.jsonl"

    with path.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                record,
                ensure_ascii=False,
                default=str,
            )
            + "\n"
        )


# ============================================================
# DISCOVERY
# ============================================================

class CapabilityDiscovery:

    IGNORE = {
        ".git",
        "node_modules",
        "venv",
        ".venv",
        "__pycache__",
        "dist",
        "build",
    }

    # שמות שמייצגים יכולות, לא שמות קבצים בלבד.
    SYMBOL_PATTERNS = {
        "action": (
            "ActionEngine",
            "action_engine",
            "execute",
            "execute_action",
            "run_action",
            "act",
            "run_world_actions",
        ),
        "research": (
            "ResearchCouncil",
            "research_council",
            "investigate",
            "research",
            "literature",
            "semantic_scholar",
            "SEMANTIC_SCHOLAR",
            "MEDA",
            "meda",
        ),
        "memory": (
            "memory",
            "remember",
            "learning",
            "knowledge",
        ),
        "automation": (
            "automation",
            "scheduler",
            "schedule",
            "reminder",
        ),
        "connector": (
            "connector",
            "connect",
            "bridge",
        ),
        "agent": (
            "agent",
            "Agent",
        ),
        "planning": (
            "planner",
            "planning",
            "plan",
            "decision",
        ),
    }

    def __init__(self, root: Path):
        self.root = root

    def python_files(self):
        for path in self.root.rglob("*.py"):

            if any(
                part in self.IGNORE
                for part in path.parts
            ):
                continue

            yield path

    def module_name(self, path: Path):
        try:
            relative = path.relative_to(self.root)
        except ValueError:
            return None

        parts = list(relative.parts)

        if parts[-1].endswith(".py"):
            parts[-1] = parts[-1][:-3]

        if parts[-1] == "__init__":
            parts.pop()

        if not parts:
            return None

        return ".".join(parts)

    def classify_symbol(self, symbol: str):
        result = []

        lowered = symbol.lower()

        for domain, patterns in self.SYMBOL_PATTERNS.items():

            for pattern in patterns:

                if pattern.lower() in lowered:
                    result.append(domain)
                    break

        return result

    def inspect_source(self, path: Path):

        try:
            text = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except Exception as exc:

            log(
                "DISCOVERY_READ_FAILED",
                path=str(path),
                error=repr(exc),
            )

            return []

        module = self.module_name(path)

        if not module:
            return []

        capabilities = []

        # ----------------------------------------------------
        # FUNCTIONS
        # ----------------------------------------------------

        function_pattern = re.compile(
            r"^\s*(?:async\s+)?def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(",
            re.MULTILINE,
        )

        for match in function_pattern.finditer(text):

            name = match.group(1)
            domains = self.classify_symbol(name)

            if not domains:
                # בדיקה נוספת לפי תוכן הקובץ.
                surrounding = text[
                    max(0, match.start() - 300):
                    min(len(text), match.end() + 1000)
                ].lower()

                for domain, patterns in self.SYMBOL_PATTERNS.items():

                    if any(
                        p.lower() in surrounding
                        for p in patterns
                    ):
                        domains.append(domain)

            for domain in sorted(set(domains)):

                capabilities.append(
                    Capability(
                        name=f"{module}.{name}",
                        module=module,
                        kind="function",
                        callable_name=name,
                        confidence=0.85,
                    )
                )

        # ----------------------------------------------------
        # CLASSES
        # ----------------------------------------------------

        class_pattern = re.compile(
            r"^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)",
            re.MULTILINE,
        )

        for match in class_pattern.finditer(text):

            name = match.group(1)
            domains = self.classify_symbol(name)

            if not domains:
                continue

            capabilities.append(
                Capability(
                    name=f"{module}.{name}",
                    module=module,
                    kind="class",
                    callable_name=name,
                    confidence=0.95,
                )
            )

        # ----------------------------------------------------
        # FILE-LEVEL CAPABILITIES
        # ----------------------------------------------------

        lowered = text.lower()

        for domain, patterns in self.SYMBOL_PATTERNS.items():

            hits = [
                pattern
                for pattern in patterns
                if pattern.lower() in lowered
            ]

            if hits:

                capabilities.append(
                    Capability(
                        name=f"{module}::{domain}",
                        module=module,
                        kind="module_capability",
                        callable_name="",
                        confidence=0.70,
                    )
                )

        return capabilities

    def scan(self):

        found = []

        files_scanned = 0

        for path in self.python_files():

            files_scanned += 1

            found.extend(
                self.inspect_source(path)
            )

        unique = {}

        for capability in found:

            unique[
                capability.name
            ] = capability

        result = list(
            unique.values()
        )

        result.sort(
            key=lambda x: (
                x.kind,
                x.name,
            )
        )

        CAPABILITY_REGISTRY.write_text(
            json.dumps(
                [
                    asdict(cap)
                    for cap in result
                ],
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        log(
            "DISCOVERY_COMPLETE",
            files_scanned=files_scanned,
            capabilities=len(result),
        )

        return result


# ============================================================
# EXISTING COMPONENT MATCHING
# ============================================================

class CapabilityMatcher:

    PREFERRED = {
        "research": (
            "research",
            "literature",
            "semantic",
            "meda",
            "investigate",
        ),
        "action": (
            "action",
            "execute",
            "act",
            "automation",
            "agent",
        ),
        "memory": (
            "memory",
            "remember",
            "learning",
        ),
    }

    def match(
        self,
        goal: str,
        capabilities: list[Capability],
    ) -> list[Capability]:

        text = normalize(goal)

        scored = []

        for capability in capabilities:

            haystack = normalize(
                capability.name
            )

            score = 0

            for group in self.PREFERRED.values():

                for keyword in group:

                    if keyword in haystack:
                        score += 1

            for word in re.findall(
                r"[a-zA-Z_]+",
                text,
            ):

                if word in haystack:
                    score += 2

            if score:
                scored.append(
                    (
                        score,
                        capability,
                    )
                )

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            capability
            for _, capability
            in scored[:20]
        ]


# ============================================================
# ACTION MEMORY
# ============================================================

class ActionMemory:

    def seen(self, action: Action) -> bool:

        if not ACTION_MEMORY.exists():
            return False

        key = action.identity

        try:
            lines = ACTION_MEMORY.read_text(
                encoding="utf-8"
            ).splitlines()

            for line in reversed(lines[-10000:]):

                try:
                    record = json.loads(line)
                except Exception:
                    continue

                if record.get("identity") == key:
                    return True

        except Exception:
            return False

        return False

    def remember(
        self,
        action: Action,
        status: str,
        result: Any = None,
    ):

        record = {
            "timestamp": time.time(),
            "identity": action.identity,
            "action": action.action,
            "target": action.target,
            "goal": action.goal,
            "status": status,
            "result": result,
        }

        with ACTION_MEMORY.open(
            "a",
            encoding="utf-8",
        ) as f:

            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                    default=str,
                )
                + "\n"
            )


# ============================================================
# ACTING AI
# ============================================================

class ActingAI:

    def __init__(self):

        self.discovery = CapabilityDiscovery(
            ROOT
        )

        self.matcher = CapabilityMatcher()
        self.memory = ActionMemory()

        self.capabilities = []

    # --------------------------------------------------------
    # DISCOVER
    # --------------------------------------------------------

    def discover(self):

        self.capabilities = (
            self.discovery.scan()
        )

        return self.capabilities

    # --------------------------------------------------------
    # PLAN
    # --------------------------------------------------------

    def plan(self, goal: str):

        if not self.capabilities:
            self.discover()

        matches = self.matcher.match(
            goal,
            self.capabilities,
        )

        action = Action(
            action="pursue_goal",
            target=self._target(goal),
            goal=goal,
        )

        plan = {
            "goal": goal,
            "action": asdict(action),
            "identity": action.identity,
            "already_seen": self.memory.seen(
                action
            ),
            "candidate_capabilities": [
                asdict(cap)
                for cap in matches
            ],
        }

        log(
            "PLAN_CREATED",
            plan=plan,
        )

        return plan

    # --------------------------------------------------------
    # TARGET
    # --------------------------------------------------------

    def _target(self, goal: str):

        text = normalize(goal)

        if any(
            x in text
            for x in (
                "research",
                "research",
                "חקור",
                "מחקר",
                "semantic scholar",
                "literature",
                "meda",
            )
        ):
            return "research"

        if any(
            x in text
            for x in (
                "code",
                "coding",
                "קוד",
                "באג",
                "תקן",
            )
        ):
            return "coding"

        if any(
            x in text
            for x in (
                "business",
                "startup",
                "עסק",
                "משקיע",
            )
        ):
            return "business"

        return "general"

    # --------------------------------------------------------
    # ACT
    # --------------------------------------------------------

    def act(
        self,
        goal: str,
        approve: bool = False,
    ):

        plan = self.plan(goal)

        action = Action(
            **plan["action"]
        )

        if plan["already_seen"]:

            return {
                "status": "DEDUPLICATED",
                "identity": action.identity,
            }

        candidates = plan[
            "candidate_capabilities"
        ]

        if not candidates:

            self.memory.remember(
                action,
                "CAPABILITY_MISSING",
            )

            return {
                "status": "CAPABILITY_MISSING",
                "goal": goal,
                "message": (
                    "No existing capability "
                    "was discovered."
                ),
            }

        selected = candidates[0]

        result = self._execute(
            selected,
            goal,
        )

        self.memory.remember(
            action,
            result["status"],
            result,
        )

        return result

    # --------------------------------------------------------
    # EXECUTE EXISTING CAPABILITY
    # --------------------------------------------------------

    def _execute(
        self,
        capability,
        goal,
    ):

        try:

            module = importlib.import_module(
                capability["module"]
            )

            obj = getattr(
                module,
                capability["callable_name"],
            )

            if inspect.isclass(obj):

                try:
                    instance = obj(
                        root=ROOT
                    )
                except TypeError:
                    instance = obj()

                for method_name in (
                    "execute",
                    "run",
                    "act",
                    "investigate",
                    "handle",
                ):

                    method = getattr(
                        instance,
                        method_name,
                        None,
                    )

                    if callable(method):

                        try:
                            result = method(
                                goal
                            )
                        except TypeError:
                            result = method(
                                {"goal": goal}
                            )

                        log(
                            "REUSED_CAPABILITY",
                            capability=capability,
                        )

                        return {
                            "status": "EXECUTED",
                            "component": capability[
                                "name"
                            ],
                            "result": result,
                        }

            elif callable(obj):

                try:
                    result = obj(goal)
                except TypeError:
                    result = obj(
                        {"goal": goal}
                    )

                log(
                    "REUSED_CAPABILITY",
                    capability=capability,
                )

                return {
                    "status": "EXECUTED",
                    "component": capability[
                        "name"
                    ],
                    "result": result,
                }

        except Exception as exc:

            log(
                "EXECUTION_FAILED",
                capability=capability,
                error=repr(exc),
            )

            return {
                "status": "EXECUTION_FAILED",
                "error": repr(exc),
            }

        return {
            "status": "CAPABILITY_NOT_CALLABLE",
            "component": capability["name"],
        }


# ============================================================
# CLI
# ============================================================

def main():

    import sys

    ai = ActingAI()

    if len(sys.argv) < 2:

        print(
            "IMA Acting AI"
        )

        print(
            "discover | plan <goal> | act <goal>"
        )

        return 0

    command = sys.argv[1]

    if command == "discover":

        result = ai.discover()

        print(
            json.dumps(
                [
                    asdict(cap)
                    for cap in result
                ],
                ensure_ascii=False,
                indent=2,
            )
        )

        return 0

    goal = " ".join(
        sys.argv[2:]
    ).strip()

    if not goal:

        print(
            "ERROR: missing goal"
        )

        return 2

    if command == "plan":

        print(
            json.dumps(
                ai.plan(goal),
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )

        return 0

    if command == "act":

        print(
            json.dumps(
                ai.act(goal),
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )

        return 0

    print(
        f"ERROR: unknown command: {command}"
    )

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
