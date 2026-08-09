from pathlib import Path
import sys

ROOT=Path(".ima/agi_evolution").resolve()
sys.path.insert(0,str(ROOT))

print("=== IMA AGI CAPABILITY PROBE ===")

modules=[
("reasoning.reasoning_engine","ReasoningEngine"),
("autonomy.autonomy_engine","AutonomyEngine"),
("persona_engine.persona_engine","PersonaEngine"),
("self_improvement.self_improvement_engine","SelfImprovement")
]

for module,cls in modules:
    try:
        m=__import__(module,fromlist=[cls])
        c=getattr(m,cls)
        obj=c()

        methods=[
            x for x in dir(obj)
            if not x.startswith("_")
        ]

        print("\n[MODULE]",module)
        print("[CLASS]",cls)
        print("[METHODS]",methods[:15])

    except Exception as e:
        print("[ERROR]",module,e)

print("\n=== END ===")
