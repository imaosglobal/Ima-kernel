from pathlib import Path
import json
import pandas as pd
import numpy as np

LEARN = Path("learning")

test_path = LEARN / "conscious_continuation_HOLDOUT_test.csv"
test = pd.read_csv(test_path)

print("=" * 72)
print("CONSCIOUS CONTINUATION — UNTOUCHED HOLDOUT EVALUATION")
print("=" * 72)
print("TEST ROWS:", len(test))
print()

for h in ("H0", "H1"):
    p = LEARN / f"conscious_continuation_{h}_HOLDOUT_train_results.json"
    d = json.loads(p.read_text())

    print("-" * 72)
    print(h)
    print("-" * 72)

    print("TRAIN DATA SCORE :", d["data_score"])
    print("TRAIN RMSE       :", d["rmse"])
    print("TRAIN FITNESS    :", d["best_fitness"])
    print("TRAIN CONSTRAINT :", d["constraint_score"])
    print("EQUATIONS        :")

    for eq, terms in d["best_equations"].items():
        print(" ", eq, "=", terms)

    print()

print("=" * 72)
print("IMPORTANT")
print("=" * 72)
print("This script only inspects the trained models and untouched test data.")
print("It does NOT retrain either model.")
print()
print("TEST DATA:")
print(test.to_string(index=False))
print()
print("READY FOR MODEL SIMULATION.")
print("=" * 72)
