import csv
from pathlib import Path

src = Path("learning/conscious_continuation_meda_numeric.csv")

rows = []
with src.open(encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows.append(r)

if len(rows) < 10:
    raise SystemExit(f"Not enough rows: {len(rows)}")

# Deterministic chronological split.
# Train = first 70%, test = final 30%.
n = len(rows)
cut = max(1, int(n * 0.70))

train = rows[:cut]
test = rows[cut:]

fields = list(rows[0].keys())

for name, data in [
    ("conscious_continuation_HOLDOUT_train.csv", train),
    ("conscious_continuation_HOLDOUT_test.csv", test),
]:
    p = Path("learning") / name
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(data)

print("=" * 72)
print("CONSCIOUS CONTINUATION HOLDOUT DATASET")
print("=" * 72)
print("TOTAL :", len(rows))
print("TRAIN :", len(train))
print("TEST  :", len(test))
print("SPLIT :", cut, "/", n)
print()
print("TRAIN:", Path("learning/conscious_continuation_HOLDOUT_train.csv"))
print("TEST :", Path("learning/conscious_continuation_HOLDOUT_test.csv"))
print("=" * 72)
