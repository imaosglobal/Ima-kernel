from .adapters import DEFAULT_CAPABILITIES,not_connected_executor
from .models import ActionRequest
from .policy import PolicyGate
from .provenance import Provenance
from .registry import CapabilityRegistry
class IMAOrchestrator:
    def __init__(self,registry=None,executor=not_connected_executor):
        self.registry=registry or CapabilityRegistry()
        for c in DEFAULT_CAPABILITIES:self.registry.register(c)
        self.policy,self.provenance,self.executor=PolicyGate(),Provenance(),executor
    def discover(self,action="",category=""): return self.registry.discover(action,category)
    def plan(self,request): return {"goal":request.goal,"action":request.action,"candidates":[c.id for c in self.discover(request.action)]}
    def execute(self,request):
        cs=self.discover(request.action)
        if not cs:return {"ok":False,"status":"NO_CAPABILITY","candidates":[]}
        c=cs[0]; allowed,reason=self.policy.authorize(c,request)
        if not allowed:return {"ok":False,"status":reason,"capability_id":c.id}
        result=self.executor(c,request)
        return {"result":vars(result),"provenance":self.provenance.record(c.id,request,result)}
