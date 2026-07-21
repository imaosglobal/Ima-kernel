#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA GLOBAL BUILDER ==="

echo "[1] Git snapshot"

git status

git add .
git commit -m "IMA snapshot before global architecture sync" || true


echo "[2] Verify brain"

mkdir -p .ima/governance

if [ ! -f learning/brain_guard.py ]; then
echo "Missing brain guard"
exit 1
fi


python3 - <<'PY'
from learning.brain_guard import verify_brain
verify_brain("learning/meta_orchestrator.py")
print("BRAIN LOCK OK")
PY


echo "[3] Creating missing product layers"


mkdir -p \
users \
memory \
safety \
devices \
deployment \
product


create_file(){

FILE=$1
CONTENT=$2

if [ ! -f "$FILE" ]; then
echo "$CONTENT" > "$FILE"
echo "CREATED $FILE"
else
echo "EXISTS $FILE"
fi

}


create_file product/README.md \
"IMA PRODUCT RUNTIME"

create_file users/README.md \
"IMA USER IDENTITY LAYER"

create_file memory/README.md \
"IMA MEMORY ISOLATION LAYER"

create_file safety/README.md \
"IMA SAFETY LAYER"

create_file devices/README.md \
"IMA DEVICE CONNECTIVITY LAYER"

create_file deployment/README.md \
"IMA DEPLOYMENT LAYER"


echo "[4] Create global registry"


cat > .ima/governance/global_architecture_registry.json <<EOF
{
 "system":"IMA",
 "brain":"learning/meta_orchestrator.py",
 "orchestrator":"learning/meta_orchestrator.py",
 "layers":{
   "product":"product",
   "users":"users",
   "memory":"memory",
   "safety":"safety",
   "devices":"devices",
   "deployment":"deployment"
 },
 "policy":[
   "single_brain_only",
   "single_orchestrator_only",
   "no_duplicate_creation"
 ]
}
EOF


echo "[5] Run verification"


python3 learning/module_registry.py

python3 ima_full_system_check.py


echo "[6] Git sync"


git add .

git commit -m "IMA global product architecture sync" || true

git tag -a IMA_GLOBAL_PRODUCT_BASELINE_v1 \
-m "IMA global product baseline with canonical architecture" || true


echo "=== COMPLETE ==="

git status

git tag --list | grep IMA

