import json
from pathlib import Path

src = Path(".ima/ledger.jsonl")
out = Path(".ima/ledger.migrated.jsonl")

count = 0

with src.open() as f, out.open("w") as w:
    for i,line in enumerate(f,1):
        e = json.loads(line)

        if e.get("type") == "QUESTION":
            data = e.setdefault("data", {})

            if "id" not in data:
                data["id"] = f"legacy-{i}"
                count += 1

        w.write(json.dumps(e, ensure_ascii=False) + "\n")

print("MIGRATED:", count)

