from pathlib import Path
import shutil
from datetime import datetime
import py_compile

p = Path(".ima/research/ima_research_council.py")

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = p.parent / "backups" / f"ima_research_council_before_semantic_debug_{ts}.py"
backup.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(p, backup)

text = p.read_text(encoding="utf-8")

# Locate the exception handler in _run_agent.
old = '''        except Exception as exc:
            self.log(
                f"ERROR {agent_name} [{subquestion_id}] "
                f"{repr(exc)}"
            )

            return {
'''

new = '''        except Exception as exc:
            import traceback

            self.log(
                f"ERROR {agent_name} [{subquestion_id}] "
                f"{type(exc).__name__}: {exc}"
            )

            self.log(
                f"DEBUG agent_name={agent_name!r}"
            )

            self.log(
                f"DEBUG subquestion_id={subquestion_id!r}"
            )

            self.log(
                f"DEBUG registry_has_agent="
                f"{agent_name in self.registry.get('agents', {})}"
            )

            try:
                registry_cfg = self.registry.get(
                    "agents", {}
                ).get(agent_name)

                self.log(
                    f"DEBUG registry_config={registry_cfg!r}"
                )
            except Exception:
                self.log(
                    "DEBUG registry_config=<FAILED>"
                )

            self.log(
                "DEBUG FULL TRACEBACK:"
            )

            for line in traceback.format_exc().rstrip().splitlines():
                self.log(
                    f"DEBUG_TRACE {line}"
                )

            return {
'''

if old not in text:
    raise SystemExit(
        "ERROR: dispatcher exception handler not found"
    )

text = text.replace(old, new, 1)

p.write_text(text, encoding="utf-8")

py_compile.compile(
    str(p),
    doraise=True
)

print("=" * 78)
print("SEMANTIC SCHOLAR DISPATCH DIAGNOSTIC INSTALLED")
print("=" * 78)
print("BACKUP:", backup)
print("COMPILE: PASS")
print("=" * 78)
