from pathlib import Path
from collections import defaultdict
import json
import math

EVENTS = Path("learning/state_transition_events.jsonl")
MODEL = Path("learning/state_transition_model.json")


def load_events():
    if not EVENTS.exists():
        return []

    events = []

    with EVENTS.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                events.append(json.loads(line))
            except Exception:
                continue

    return events


def _transition_key(event):
    transition = event.get("transition")

    if transition:
        return (
            transition.get("from"),
            transition.get("to"),
        )

    # compatibility with V1
    transition_hypotheses = event.get(
        "transition_hypotheses",
        []
    )

    if transition_hypotheses:
        t = transition_hypotheses[0]

        return (
            t.get("from"),
            t.get("to"),
        )

    return (
        event.get("previous_state", {}).get("label"),
        event.get("state", {}).get("label"),
    )


def _factor_names(event):
    return {
        x.get("name")
        for x in event.get("factors", [])
        if x.get("name")
    }


def build_model(events=None):
    events = events if events is not None else load_events()

    transitions = defaultdict(int)
    factor_transition = defaultdict(int)
    factor_total = defaultdict(int)
    state_total = defaultdict(int)

    for event in events:

        previous, current = _transition_key(event)

        if not previous or not current:
            continue

        key = (previous, current)

        transitions[key] += 1
        state_total[previous] += 1

        factors = _factor_names(event)

        for factor in factors:
            factor_total[(previous, factor)] += 1
            factor_transition[(previous, factor, current)] += 1

    model = {
        "schema": "ima.state_transition_model.v1",
        "events_used": len(events),
        "transitions": {},
        "causal_candidates": {},
    }

    # ---------------------------------------------------------
    # Empirical transition probabilities
    # ---------------------------------------------------------

    for (previous, current), count in transitions.items():

        denominator = state_total[previous]

        probability = (
            count / denominator
            if denominator
            else 0.0
        )

        model["transitions"][
            f"{previous} -> {current}"
        ] = {
            "count": count,
            "probability": round(probability, 6),
        }

    # ---------------------------------------------------------
    # Factor-conditioned transition probabilities
    # ---------------------------------------------------------

    for (
        previous,
        factor,
        current
    ), count in factor_transition.items():

        denominator = factor_total[
            (previous, factor)
        ]

        probability = (
            count / denominator
            if denominator
            else 0.0
        )

        key = (
            f"{previous} + {factor} -> {current}"
        )

        model["causal_candidates"][key] = {
            "count": count,
            "probability": round(probability, 6),
        }

    return model


def save_model(model):
    MODEL.write_text(
        json.dumps(
            model,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def learn():
    events = load_events()
    model = build_model(events)

    save_model(model)

    return model


def report(model):
    print("=" * 72)
    print("IMA STATE TRANSITION LEARNING")
    print("=" * 72)

    print(
        "EVENTS:",
        model["events_used"]
    )

    print()
    print("EMPIRICAL TRANSITIONS:")

    for key, value in model["transitions"].items():
        print(
            f"  {key} | "
            f"n={value['count']} | "
            f"P={value['probability']}"
        )

    print()
    print("FACTOR-CONDITIONED TRANSITIONS:")

    for key, value in model[
        "causal_candidates"
    ].items():

        print(
            f"  {key} | "
            f"n={value['count']} | "
            f"P={value['probability']}"
        )

    print("=" * 72)


if __name__ == "__main__":
    model = learn()
    report(model)
