import json
import copy
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPTS = Path("external/MEDA/skills/meda/scripts").resolve()
sys.path.insert(0, str(SCRIPTS))

from data_fit import simulate_system

BASE = Path("learning")
TRAIN_RESULT = BASE / "conscious_continuation_H1_HOLDOUT_train_results.json"
TEST = BASE / "conscious_continuation_HOLDOUT_test.csv"

ORIGINAL = json.loads(TRAIN_RESULT.read_text())
ORIGINAL_EQ = ORIGINAL["best_equations"]

TARGETS = [
    ("dstimulus/dt", "conscious_continuation^2"),
    ("dstimulus/dt", "confidence*conscious_continuation"),
    ("dconfidence/dt", "conscious_continuation*word_count"),
    ("dword_count/dt", "conscious_continuation^2"),
]

df = pd.read_csv(TEST)

def evaluate(label, equations):
    variables = [
        eq[1:-3]
        for eq in equations
        if eq.startswith("d") and eq.endswith("/dt")
    ]

    y0 = df[variables].iloc[0].to_numpy(dtype=float)
    t = df["t"].to_numpy(dtype=float)
    actual = df[variables].to_numpy(dtype=float)

    trajectory, status = simulate_system(
        equations,
        variables,
        y0,
        t,
    )

    print()
    print("=" * 72)
    print(label)
    print("=" * 72)
    print("STATUS:", status)

    if trajectory is None:
        print("RESULT: INTEGRATION FAILED")
        return {
            "label": label,
            "status": status,
            "holdout_rmse": None,
        }

    # Correct orientation: simulate_system returns (n_vars, n_points)
    if trajectory.shape == (len(variables), len(t)):
        trajectory = trajectory.T

    if trajectory.shape != actual.shape:
        raise RuntimeError(
            f"{label}: trajectory shape {trajectory.shape} "
            f"!= actual shape {actual.shape}"
        )

    error = trajectory - actual
    variable_rmse = np.sqrt(np.mean(error ** 2, axis=0))
    overall_rmse = float(np.sqrt(np.mean(error ** 2)))

    print()
    print("RMSE BY VARIABLE")
    print("-" * 72)

    for v, r in zip(variables, variable_rmse):
        print(f"{v:32} {r:.6f}")

    print()
    print(f"OVERALL HOLDOUT RMSE: {overall_rmse:.6f}")

    return {
        "label": label,
        "status": status,
        "variables": variables,
        "holdout_rmse": overall_rmse,
        "rmse_by_variable": {
            v: float(r)
            for v, r in zip(variables, variable_rmse)
        },
        "predicted": trajectory.tolist(),
        "actual": actual.tolist(),
    }


results = []

# Baseline
results.append(
    evaluate(
        "H1 BASELINE — ALL TERMS",
        copy.deepcopy(ORIGINAL_EQ),
    )
)

# One-at-a-time ablations
for equation, term in TARGETS:
    equations = copy.deepcopy(ORIGINAL_EQ)

    if term not in equations.get(equation, {}):
        print()
        print("MISSING TARGET:", equation, term)
        continue

    del equations[equation][term]

    # Remove empty equations defensively
    equations = {
        k: v for k, v in equations.items()
        if v
    }

    label = f"ABLATE: {equation} <- {term}"

    results.append(
        evaluate(label, equations)
    )

# All four removed together
equations = copy.deepcopy(ORIGINAL_EQ)

for equation, term in TARGETS:
    equations.get(equation, {}).pop(term, None)

equations = {
    k: v for k, v in equations.items()
    if v
}

results.append(
    evaluate(
        "ABLATE ALL FOUR HIGH-RISK TERMS",
        equations,
    )
)

out = BASE / "conscious_continuation_H1_term_ablation.json"

out.write_text(
    json.dumps(
        {
            "source_model": str(TRAIN_RESULT),
            "holdout": str(TEST),
            "retrained": False,
            "targets": TARGETS,
            "results": results,
        },
        indent=2,
        ensure_ascii=False,
    ),
    encoding="utf-8",
)

print()
print("=" * 72)
print("ABLATION SUMMARY")
print("=" * 72)

for r in results:
    print(
        f"{r['label']}: "
        f"status={r['status']} "
        f"RMSE={r.get('holdout_rmse')}"
    )

print()
print("SAVED:", out)
print("NO RETRAINING WAS PERFORMED.")
print("HOLDOUT DATA WAS NOT MODIFIED.")
print("=" * 72)
