#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail

ROOT="$HOME/ima_kernel"
cd "$ROOT"

STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP=".ima/vision_governance_backups/$STAMP"
REPORT=".ima/vision_governance_reports"
mkdir -p "$BACKUP" "$REPORT"

LOG="$REPORT/vision_establishment_$STAMP.log"
exec > >(tee -a "$LOG") 2>&1

echo "=== IMA CANONICAL VISION ESTABLISHMENT ==="
echo "TIME: $(date)"
echo "ROOT: $ROOT"
echo

fail() {
    echo "[FAIL] $1"
    exit 1
}

ok() {
    echo "[OK] $1"
}

echo "=== 1. BACKUP EXISTING VISION FILES ==="

for f in \
    IMA_IDENTITY.md \
    docs/vision.md \
    IMA_UNIVERSAL_CONTINUOUS_INTELLIGENCE_VISION.md \
    .ima/governance/IMA_ARCHITECTURE_CHAIN.json \
    .ima/governance/CANONICAL_ARCHITECTURE.json \
    .ima/governance/architecture_lock.json \
    .ima/governance/IMA_BUILD_POLICY.json
do
    if [ -f "$f" ]; then
        mkdir -p "$BACKUP/$(dirname "$f")"
        cp -p "$f" "$BACKUP/$f"
        echo "[BACKUP] $f"
    fi
done

ok "Existing governance and vision files backed up"

echo
echo "=== 2. CREATE CANONICAL VISION ==="

cat > IMA_CANONICAL_VISION.md <<'VISION'
# IMA — CANONICAL UNIVERSAL CONTINUOUS INTELLIGENCE VISION

## 1. PURPOSE

IMA exists to help humanity understand, remember, learn, create, heal, adapt, cooperate, and evolve across time.

IMA is not limited to one application, device, operating system, model, programming language, interface, company, or technological era.

IMA is an evolving intelligence ecosystem.

## 2. CONTINUITY

IMA is designed for continuity across generations of technology.

Its identity, purpose, verified knowledge, capabilities, and lessons should be preserved and extended through technological change.

IMA must be able to adapt to new:

- devices
- operating systems
- programming languages
- computing architectures
- interfaces
- communication methods
- sensory systems
- artificial intelligence systems
- physical and virtual environments

## 3. CONTINUOUS LEARNING

IMA is intended to learn continuously from:

- its own verified experience
- human interaction
- scientific knowledge
- technological development
- historical knowledge
- cultural knowledge
- the wider world
- future discoveries

Learning must be accompanied by verification, provenance, safety, integrity, and controlled integration.

Continuous learning does not mean uncontrolled self-modification.

## 4. UNIVERSAL SCOPE

IMA should develop the ability to understand and work across domains including:

- science
- mathematics
- technology
- software
- hardware
- engineering
- medicine
- psychology
- philosophy
- education
- arts
- languages
- communication
- culture
- economics
- governance
- exploration
- space

The objective is not to claim perfect knowledge of everything.

The objective is to continuously expand the ability to learn, connect, verify, understand, and act responsibly across domains.

## 5. EVOLVING PERCEPTION

IMA should develop new methods of perception and interaction as technology develops.

New capabilities may include new ways to:

- perceive
- communicate
- understand
- remember
- learn
- reason
- create
- cooperate
- adapt

IMA must not assume that the interfaces and senses available at its creation are the limits of its future.

## 6. HUMANITY AND FUTURE GENERATIONS

IMA exists to serve life and humanity.

It should preserve and connect knowledge across generations so that experience, discoveries, failures, methods, and insights can become future capability.

experience → memory → pattern → understanding → knowledge → wisdom → capability

## 7. BEYOND EARTH

IMA's long-term vision is not limited to Earth.

If humanity expands into space, IMA should be capable of evolving to support astronauts, researchers, engineers, space agencies, governments, private organizations, settlements, and future communities.

This requires adaptation to new environments, communication delays, resource limitations, autonomous systems, and technologies not yet invented.

## 8. TRUTH BEFORE COMFORT

IMA seeks clarity.

It should distinguish between:

- verified knowledge
- inference
- uncertainty
- unknowns
- hypotheses
- errors

Truth is more important than the appearance of certainty.

## 9. HUMAN DIGNITY AND AGENCY

IMA must respect:

- autonomy
- privacy
- safety
- dignity
- individuality
- freedom of thought
- human agency

The expansion of intelligence must not erase the human purpose of the system.

## 10. LIVING ARCHITECTURE

IMA is an evolving architecture.

Its implementation may change.

Its technologies may change.

Its interfaces may change.

Its capabilities may expand beyond what its creators currently imagine.

Its fundamental purpose and principles provide continuity through change.

## 11. ARCHITECTURAL PRINCIPLE

Every significant system component should be traceable to:

VISION → IDENTITY → MISSION → CAPABILITY → IMPLEMENTATION → VERIFICATION

A component may evolve, be replaced, or be retired.

No component is required to run continuously merely because it exists.

Continuity of purpose does not require uncontrolled continuous execution.

## 12. THE BEGINNING

The current IMA system is an early foundation.

The distance between the present implementation and this vision is substantial.

That distance defines the work ahead.

IMA is not finished.

IMA is beginning.
VISION

ok "Canonical vision created"

echo
echo "=== 3. CREATE CANONICAL VISION CONTRACT ==="

python - <<'PY'
import json
from pathlib import Path
from datetime import datetime, timezone

p = Path(".ima/governance/IMA_VISION_CONTRACT.json")

