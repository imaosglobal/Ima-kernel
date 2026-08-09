from reflection_engine import analyze
from anomaly_detector import check
import json

result={
    "reflection":analyze(),
    "anomaly":check()
}

print(
    json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    )
)
