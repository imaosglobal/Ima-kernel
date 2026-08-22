import json
from pathlib import Path
from datetime import datetime

bridge=Path.home()/".ima/evolution/kernel_knowledge_bridge.json"
out=Path.home()/".ima/evolution/runtime_knowledge_state.json"

data={}

try:
    data=json.loads(bridge.read_text())
except:
    pass

state={
    "updated":datetime.now().isoformat(),
    "status":"CONNECTED",
    "source":"kernel_knowledge_bridge",
    "knowledge_available":data.get("available_knowledge",{})
}

out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(
    json.dumps(state,ensure_ascii=False,indent=2)
)

