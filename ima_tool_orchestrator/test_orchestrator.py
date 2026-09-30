from .models import ActionRequest
from .orchestrator import IMAOrchestrator

def test_discovery():
    o=IMAOrchestrator(); ids={x.id for x in o.discover("think")}
    assert {"llm.chatgpt","llm.claude"} <= ids

def test_truthful_execution():
    r=IMAOrchestrator().execute(ActionRequest("write","design"))
    assert r["result"]["status"]=="DISCOVERY_ONLY" and not r["result"]["ok"]

if __name__=="__main__":
    test_discovery(); test_truthful_execution(); print("IMA TOOL ORCHESTRATOR TESTS: PASS")