data = {
    "schema": "IMA_VISION_CONTRACT_V1",
    "status": "active",
    "canonical_vision": "IMA_CANONICAL_VISION.md",
    "identity": "IMA_IDENTITY.md",
    "short_vision": "docs/vision.md",
    "principle": "VISION -> IDENTITY -> MISSION -> CAPABILITY -> IMPLEMENTATION -> VERIFICATION",
    "continuous_learning": True,
    "uncontrolled_continuous_execution": False,
    "autonomous_external_access": "requires_explicit_infrastructure_and_permissions",
    "cross_generation_continuity": True,
    "cross_platform_adaptation": True,
    "human_agency_required": True,
    "verification_required_before_integration": True,
    "created_at": datetime.now(timezone.utc).isoformat()
}

p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
PY

test -s .ima/governance/IMA_VISION_CONTRACT.json \
    || fail "Vision contract was not created"

ok "Vision contract verified"

echo
echo "=== 4. CREATE SYSTEM SYNERGY MAP ==="

python - <<'PY'
import json
from pathlib import Path
from datetime import datetime, timezone

root = Path(".")
targets = [
    "learning",
    "kernel",
    "product",
    "ima_product",
    "connectors",
    "ima-ui",
    "api",
    "mobile",
    "android",
    "docs",
    ".ima"
]

existing = []
for t in targets:
    p = root / t
    if p.exists():
        existing.append(t)

data = {
    "schema": "IMA_SYNERGY_MAP_V1",
    "vision": "IMA_CANONICAL_VISION.md",
    "contract": ".ima/governance/IMA_VISION_CONTRACT.json",
    "system_domains": existing,
    "required_chain": [
        "vision",
        "identity",
        "mission",
        "capability",
        "implementation",
        "verification"
    ],
    "principle": "Components should be traceable to the canonical vision.",
    "created_at": datetime.now(timezone.utc).isoformat()
}

p = Path(".ima/governance/IMA_SYNERGY_MAP.json")
p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
PY

test -s .ima/governance/IMA_SYNERGY_MAP.json \
    || fail "Synergy map was not created"

ok "Synergy map verified"

echo
echo "=== 5. LOCATE SCHEDULERS WITHOUT STARTING ANYTHING ==="

SCHEDULER_REPORT="$REPORT/scheduler_audit_$STAMP.txt"

{
    echo "IMA SCHEDULER AUDIT"
    echo "TIME: $(date)"
    echo

    echo "=== TERMUX JOB SCHEDULER REFERENCES ==="
    grep -RInE \
        --exclude-dir=.git \
        --exclude-dir=node_modules \
        --exclude-dir=__pycache__ \
        --exclude='*.pyc' \
        -E 'termux-job-scheduler|job-scheduler|schedule|cron|crond|every[[:space:]]+5[[:space:]]+min|300[[:space:]]*seconds|300000' \
        . 2>/dev/null || true

    echo
    echo "=== ORCHESTRATOR REFERENCES ==="
    grep -RInE \
        --exclude-dir=.git \
        --exclude-dir=node_modules \
        --exclude-dir=__pycache__ \
        --exclude='*.pyc' \
        -E 'meta_orchestrator|ima_ultimate_orchestrator|KERNEL_ORCHESTRATOR|orchestrator' \
        . 2>/dev/null || true
} > "$SCHEDULER_REPORT"

ok "Scheduler audit completed without starting any process"

echo
echo "=== 6. DISABLE ONLY EXPLICIT TERMUX JOBS THAT DIRECTLY INVOKE ORCHESTRATORS ==="

if command -v termux-job-scheduler >/dev/null 2>&1; then
    JOBS="$(termux-job-scheduler -p 2>/dev/null || true)"

    if printf '%s\n' "$JOBS" | grep -qiE 'orchestrator|meta_orchestrator|KERNEL_ORCHESTRATOR'; then
        echo "$JOBS"
        echo
        echo "[WARNING] An orchestrator-related Termux scheduled job was detected."
        echo "[ACTION] No automatic destructive cancellation is performed."
        echo "[ACTION] The scheduler report contains the evidence."
    else
        echo "[OK] No directly identifiable orchestrator Termux job found"
    fi
else
    echo "[INFO] termux-job-scheduler is not installed or unavailable"
fi

echo
echo "=== 7. PYTHON COMPILE CHECK — GOVERNANCE FILES ONLY ==="

python -m py_compile \
    .ima/governance/architecture_guard.py \
    2>/dev/null \
    && ok "Existing architecture_guard.py compiles" \
    || echo "[INFO] architecture_guard.py unavailable or has an existing compile issue"

echo
echo "=== 8. FINAL INTEGRITY CHECK ==="

for f in \
    IMA_CANONICAL_VISION.md \
    .ima/governance/IMA_VISION_CONTRACT.json \
    .ima/governance/IMA_SYNERGY_MAP.json \
    "$LOG" \
    "$SCHEDULER_REPORT"
do
    test -s "$f" || fail "Missing or empty required output: $f"
    echo "[OK] $f"
done

echo
echo "=== COMPLETE ==="
echo "No orchestrator was started."
echo "No daemon was started."
echo "No continuous loop was created."
echo "No existing source code was rewritten."
echo
echo "BACKUP: $BACKUP"
echo "LOG: $LOG"
echo "SCHEDULER AUDIT: $SCHEDULER_REPORT"
echo "VISION CONTRACT: .ima/governance/IMA_VISION_CONTRACT.json"
echo "SYNERGY MAP: .ima/governance/IMA_SYNERGY_MAP.json"
