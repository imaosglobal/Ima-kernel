from pathlib import Path
import json
import time

EVENTS = Path("learning/state_transition_events.jsonl")
OUTCOMES = Path("learning/state_transition_outcomes.jsonl")


def _read_events():
    if not EVENTS.exists():
        return []

    result = []

    with EVENTS.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            try:
                result.append(json.loads(line))
            except Exception:
                continue

    return result


def evaluate_event(event):
    prediction = event.get("prediction") or {}
    candidates = prediction.get("candidates") or []

    if not candidates:
        return {
            "status": "no_prediction"
        }

    predicted = candidates[0].get("state")

    actual = (
        event.get("outcome", {}).get("next_state")
        or event.get("next_state")
    )

    if not actual:
        return {
            "status": "awaiting_outcome",
            "predicted_state": predicted
        }

    correct = predicted == actual

    return {
        "status": "evaluated",
        "predicted_state": predicted,
        "actual_state": actual,
        "correct": correct,
        "probability": candidates[0].get("probability", 0.0),
    }


def record_outcome(event_id, actual_state):
    events = _read_events()

    for event in reversed(events):
        if event.get("_id") != event_id:
            continue

        evaluation = evaluate_event(
            {
                **event,
                "outcome": {
                    **event.get("outcome", {}),
                    "next_state": actual_state,
                    "observed": True,
                }
            }
        )

        record = {
            "_id": event_id,
            "time": time.time(),
            "actual_state": actual_state,
            **evaluation,
        }

        with OUTCOMES.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                ) + "\n"
            )

        return record

    return {
        "status": "event_not_found",
        "event_id": event_id,
    }


def evaluate_all():
    events = _read_events()

    outcome_records = {}

    if OUTCOMES.exists():
        with OUTCOMES.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                try:
                    record = json.loads(line)
                    outcome_records[record.get("_id")] = record
                except Exception:
                    continue

    evaluated = []
    pending = []

    for event in events:
        event_id = event.get("_id")

        stored = outcome_records.get(event_id)

        if stored and stored.get("status") == "evaluated":
            evaluated.append(stored)
            continue

        result = evaluate_event(event)

        if result["status"] == "evaluated":
            evaluated.append({
                "_id": event_id,
                **result,
            })

        elif result["status"] == "awaiting_outcome":
            pending.append({
                "_id": event_id,
                **result,
            })

    correct = sum(
        1
        for x in evaluated
        if x.get("correct")
    )

    accuracy = (
        correct / len(evaluated)
        if evaluated
        else 0.0
    )

    return {
        "events": len(events),
        "evaluated": len(evaluated),
        "pending": len(pending),
        "correct": correct,
        "accuracy": round(accuracy, 6),
    }


if __name__ == "__main__":
    print("=" * 72)
    print("IMA STATE TRANSITION OUTCOME EVALUATION")
    print("=" * 72)

    result = evaluate_all()

    for key, value in result.items():
        print(f"{key.upper()}: {value}")

    print("=" * 72)
