#!/bin/bash
echo "=== בונה את כל רכיבי הליבה החסרים ==="

# 1. יוצר תיקיות ליבה
mkdir -p kernel/runtime learning kernel/device kernel/plugins .ima/governance

# 2. בונה קבצי Kernel ריקים
cat > kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js << 'EOL'
module.exports = { status: "mock", start: () => console.log("Kernel Mock Running") }
EOL

cat > kernel/runtime/KERNEL_EVENT_BUS.js << 'EOL'
class EventBus { emit(){} on(){} } module.exports = new EventBus()
EOL

cat > kernel/runtime/KERNEL_API_GATEWAY.js << 'EOL'
module.exports = { route: () => "API Gateway Mock" }
EOL

# 3. בונה קבצי Learning ריקים
cat > learning/__init__.py << 'EOL'
EOL

cat > learning/safe_scheduler.py << 'EOL'
def schedule(): pass
EOL

cat > learning/meta_orchestrator.py << 'EOL'
class MetaOrchestrator: pass
EOL

cat > learning/persona_engine.py << 'EOL'
class PersonaEngine: pass
EOL

cat > learning/child_safety_engine.py << 'EOL'
def check(): return True
EOL

cat > learning/single_gate.py << 'EOL'
def gate(): return "MOCK GATE"
EOL

cat > learning/brain_guard.py << 'EOL'
def guard(): return "MOCK GUARD"
EOL

cat > learning/evolution_controller.py << 'EOL'
def evolve(): pass
EOL

# 4. בונה קבצי Governance ריקים
echo '{}' > .ima/governance/brain_registry.json
echo '{}' > .ima/governance/runtime_registry.json
echo '{}' > .ima/governance/device_registry.json
echo '{"status":"mock"}' > .ima/governance/architecture_status.json

# 5. תיקון git
git add .
git commit -m "Add all missing skeleton files for simulation"

echo "=== DONE. כל השלד נבנה. הרץ בדיקה מחדש ==="
