from pathlib import Path
import json
import sys

import numpy as np
import pandas as pd

sys.path.insert(
    0,
    str(Path("external/MEDA/skills/meda/scripts").resolve())
)

from data_fit import simulate_system


BASE = Path("learning")

TEST = BASE / "conscious_continuation_HOLDOUT_test.csv"

MODELS = {
    "H0": BASE / "conscious_continuation_H0_HOLDOUT_train_results.json",
    "H1": BASE / "conscious_continuation_H1_HOLDOUT_train_results.json",
}


def evaluate_model(name, result_path):

    result = json.loads(result_path.read_text())

    equations = result["best_equations"]

    variables = [
        eq[1:-3]
        for eq in equations
        if eq.startswith("d") and eq.endswith("/dt")
    ]

    df = pd.read_csv(TEST)

    missing = [v for v in variables if v not in df.columns]

    if missing:
        raise RuntimeError(
            f"{name}: missing variables: {missing}"
        )

    # Initial condition from first untouched holdout row.
    y0 = df[variables].iloc[0].to_numpy(dtype=float)

    t = df["t"].to_numpy(dtype=float)

    print()
    print("=" * 72)
    print(f"{name} — UNTOUCHED HOLDOUT SIMULATION")
    print("=" * 72)

    print("Variables:", variables)
    print("n_variables:", len(variables))
    print("n_test_rows:", len(df))
    print("Initial state:", y0)
    print("Time:", t)

    trajectory, status = simulate_system(
        equations,
        variables,
        y0,
        t,
    )

    print()
    print("INTEGRATION STATUS:", status)

    if trajectory is None:
        print("RESULT: FAILED")

        return {
            "model": name,
            "status": status,
            "holdout_rmse": None,
        }

    trajectory = np.asarray(trajectory, dtype=float)

    print("RAW TRAJECTORY SHAPE:", trajectory.shape)

    # simulate_system explicitly returns:
    # (n_variables, n_points)
    expected_shape = (len(variables), len(t))

    if trajectory.shape != expected_shape:
        raise RuntimeError(
            f"{name}: unexpected trajectory shape "
            f"{trajectory.shape}; expected {expected_shape}"
        )

    # Convert to:
    # (n_points, n_variables)
    predicted = trajectory.T

    actual = df[variables].to_numpy(dtype=float)

    print()
    print("PREDICTED TRAJECTORY")
    print("-" * 72)

    for i, ti in enumerate(t):

        parts = []

        for j, variable in enumerate(variables):
            parts.append(
                f"{variable}={predicted[i, j]: .6f}"
            )

        print(
            f"t={ti:>5.1f} | "
            + " | ".join(parts)
        )

    # Element-wise error.
    error = predicted - actual

    rmse_per_variable = np.sqrt(
        np.mean(error ** 2, axis=0)
    )

    overall_rmse = float(
        np.sqrt(np.mean(error ** 2))
    )

    print()
    print("ACTUAL HOLDOUT")
    print("-" * 72)

    for i, ti in enumerate(t):

        parts = []

        for j, variable in enumerate(variables):
            parts.append(
                f"{variable}={actual[i, j]: .6f}"
            )

        print(
            f"t={ti:>5.1f} | "
            + " | ".join(parts)
        )

    print()
    print("RMSE BY VARIABLE")
    print("-" * 72)

    for variable, value in zip(
        variables,
        rmse_per_variable
    ):
        print(
            f"{variable:>24}: {value:.6f}"
        )

    print()
    print("OVERALL HOLDOUT RMSE:", f"{overall_rmse:.6f}")

    result_out = {
        "model": name,
        "training_result": str(result_path),
        "holdout_data": str(TEST),
        "retrained": False,
        "variables": variables,
        "integration_status": status,
        "trajectory_shape_raw": list(trajectory.shape),
        "trajectory_shape_normalized": list(predicted.shape),
        "holdout_rows": len(df),
        "holdout_rmse": overall_rmse,
        "rmse_per_variable": {
            variable: float(value)
            for variable, value in zip(
                variables,
                rmse_per_variable
            )
        },
        "predicted": predicted.tolist(),
        "actual": actual.tolist(),
    }

    out = (
        BASE
        / f"conscious_continuation_{name}_HOLDOUT_simulation.json"
    )

    out.write_text(
        json.dumps(
            result_out,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print()
    print("SAVED:", out)

    return result_out


results = []

for name, path in MODELS.items():
    results.append(
        evaluate_model(name, path)
    )


print()
print("=" * 72)
print("HOLDOUT SIMULATION COMPLETE")
print("=" * 72)

for r in results:
    print(
        f"{r['model']}: "
        f"status={r['integration_status']} "
        f"RMSE={r['holdout_rmse']}"
    )

print()
print("NO RETRAINING PERFORMED.")
print("TEST ROWS REMAINED UNTOUCHED.")
print("=" * 72)
