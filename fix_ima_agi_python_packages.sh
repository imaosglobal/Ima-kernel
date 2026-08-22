#!/data/data/com.termux/files/usr/bin/bash

ROOT=".ima/agi_evolution"

echo "=== FIX IMA AGI PYTHON PACKAGES ==="

mkdir -p $ROOT

touch $ROOT/__init__.py

for d in \
reasoning \
autonomy \
persona_engine \
self_improvement \
business_intelligence \
finance \
connectors \
runtime
do
    touch "$ROOT/$d/__init__.py"
done


cat > $ROOT/runtime/agi_integration_test.py <<'PY'
from pathlib import Path
import sys

ROOT=Path(".ima/agi_evolution").resolve()

sys.path.insert(0,str(ROOT))


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
    except Exception as e:

PY


python3 $ROOT/runtime/agi_integration_test.py

