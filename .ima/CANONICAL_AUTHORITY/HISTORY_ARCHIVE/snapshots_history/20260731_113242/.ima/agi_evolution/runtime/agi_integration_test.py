from pathlib import Path
import sys

ROOT=Path(".ima/agi_evolution").resolve()

sys.path.insert(0,str(ROOT))

print("=== IMA AGI INTEGRATION TEST ===")

tests=[
("reasoning.reasoning_engine","ReasoningEngine"),
("autonomy.autonomy_engine","AutonomyEngine"),
("persona_engine.persona_engine","PersonaEngine"),
("self_improvement.self_improvement_engine","SelfImprovement")
]

for module,cls in tests:
    try:
        mod=__import__(module,fromlist=[cls])
        obj=getattr(mod,cls)()
        print("[ACTIVE]",module,cls)
    except Exception as e:
        print("[FAIL]",module,e)

print("=== END ===")
