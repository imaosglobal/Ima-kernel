
import time
import json
from pathlib import Path

POLICY=json.loads(
Path(
"learning/learning_policy.json"
).read_text()
)


def learning_cycle():

    print(
    "[ADAPTIVE LEARNING]"
    )

    print(
    "Resource limit:",
    POLICY["max_memory_mb"],
    "MB"
    )

    print(
    "Sources per cycle:",
    POLICY["max_background_sources_per_cycle"]
    )

    # future source discovery hook
    # never loads unlimited data

    return True


if __name__=="__main__":

    while True:

        learning_cycle()

        time.sleep(
            POLICY["sleep_between_cycles"]
        )
