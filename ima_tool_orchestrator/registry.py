from .models import Capability
class CapabilityRegistry:
    def __init__(self): self._items={}
    def register(self,c): self._items[c.id]=c
    def discover(self,action="",category=""):
        return [c for c in self._items.values() if c.enabled and (not action or c.action==action) and (not category or c.category==category)]
    def get(self,capability_id): return self._items.get(capability_id)
    def as_dict(self): return {k:vars(v) for k,v in self._items.items()}
