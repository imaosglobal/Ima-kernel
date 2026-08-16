import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent

MEMORY_TARGET = Path.home() / ".ima/software_learning.jsonl"

def load_brain():
    from software_brain import analyze
    from learning_graph import understand

    return {
        "software": analyze(),
        "graph": understand()
    }


def save_to_ima(data):
    MEMORY_TARGET.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    record = {
        "time": datetime.now().isoformat(),
        "source": "software_intelligence",
        "data": data
    }

    with open(MEMORY_TARGET,"a",encoding="utf-8") as f:
        f.write(
            json.dumps(record,ensure_ascii=False)
            + "\n"
        )


if __name__ == "__main__":
    knowledge = load_brain()
    save_to_ima(knowledge)

    print("IMA MEMORY UPDATED")
    print(MEMORY_TARGET)


# ----------------------------------------------------------------------
# IMA CANONICAL ASGI ENTRYPOINT
# ----------------------------------------------------------------------
try:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
except Exception as e:
    raise RuntimeError(
        "FastAPI is required for the IMA bridge ASGI runtime: " + repr(e)
    )

app = FastAPI(
    title="IMA Bridge",
    version="1.0",
)

@app.get("/")
async def root():
    return JSONResponse({
        "system": "IMA",
        "status": "online",
        "continuity": True,
        "bridge": "connectors.intelligence.ima_bridge",
    })

@app.get("/health")
async def health():
    result = {
        "status": "healthy",
        "system": "IMA",
        "continuity": True,
    }

    try:
        from pathlib import Path
        import json

        state_path = (
            Path.cwd()
            / ".ima/CANONICAL_AUTHORITY/SINGLE_SNAPSHOT/CURRENT"
            / ".ima/continuity/generation_state.json"
        )

        if state_path.exists():
            state = json.loads(
                state_path.read_text(encoding="utf-8")
            )
            result["generation"] = state.get("generation", 1)
    except Exception:
        pass

    return JSONResponse(result)

@app.get("/continuity")
async def continuity():
    try:
        from pathlib import Path
        import json

        bridge_path = (
            Path.cwd()
            / ".ima/CANONICAL_AUTHORITY/SINGLE_SNAPSHOT/CURRENT"
            / ".ima/continuity/runtime_bridge.json"
        )

        state = json.loads(
            bridge_path.read_text(encoding="utf-8")
        )

        return JSONResponse(state)

    except Exception as e:
        return JSONResponse(
            {
                "continuity_active": False,
                "error": repr(e),
            },
            status_code=500,
        )

@app.get("/heartbeat")
async def heartbeat():
    return JSONResponse({
        "system": "IMA",
        "heartbeat": True,
        "continuity": True,
    })
