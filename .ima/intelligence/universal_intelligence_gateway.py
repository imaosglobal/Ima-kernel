
from __future__ import annotations
import hashlib, json, os, time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / ".ima" / "intelligence" / "PROVIDER_REGISTRY.json"
LEDGER = ROOT / ".ima" / "intelligence" / "INTELLIGENCE_EVIDENCE.jsonl"
LEARNING_CANDIDATES = ROOT / ".ima" / "conversation" / "intelligence_learning_candidates.jsonl"
PROVIDER_ENV = {"openai":"OPENAI_API_KEY","anthropic":"ANTHROPIC_API_KEY","gemini":"GEMINI_API_KEY","groq":"GROQ_API_KEY"}

def _now(): return time.time()
def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,default=str).encode()).hexdigest()

def load_registry():
    if REGISTRY.exists():
        try: return json.loads(REGISTRY.read_text(encoding="utf-8"))
        except Exception: pass
    return {"schema":"IMA-PROVIDER-REGISTRY-1.0","providers":[],"policy":{"auto_connect_external_provider":False,"never_store_provider_secrets":True,"private_by_default":True}}

def _configured(provider):
    env=PROVIDER_ENV.get(provider)
    return bool(env and os.getenv(env))

def discover():
    registry=load_registry()
    providers={p.get("id"):dict(p) for p in registry.get("providers",[]) if p.get("id")}
    for provider,env in PROVIDER_ENV.items():
        item=providers.setdefault(provider,{"id":provider,"provider":provider,"interface":"native_api","capabilities":["text_generation"],"auth":{"env":env},"privacy_scope":"provider_terms","provenance":"IMA built-in provider adapter"})
        configured=_configured(provider)
        item["status"]="AUTHORIZED" if configured else item.get("status","DISCOVERED")
        item["configured"]=configured
        item["last_observed_at"]=_now()
    registry["providers"]=list(providers.values())
    REGISTRY.parent.mkdir(parents=True,exist_ok=True)
    REGISTRY.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return registry

def _ask(provider,prompt):
    if provider=="gemini":
        from connectors.llm import gemini
        return gemini.ask(prompt)
    if provider=="anthropic":
        from connectors.llm import anthropic
        return anthropic.ask(prompt)
    if provider=="openai":
        from connectors.llm import openai
        return openai.ask(prompt)
    if provider=="ollama":
        from connectors.llm import ollama
        return ollama.ask(prompt)
    if provider=="groq":
        from connectors.llm import groq
        return groq.ask(prompt)
    raise ValueError("unsupported provider: "+provider)

def _available():
    return [p["id"] for p in discover().get("providers",[]) if p.get("configured") and p.get("status") in {"AUTHORIZED","HEALTH_CHECKED","LIVE"}]

def route(question, *, preferred=None, cross_check=False, private=True, high_impact=False):
    if not question or not question.strip(): return {"status":"EMPTY","response":"","providers":[]}
    providers=_available()
    ordered=([preferred]+[p for p in providers if p!=preferred]) if preferred in providers else providers
    if not ordered:
        return {"status":"NO_AUTHORIZED_PROVIDER","response":"","providers":[],"reason":"No external intelligence provider is currently authorized."}
    if private and os.getenv("IMA_ALLOW_PRIVATE_EXTERNAL_INTELLIGENCE")!="1": cross_check=False
    targets=ordered if (cross_check or high_impact) else ordered[:1]
    results=[]
    for provider in targets:
        started=_now()
        try:
            response=_ask(provider,question)
            text=response.get("response","") if isinstance(response,dict) else str(response or "")
            results.append({"provider":provider,"status":"OK" if text and not text.startswith("[") else "DEGRADED","response":text,"latency_seconds":round(_now()-started,3)})
        except Exception as exc:
            results.append({"provider":provider,"status":"ERROR","error":type(exc).__name__})
    good=[r for r in results if r.get("status")=="OK"]
    selected=good[0] if good else None
    record={"timestamp":_now(),"question_hash":_hash(question),"provider_results":[{k:v for k,v in r.items() if k!="response"} for r in results],"cross_check":bool(cross_check or high_impact),"private_scope":private,"truth_state":"REPORTED_MODEL_OUTPUT","verification_required":True}
    LEDGER.parent.mkdir(parents=True,exist_ok=True)
    with LEDGER.open("a",encoding="utf-8") as fh: fh.write(json.dumps(record,ensure_ascii=False)+"\n")
    if selected:
        LEARNING_CANDIDATES.parent.mkdir(parents=True,exist_ok=True)
        candidate={
            "timestamp": _now(),
            "source_type": "intelligence_provider",
            "provider": selected.get("provider"),
            "question_hash": _hash(question),
            "response": selected.get("response",""),
            "truth_state": "OPEN_HYPOTHESIS",
            "privacy_class": "PRIVATE_UNLESS_EXPLICITLY_SHAREABLE",
            "verification_required": True,
            "provenance": "IMA-UNIVERSAL-INTELLIGENCE-GATEWAY-1.0",
        }
        with LEARNING_CANDIDATES.open("a",encoding="utf-8") as fh: fh.write(json.dumps(candidate,ensure_ascii=False)+"\n")
    return {"status":"OK" if selected else "NO_USABLE_PROVIDER","response":selected.get("response","") if selected else "","provider":selected.get("provider") if selected else None,"providers":results,"truth_state":"REPORTED_MODEL_OUTPUT","verification_required":True,"gateway":"IMA-UNIVERSAL-INTELLIGENCE-GATEWAY-1.0"}

def status():
    registry=discover()
    return {"gateway":"IMA-UNIVERSAL-INTELLIGENCE-GATEWAY-1.0","authorized":[p.get("id") for p in registry.get("providers",[]) if p.get("configured")],"providers":registry.get("providers",[]),"private_external_fanout":os.getenv("IMA_ALLOW_PRIVATE_EXTERNAL_INTELLIGENCE")=="1"}

if __name__=="__main__": print(json.dumps(status(),ensure_ascii=False,indent=2))
