import time


def detect_signals(company):

    signals=[]

    text=" ".join(
        company.get("signals",[])
    ).lower()

    if "ai" in text:
        signals.append({
            "signal":"AI focus",
            "importance":30
        })

    if "llm" in text:
        signals.append({
            "signal":"LLM usage",
            "importance":30
        })

    if company.get("founders",99)<=5:
        signals.append({
            "signal":"small founding team",
            "importance":20
        })

    if company.get("stage") in ["pre-seed","seed"]:
        signals.append({
            "signal":"early funding stage",
            "importance":20
        })

    return {
        "company":company.get("name"),
        "signals":signals,
        "detected_at":time.time()
    }
