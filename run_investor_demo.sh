#!/data/data/com.termux/files/usr/bin/bash

echo "=============================="
echo "        IMA INVESTOR DEMO"
echo "=============================="

echo ""
echo "[SYSTEM HEALTH]"

python3 - <<'PY'
from product.health.health_manager import health_report
PY

echo ""
echo "[MEMORY QUESTION]"

python3 - <<'PY'
from product.gateway.product_gateway import ask

r = ask("מה למדת ממני?")
PY

echo ""
echo "[FILES]"

echo "Vision:"
test -f docs/vision.md && echo OK

echo "Architecture:"
test -f investor/architecture_diagram.md && echo OK

echo "Governance:"
test -f governance/learning_policy.json && echo OK

echo ""
echo "=============================="
echo "IMA DEMO COMPLETE"
echo "=============================="
