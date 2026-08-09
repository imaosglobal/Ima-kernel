
from learning.learning_memory import get_patterns
import time


def evaluate_learning():

    patterns=get_patterns()

    improvements=[]

    for item in patterns:
        name=item.get("pattern","")
        count=item.get("count",0)

        if count >= 2:
            improvements.append({
                "pattern":name,
                "strength":count,
                "suggestion":
                    f"להעמיק יכולת IMA בתחום {name}"
            })

    return {
        "time":time.time(),
        "patterns":patterns,
        "improvements":improvements,
        "status":"learning_evaluated"
    }
