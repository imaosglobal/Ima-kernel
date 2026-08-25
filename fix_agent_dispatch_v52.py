from pathlib import Path
import ast
import py_compile
import shutil
from datetime import datetime

p = Path(".ima/research/ima_research_council.py")
text = p.read_text(encoding="utf-8")

backup_dir = Path(".ima/research/backups")
backup_dir.mkdir(parents=True, exist_ok=True)

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = backup_dir / f"ima_research_council_before_dispatch_v52_{stamp}.py"
shutil.copy2(p, backup)

start = text.find("    def _agent(")

if start < 0:
    raise SystemExit("ERROR: def _agent() not found")

end = text.find("    def _run_agent(", start)

if end < 0:
    raise SystemExit("ERROR: def _run_agent() boundary not found")

new_agent = r'''    def _agent(self, agent_name):
        """
        V5.2 canonical agent dispatcher.

        Agents are resolved from the research agent directory by the
        adapter filename stored in agent_registry.json.

        This intentionally avoids:
            from agents.<module> import ...

        because ~/ima_kernel/agents may shadow
        .ima/research/agents.
        """

        import importlib.util
        import inspect
        from pathlib import Path

        registry_cfg = (
            self.registry
            .get("agents", {})
            .get(agent_name)
        )

        if not registry_cfg:
            raise KeyError(
                f"Agent {agent_name!r} missing from registry"
            )

        adapter = registry_cfg.get("adapter")

        if not adapter:
            raise KeyError(
                f"Agent {agent_name!r} has no adapter in registry"
            )

        research_dir = Path(__file__).resolve().parent
        agents_dir = research_dir / "agents"
        adapter_path = agents_dir / adapter

        self.log(
            f"DEBUG DISPATCH {agent_name} "
            f"adapter={adapter!r}"
        )

        self.log(
            f"DEBUG DISPATCH PATH {adapter_path}"
        )

        if not adapter_path.exists():
            raise FileNotFoundError(
                f"Agent adapter not found: {adapter_path}"
            )

        module_name = (
            f"ima_research_agent_{adapter_path.stem}"
        )

        spec = importlib.util.spec_from_file_location(
            module_name,
            str(adapter_path)
        )

        if spec is None or spec.loader is None:
            raise ImportError(
                f"Cannot create import spec for {adapter_path}"
            )

        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        class_map = {
            "MEDA": "MEDAAgent",
            "DEEP_RESEARCH": "DeepResearchAgent",
            "LITERATURE": "LiteratureAgent",
            "HYPOTHESIS": "HypothesisAgent",
            "CRITIC": "CriticAgent",
            "EVOLUTIONARY_SEARCH": "EvolutionaryAgent",
            "SEMANTIC_SCHOLAR": "SemanticScholarAgent",
        }

        class_name = class_map.get(agent_name)

        if not class_name:
            candidates = []

            for name, obj in vars(module).items():
                if (
                    inspect.isclass(obj)
                    and obj.__module__ == module.__name__
                    and name != "Agent"
                ):
                    candidates.append(obj)

            if len(candidates) != 1:
                raise RuntimeError(
                    f"Cannot uniquely resolve class for "
                    f"{agent_name}: "
                    f"{[c.__name__ for c in candidates]}"
                )

            agent_class = candidates[0]

        else:
            agent_class = getattr(module, class_name, None)

            if agent_class is None:
                raise AttributeError(
                    f"{class_name} not found in {adapter_path}"
                )

        self.log(
            f"DEBUG DISPATCH CLASS {agent_class.__name__}"
        )

        try:
            return agent_class(root=self.root)
        except TypeError:
            return agent_class()

'''

text = text[:start] + new_agent + text[end:]

# Ensure the version banner reflects the actual runtime.
text = text.replace(
    'self.log(\n            "IMA RESEARCH COUNCIL V4"\n        )',
    'self.log(\n            "IMA RESEARCH COUNCIL V5.2"\n        )',
    1
)

text = text.replace(
    'IMA_RESEARCH_COUNCIL_VERSION = "V5"',
    'IMA_RESEARCH_COUNCIL_VERSION = "V5.2"',
    1
)

text = text.replace(
    'IMA_RESEARCH_COUNCIL_ARCHITECTURE = "IMA_RESEARCH_COUNCIL_V5"',
    'IMA_RESEARCH_COUNCIL_ARCHITECTURE = "IMA_RESEARCH_COUNCIL_V5.2"',
    1
)

p.write_text(text, encoding="utf-8")

py_compile.compile(str(p), doraise=True)

# Direct dispatcher test without relying on the root-level `agents` package.
import sys

research_root = str(Path(".ima/research").resolve())
if research_root not in sys.path:
    sys.path.insert(0, research_root)

from ima_research_council import IMAResearchCouncil

council = IMAResearchCouncil(live_log=False)

print("=" * 78)
print("IMA RESEARCH COUNCIL V5.2 — DISPATCH FIX")
print("=" * 78)
print("BACKUP:", backup)
print("COMPILE: PASS")
print()

for name in [
    "LITERATURE",
    "MEDA",
    "HYPOTHESIS",
    "CRITIC",
    "DEEP_RESEARCH",
    "SEMANTIC_SCHOLAR",
]:
    try:
        agent = council._agent(name)
        print(
            f"{name}: PASS -> "
            f"{agent.__class__.__name__}"
        )
    except Exception as e:
        print(
            f"{name}: FAIL -> "
            f"{type(e).__name__}: {e}"
        )
        raise

print()
print("SEMANTIC_SCHOLAR DISPATCH: PASS")
print("VALIDATION: PASS")
print("=" * 78)
