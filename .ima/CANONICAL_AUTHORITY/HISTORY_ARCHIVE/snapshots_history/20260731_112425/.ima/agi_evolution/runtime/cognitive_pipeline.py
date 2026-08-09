from pathlib import Path
import json,time

ROOT=Path(".ima/agi_evolution/runtime")

def load(name):
    p=ROOT/name
    if p.exists():
        return json.loads(p.read_text())
    return {}

def run():
    state={
        "time":time.time(),
        "memory":"pending",
        "goal":"pending",
        "decision":"pending",
        "evolution":"pending"
    }

    try:
        from goal_engine import create_goal
        state["goal"]=create_goal()
    except Exception as e:
        state["goal"]="error:"+str(e)

    try:
        from decision_engine import decide
        state["decision"]=decide()
    except Exception as e:
        state["decision"]="error:"+str(e)

    try:
        from self_evolution_loop import IMA_SELF_EVOLUTION
        state["evolution"] = IMA_SELF_EVOLUTION.create_plan()
    except Exception as e:
        state["evolution"]="error:"+str(e)

    state["memory"]="available"

    (ROOT/"cognitive_pipeline_state.json").write_text(
        json.dumps(state,indent=2,ensure_ascii=False)
    )

    return state

if __name__=="__main__":
    print(json.dumps(run(),indent=2,ensure_ascii=False))
