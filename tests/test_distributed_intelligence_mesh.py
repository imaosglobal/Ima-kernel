import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_mesh_contracts_are_valid():
    for rel in [
        ".ima/evolution/DISTRIBUTED_KNOWLEDGE_MESH.json",
        ".ima/evolution/SOURCE_ADAPTER_CONTRACT.json",
        ".ima/evolution/UNIVERSAL_INTELLIGENCE_CHARTER.json",
        ".ima/evolution/CAPABILITY_GRAPH.json",
        ".ima/engines/REGISTRY.json",
    ]:
        json.loads((ROOT / rel).read_text(encoding="utf-8"))

def test_world_router_is_capability_first():
    sys.path.insert(0, str(ROOT))
    from .ima.runtime.world_router import route
    result = route({"intent": "create an image"})
    assert result["capability_first"] is True
    assert result["truth_state"] == "routing_plan_only"

def test_mesh_rejects_unauthorized_source():
    sys.path.insert(0, str(ROOT))
    from .ima.runtime.distributed_knowledge_mesh import SourceObservation, plan_learning
    item = SourceObservation("x", "sensor", "transport", "telemetry", "2026-10-06", "observed", {"source": "test"}, False)
    result = plan_learning(item)
    assert result.safe_to_integrate is False
    assert result.stages == ("reject",)
