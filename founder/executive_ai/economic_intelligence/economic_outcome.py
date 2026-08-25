from pathlib import Path
import json
import time

FILE = Path("founder/data/economic_outcomes.jsonl")
FILE.parent.mkdir(parents=True, exist_ok=True)


def record_outcome(
    action,
    revenue=0.0,
    acquisition_cost=0.0,
    operating_cost=0.0,
    conversion=None,
    status="observed",
):
    revenue = float(revenue or 0)
    acquisition_cost = float(acquisition_cost or 0)
    operating_cost = float(operating_cost or 0)

    total_cost = acquisition_cost + operating_cost
    profit = revenue - total_cost

    roi = (
        profit / total_cost
        if total_cost > 0
        else 0.0
    )

    margin = (
        profit / revenue
        if revenue > 0
        else 0.0
    )

    record = {
        "timestamp": time.time(),
        "action": action,
        "status": status,
        "revenue": revenue,
        "acquisition_cost": acquisition_cost,
        "operating_cost": operating_cost,
        "total_cost": total_cost,
        "profit": profit,
        "margin": margin,
        "roi": roi,
    }

    if conversion is not None:
        record["conversion"] = float(conversion)

    with FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record


def get_outcomes():
    if not FILE.exists():
        return []

    results = []

    for line in FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue

        try:
            item = json.loads(line)
            if isinstance(item, dict):
                results.append(item)
        except Exception:
            continue

    return results
