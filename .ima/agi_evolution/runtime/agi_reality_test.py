from pathlib import Path
import importlib.util

ROOT=Path(".ima/agi_evolution")

tests=[
"reasoning/reasoning_engine.py",
"autonomy/autonomy_engine.py",
"business_intelligence/business_engine.py",
"finance/finance_engine.py",
"persona_engine/persona_engine.py",
"self_improvement/self_improvement_engine.py"
]


print("=== IMA AGI REALITY TEST ===")

for t in tests:
    p=ROOT/t
    if p.exists():
        print("[OK]",t)
    else:
        print("[MISS]",t)

print("=== END ===")
