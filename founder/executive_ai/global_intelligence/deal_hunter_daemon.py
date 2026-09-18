"""Continuous IMA Deal Hunter: discovery -> matching -> referral action queue."""
from __future__ import annotations
import json,time
from pathlib import Path
from founder.executive_ai.global_intelligence.autonomy_orchestrator import cycle

INTERVAL=900
LOG=Path(".ima/deal_hunter.log")

def log(event):
    LOG.parent.mkdir(parents=True,exist_ok=True)
    with LOG.open("a",encoding="utf-8") as fh: fh.write(json.dumps(event,ensure_ascii=False)+"\n")

def run():
    log({"event":"started","interval":INTERVAL,"time":time.time()})
    while True:
        started=time.time()
        try:
            result=cycle(); log({"event":"scan","result":result,"time":time.time()})
        except Exception as exc: log({"event":"error","error":repr(exc),"time":time.time()})
        time.sleep(max(5,INTERVAL-(time.time()-started)))

if __name__=="__main__": run()
