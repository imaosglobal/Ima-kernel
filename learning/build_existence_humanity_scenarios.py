from pathlib import Path
import csv

out = Path("learning/existence_humanity_scenarios.csv")

scales = [
    ("zero", 0, 0),
    ("one", 1, 1),
    ("two", 2, 1),
    ("three", 3, 1),
    ("ten", 10, 1),
    ("hundred", 100, 1),
    ("thousand", 1_000, 1),
    ("million", 1_000_000, 1),
    ("billion", 1_000_000_000, 1),
    ("infinity", "", 1),
]

rows = []
sid = 0

# Non-existence boundary
rows.append({
    "scenario_id": sid,
    "existence": 0,
    "humanity": 0,
    "population_scale": "zero",
    "population": 0,
    "boundary_infinity": 0,
})
sid += 1

# Existence without humanity
for label, count, _ in scales:
    if label == "infinity":
        rows.append({
            "scenario_id": sid,
            "existence": 1,
            "humanity": 0,
            "population_scale": label,
            "population": "",
            "boundary_infinity": 1,
        })
    else:
        rows.append({
            "scenario_id": sid,
            "existence": 1,
            "humanity": 0,
            "population_scale": label,
            "population": count,
            "boundary_infinity": 0,
        })
    sid += 1

# Humanity
for label, count, _ in scales:
    if label == "zero":
        continue

    rows.append({
        "scenario_id": sid,
        "existence": 1,
        "humanity": 1,
        "population_scale": label,
        "population": count,
        "boundary_infinity": int(label == "infinity"),
    })
    sid += 1

fields = [
    "scenario_id",
    "existence",
    "humanity",
    "population_scale",
    "population",
    "boundary_infinity",
]

with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

print("=" * 72)
print("EXISTENCE × HUMANITY SCENARIO MATRIX")
print("=" * 72)
print("SCENARIOS:", len(rows))
print("OUTPUT:", out)
print()

for r in rows:
    print(
        f"{r['scenario_id']:>2}: "
        f"existence={r['existence']} "
        f"humanity={r['humanity']} "
        f"population={r['population_scale']}"
    )

print("=" * 72)
print("SCENARIO MATRIX CREATED — NOT TRAINING DATA")
