from pathlib import Path
import csv

out = Path("learning/existence_humanity_state_space.csv")

# Finite population scales.
# infinity is represented separately as a mathematical boundary,
# not as a physical population count.
population_scales = [
    ("zero", 0),
    ("one", 1),
    ("two", 2),
    ("three", 3),
    ("ten", 10),
    ("hundred", 100),
    ("thousand", 1_000),
    ("million", 1_000_000),
    ("billion", 1_000_000_000),
]

rows = []
t = 0

for existence in (0, 1):
    for humanity in (0, 1):
        for label, count in population_scales:

            # Population consistency:
            # no existence -> no actual individuals.
            if existence == 0 and count != 0:
                continue

            # No humanity -> population can represent non-human entities.
            # Humanity=1 requires existence and at least one human.
            if humanity == 1 and (existence == 0 or count == 0):
                continue

            rows.append({
                "state_id": t,
                "existence": existence,
                "humanity": humanity,
                "individual_count": count,
                "population_scale": label,
                "boundary_infinity": 0,
            })
            t += 1

# Explicit mathematical boundary.
rows.append({
    "state_id": t,
    "existence": 1,
    "humanity": 0,
    "individual_count": "",
    "population_scale": "infinity",
    "boundary_infinity": 1,
})

rows.append({
    "state_id": t + 1,
    "existence": 1,
    "humanity": 1,
    "individual_count": "",
    "population_scale": "infinity",
    "boundary_infinity": 1,
})

fields = [
    "state_id",
    "existence",
    "humanity",
    "individual_count",
    "population_scale",
    "boundary_infinity",
]

with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

print("=" * 72)
print("EXISTENCE × HUMANITY STATE SPACE")
print("=" * 72)
print("STATES:", len(rows))
print("FILE :", out)
print()
for r in rows:
    print(
        f"{r['state_id']:>2}: "
        f"existence={r['existence']} "
        f"humanity={r['humanity']} "
        f"population={r['population_scale']}"
    )
print("=" * 72)
print("IMPORTANT: this is a scenario/state-space matrix, NOT training data.")
