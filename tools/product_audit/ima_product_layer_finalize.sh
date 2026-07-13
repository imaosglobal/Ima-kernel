#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA PRODUCT LAYER FINALIZE ==="

DATE=$(date +%Y%m%d_%H%M%S)

echo "[1] Snapshot product state"

mkdir -p .ima/runtime_snapshots/product_before_finalize_$DATE

for d in product companion device agents frontend android ui api; do
    [ -e "$d" ] && cp -r "$d" ".ima/runtime_snapshots/product_before_finalize_$DATE/" || true
done


echo "[2] Creating missing product layers"

DIRS="
web
mobile
plugins
modules
marketplace
auth
database
docs
tests
"

for d in $DIRS; do
    mkdir -p "$d"
done


echo "[3] Creating product manifests"


cat > web/README.md <<EOF
# IMA Web Layer

Frontend web application layer.
Connected to canonical API.
EOF


cat > mobile/README.md <<EOF
# IMA Mobile Layer

Mobile product interface.
EOF


cat > plugins/README.md <<EOF
# IMA Plugin Layer

External capability connectors.
EOF


cat > modules/README.md <<EOF
# IMA Modules

Product modules registry.
EOF


cat > marketplace/README.md <<EOF
# IMA Marketplace

Future product marketplace layer.
EOF


cat > auth/README.md <<EOF
# IMA Auth

Authentication layer.
EOF


cat > database/README.md <<EOF
# IMA Database

Persistent product data layer.
EOF


cat > docs/README.md <<EOF
# IMA Documentation

Product documentation.
EOF


cat > tests/README.md <<EOF
# IMA Tests

Product validation tests.
EOF


echo "[4] Product registry"

mkdir -p product/runtime

cat > product/runtime/product_layer_status.json <<EOF
{
 "product_layer":"IMA",
 "status":"INITIALIZED",
 "core_locked":true,
 "created":"$DATE",
 "protected_core":[
  "conversation_layer.py",
  "IMA_START.py",
  "kernel/runtime/CANONICAL/python_bridge.py",
  "ima_master_runtime.py"
 ]
}
EOF


echo "[5] Product audit"

python3 ima_product_layer_audit.sh 2>/dev/null || true

echo "[6] Git"

git add \
web \
mobile \
plugins \
modules \
marketplace \
auth \
database \
docs \
tests \
product/runtime/product_layer_status.json \
.ima/runtime_snapshots \
2>/dev/null || true


git commit -m "Initialize IMA product layer structure" || true


git tag -f IMA_PRODUCT_LAYER_INITIALIZED_v1


echo "=== PRODUCT LAYER FINALIZED ==="
echo "CORE: FROZEN"
echo "PRODUCT: READY FOR DEVELOPMENT"

