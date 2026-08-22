from pathlib import Path

p=Path("founder/core/founder_core.py")
text=p.read_text()

text=text.replace(
"from founder.executive_ai.memory.memory_bridge import build_memory_context",
"from founder.executive_ai.memory.memory_bridge import enrich_answer"
)

text=text.replace(
"memory = build_memory_context()",
"memory = enrich_answer('founder_cycle', [])"
)

p.write_text(text)

