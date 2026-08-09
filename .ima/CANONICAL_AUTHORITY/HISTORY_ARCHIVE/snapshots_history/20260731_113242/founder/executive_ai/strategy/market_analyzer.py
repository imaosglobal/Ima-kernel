import json
from pathlib import Path
import time

FILE=Path("founder/data/market_analysis.json")


def analyze_customer_segment(name, pain, payment, growth):

    score = {
        "pain_score": pain,
        "payment_score": payment,
        "growth_score": growth,
        "total": pain + payment + growth
    }

    return {
        "segment": name,
        "analysis": score,
        "time": time.time()
    }


def save_analysis(items):

    FILE.write_text(
        json.dumps(
            items,
            ensure_ascii=False,
            indent=2
        )
    )

    return items


def best_segment():

    if not FILE.exists():
        return None

    data=json.loads(FILE.read_text())

    return sorted(
        data,
        key=lambda x:x["analysis"]["total"],
        reverse=True
    )[0]
