#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/ima_kernel"
MEDA="$ROOT/external/MEDA"
LEARN="$ROOT/learning"

echo "============================================================"
echo "CONSCIOUS CONTINUATION — HOLDOUT TRAINING"
echo "============================================================"

# ============================================================
# 1. Create H0/H1 train CSVs from their actual source datasets
# ============================================================

python3 - <<'PY'
import csv
from pathlib import Path

learn = Path.home() / "ima_kernel" / "learning"

for h in ("H0", "H1"):
    src = learn / f"conscious_continuation_{h}.csv"
    dst = learn / f"conscious_continuation_{h}_HOLDOUT_train.csv"

    if not src.exists():
        raise SystemExit(f"MISSING SOURCE: {src}")

    with src.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if len(rows) < 10:
        raise SystemExit(f"{h}: not enough rows: {len(rows)}")

    cut = max(1, int(len(rows) * 0.70))
    train = rows[:cut]

    with dst.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(train)

    print(f"{h}: TOTAL={len(rows)} TRAIN={len(train)} TEST={len(rows)-len(train)}")
    print(f"    TRAIN CSV: {dst}")
PY

# ============================================================
# 2. Create train-only setups
# ============================================================

python3 - <<'PY'
from pathlib import Path
import re

learn = Path.home() / "ima_kernel" / "learning"

for h in ("H0", "H1"):
    src = learn / f"conscious_continuation_{h}_setup.yaml"
    dst = learn / f"conscious_continuation_{h}_HOLDOUT_train_setup.yaml"
    train_csv = learn / f"conscious_continuation_{h}_HOLDOUT_train.csv"

    text = src.read_text(encoding="utf-8")

    text2, n = re.subn(
        r"(?m)^data_file:\s*.*$",
        f"data_file: {train_csv}",
        text,
        count=1,
    )

    if n != 1:
        raise SystemExit(f"{h}: could not replace data_file")

    dst.write_text(text2, encoding="utf-8")

    print("CREATED:", dst)
    print("DATA:", train_csv)
PY

# ============================================================
# 3. Validate H0
# ============================================================

echo
echo "============================================================"
echo "VALIDATING H0 TRAIN"
echo "============================================================"

python3 "$MEDA/skills/meda/scripts/validation.py" \
  --setup "$LEARN/conscious_continuation_H0_HOLDOUT_train_setup.yaml" \
  --problem "$LEARN/conscious_continuation_H0_problem.json" \
  --data "$LEARN/conscious_continuation_H0_HOLDOUT_train.csv"

# ============================================================
# 4. Train H0
# ============================================================

echo
echo "============================================================"
echo "RUNNING H0 — TRAIN ONLY"
echo "============================================================"

python3 "$MEDA/skills/meda/scripts/main.py" \
  --mode data_anchored \
  --data "$LEARN/conscious_continuation_H0_HOLDOUT_train.csv" \
  --setup "$LEARN/conscious_continuation_H0_HOLDOUT_train_setup.yaml" \
  --problem "$LEARN/conscious_continuation_H0_problem.json" \
  --output "$LEARN/conscious_continuation_H0_HOLDOUT_train_results.json"

# ============================================================
# 5. Validate H1
# ============================================================

echo
echo "============================================================"
echo "VALIDATING H1 TRAIN"
echo "============================================================"

python3 "$MEDA/skills/meda/scripts/validation.py" \
  --setup "$LEARN/conscious_continuation_H1_HOLDOUT_train_setup.yaml" \
  --problem "$LEARN/conscious_continuation_H1_problem.json" \
  --data "$LEARN/conscious_continuation_H1_HOLDOUT_train.csv"

# ============================================================
# 6. Train H1
# ============================================================

echo
echo "============================================================"
echo "RUNNING H1 — TRAIN ONLY"
echo "============================================================"

python3 "$MEDA/skills/meda/scripts/main.py" \
  --mode data_anchored \
  --data "$LEARN/conscious_continuation_H1_HOLDOUT_train.csv" \
  --setup "$LEARN/conscious_continuation_H1_HOLDOUT_train_setup.yaml" \
  --problem "$LEARN/conscious_continuation_H1_problem.json" \
  --output "$LEARN/conscious_continuation_H1_HOLDOUT_train_results.json"

echo
echo "============================================================"
echo "HOLDOUT TRAINING COMPLETE"
echo "============================================================"

ls -lh \
  "$LEARN/conscious_continuation_H0_HOLDOUT_train_results.json" \
  "$LEARN/conscious_continuation_H1_HOLDOUT_train_results.json"

echo
echo "The 6-row test sets were NOT used for training."
echo "Next step: evaluate H0 and H1 on those untouched rows."
