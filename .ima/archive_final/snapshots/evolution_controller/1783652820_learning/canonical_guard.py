from pathlib import Path
import json

REGISTRY=Path(".ima/governance/canonical_architecture.json")

def canonical():
    return json.loads(
        REGISTRY.read_text()
    )

def verify(component,path):

    data=canonical()

    allowed=data.get(component)

    if allowed and str(path)!=allowed:

        raise RuntimeError(
            "\nIMA BLOCKED DUPLICATE COMPONENT\n"
            f"Component: {component}\n"
            f"Use canonical path:\n{allowed}\n"
        )

    return True


if __name__=="__main__":
    print(canonical())
