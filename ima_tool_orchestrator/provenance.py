import hashlib,json,time
class Provenance:
    def record(self,capability_id,request,result):
        p={"ts":time.time(),"capability_id":capability_id,"goal":request.goal,"action":request.action,"status":result.status,"ok":result.ok}
        if request.context.get("time_space") is not None:
            p["time_space"]=request.context["time_space"]
        p["event_hash"]=hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest(); return p
