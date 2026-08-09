
def record_feedback(action,status,details=""):
    path=Path(".ima/feedback_loop.json")

    try:
        data=json.loads(
            path.read_text(encoding="utf-8")
        )
    except Exception:
        data={
            "metrics":{
                "success":0,
                "failure":0,
                "rollback":0
            },
            "history":[]
        }

    if status=="success":
        data["metrics"]["success"]+=1

    elif status=="failure":
        data["metrics"]["failure"]+=1

    data.setdefault("history",[]).append({
        "time":time.time(),
        "action":action,
        "status":status,
        "details":details
    })

    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


from pathlib import Path
import json,time

STATE=Path(".ima/autonomy_state.json")
PROPOSALS=Path(".ima/improvement_proposals.jsonl")

def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except:
        return {}

def run():

    engine=load_json(
        Path(".ima/autonomy_engine.json")
    )

    state={
        "time":time.time(),
        "mode":engine.get("mode"),
        "actions":[]
    }

    if engine.get("capabilities",{}).get("learn"):
        state["actions"].append(
            "learning_loaded"
        )

    if engine.get("capabilities",{}).get("analyze"):
        state["actions"].append(
            "analysis_ready"
        )

    if engine.get("capabilities",{}).get("propose_changes"):

        memory_path=Path(".ima/proposal_memory.json")

        try:
            memory=json.loads(
                memory_path.read_text(encoding="utf-8")
            )
        except Exception:
            memory={"decisions":[]}

        action="analyze before modifying"

        already=False

        for item in memory.get("decisions",[]):
            if item.get("action")==action:
                already=True

        if already:
            state["actions"].append(
                "proposal_skipped_duplicate"
            )
            return state

        proposal={
            "type":"AUTO_PROPOSAL",
            "time":time.time(),
            "proposal":{
                "area":"system",
                "goal":"improve reliability",
                "action":action,
                "status":"pending_validation"
            }
        }

        memory.setdefault(
            "decisions",
            []
        ).append({
            "time":time.time(),
            "action":action,
            "status":"created"
        })

        memory_path.write_text(
            json.dumps(
                memory,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        with PROPOSALS.open(
            "a",
            encoding="utf-8"
        ) as f:
            f.write(
                json.dumps(
                    proposal,
                    ensure_ascii=False
                )+"\n"
            )

        state["actions"].append(
            "proposal_created"
        )

    STATE.write_text(
        json.dumps(
            state,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    return state


if __name__=="__main__":
    print(json.dumps(
        run(),
        ensure_ascii=False,
        indent=2
    ))
