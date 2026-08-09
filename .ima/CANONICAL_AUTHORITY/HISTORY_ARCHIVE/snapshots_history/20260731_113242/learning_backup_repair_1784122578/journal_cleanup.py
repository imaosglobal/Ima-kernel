from learning.self_reflection import load_journal, save_journal

def cleanup_journal():
    journal = load_journal()

    clean = []
    seen = set()

    for event in journal["events"]:
        key = event["event"]

        if key not in seen:
            seen.add(key)
            clean.append(event)

    journal["events"] = clean

    save_journal(journal)

    return {
        "before": len(seen),
        "after": len(clean)
    }
