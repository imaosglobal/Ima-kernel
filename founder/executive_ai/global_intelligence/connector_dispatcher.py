"""Safe dispatcher for commerce connectors.
Never claims external execution without a returned proof/reference.
"""
from __future__ import annotations
import json,os,time
from pathlib import Path
from .marketplace_adapters import all_marketplaces
STATE=Path("founder/data/connector_state.json")

def _configured(name):
    key=name.upper().replace(".","_").replace(" ","_")
    return bool(os.getenv(f"IMA_{key}_TOKEN") or os.getenv(f"IMA_{key}_CLIENT_ID"))

def readiness():
    out=[]
    for m in all_marketplaces():
        name=m["name"]
        configured=_configured(name)
        mode=m.get("submit_mode","")
        status="READY" if configured else ("AUTH_REQUIRED" if mode in ("api_or_account","partner_dashboard_or_api","partner_program") else "MANUAL_OR_ACCOUNT")
        out.append({"name":name,"status":status,"submit_mode":mode,"payout_model":m.get("payout_model"),"url":m.get("url")})
    return out

def dispatch(action):
    if not action.get("consent_verified"):
        raise ValueError("consent verification required")
    routes=action.get("marketplace_routes",[])
    result=[]
    for route in routes:
        name=route["name"]
        result.append({"marketplace":name,"status":"READY_FOR_AUTH" if not _configured(name) else "AUTHORIZED_CONNECTOR_AVAILABLE","external_submission":False,"checked_at":time.time()})
    STATE.parent.mkdir(parents=True,exist_ok=True)
    STATE.write_text(json.dumps({"checked_at":time.time(),"connectors":result},ensure_ascii=False,indent=2),encoding="utf-8")
    return result

if __name__=="__main__":
    import sys
    print(json.dumps(readiness(),ensure_ascii=False,indent=2))
