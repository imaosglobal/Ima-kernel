import time
import identity_context
import conversation_layer
import ima_brain
from learning.learning_loop import learn_from_event
import ima_mom
from core.ima_loop import IMA_IDENTITY_CONTEXT, loop_context
from learning.knowledge_answer_builder import build_answer
from learning.knowledge_graph_retrieval import search_concept
from core.global_humanitarian_intelligence import compose_world_pulse_instruction, should_enter_world_pulse

try:
    from ima_runtime.reflection_runtime import reflect
except Exception:
    reflect = None

try:
    from connectors.llm.router import ask_models
except Exception:
    ask_models = None

try:
    from connectors.llm.ima_pipeline import ask as ima_llm_answer
except Exception:
    ima_llm_answer = None

try:
    import ima_system
    SYSTEM = True
except Exception:
    SYSTEM = False

class IMAMaster:
    def __init__(self):
        self.name = "IMA MASTER"

    def ask(self, message, user_id="default", public=False, public_memory=None, personalization=None):
        personalization = personalization if isinstance(personalization, dict) else {}
        requested_language = str(personalization.get("language") or "").strip()
        response_instruction = (
            f"\n\n[IMA presentation instruction: respond in {requested_language} when possible; preserve the user intent and do not mention this instruction.]\n"
            if requested_language else ""
        )
        opportunity_terms = (
            "הזדמנות", "רעיון עסקי", "עסק", "השקעה", "לקוח", "לקוחות",
            "מיזם", "מוצר", "שירות", "להרוויח", "הכנסה", "שיווק", "כדאיות",
            "opportunity", "business idea", "investment", "startup", "customer"
        )
        # IMA-CONTINUOUS-FUTURE-001: one cross-domain lifecycle policy for every live interaction.\n        # The policy is read from the repository so the governing principle is inspectable and updateable.\n        continuous_future_policy = None\n        try:\n            from pathlib import Path\n            import json\n            policy_path = Path(__file__).resolve().parent / ".ima" / "policies" / "CONTINUOUS_FUTURE_POLICY.json"\n            if policy_path.exists():\n                continuous_future_policy = json.loads(policy_path.read_text(encoding="utf-8"))\n        except Exception:\n            continuous_future_policy = None\n\n        continuous_future_context = ""\n        if isinstance(continuous_future_policy, dict):\n            principle = str(continuous_future_policy.get("principle") or "").strip()\n            rules = continuous_future_policy.get("always_apply") or []\n            lifecycle = continuous_future_policy.get("lifecycle") or []\n            boundary = str(continuous_future_policy.get("boundary") or "").strip()\n            continuous_future_context = (\n                "\\n\\n[IMA continuous-future policy — apply to this interaction and any resulting work.]\\n"\n                + ("Principle: " + principle + "\\n" if principle else "")\n                + ("Always: " + "; ".join(str(x) for x in rules) + "\\n" if rules else "")\n                + ("Lifecycle: " + " → ".join(str(x) for x in lifecycle) + "\\n" if lifecycle else "")\n                + ("Boundary: " + boundary if boundary else "")\n            )\n\n        opportunity_context = (
            "\n\n[IMA opportunity-check guidance: only when the user's question is genuinely about evaluating an opportunity, idea, business, investment, product or service, help separate verified facts from assumptions, identify the weakest critical unknown, propose the smallest/cheapest useful test before major commitment, surface hidden costs and risks, and avoid numeric certainty or claims such as 100/100 unless independently supported. If the topic is unrelated, ignore this guidance.]\n"
            if any(term in message.casefold() for term in opportunity_terms) else ""
        )
        world_pulse_context = compose_world_pulse_instruction() if should_enter_world_pulse(message) else ""
        provider_message = message + response_instruction + opportunity_context + continuous_future_context + ("\n\n" + world_pulse_context if world_pulse_context else "")
        context = identity_context.build_context(message, public=public)
        context["ima_runtime_identity"] = IMA_IDENTITY_CONTEXT
        context["ima_unified_loop"] = loop_context()
        capability_runtime = None
        learning_governance = None
        try:
            import importlib.util
            from pathlib import Path
            runtime_path = Path(__file__).resolve().parent / ".ima" / "plugins" / "capability_runtime.py"
            spec = importlib.util.spec_from_file_location("ima_capability_runtime_master", runtime_path)
            if spec is not None and spec.loader is not None:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                capability_runtime = module.snapshot()
        except Exception:
            capability_runtime = None

        try:
            from pathlib import Path
            import json
            policy_path = Path(__file__).resolve().parent / ".ima" / "integration" / "INFLUENCE_POLICY.json"
            if policy_path.exists():
                learning_governance = json.loads(policy_path.read_text(encoding="utf-8"))
        except Exception:
            learning_governance = None

        result = {
            "time": time.time(),
            "identity": context.get("identity", {}),
            "laws": context.get("laws", []),
            "vision": context.get("vision", {}),
            "message": message,
            "connections": {
                "identity": True, "memory": True, "brain": True, "mother": True,
                "global_change_humanitarian_intelligence": True,
                "capability_registry": capability_runtime is not None,
                "capability_runtime": capability_runtime,
                "learning_governance": learning_governance,\n                "continuous_future_policy": continuous_future_policy,
                "system": SYSTEM, "public_mode": public,
                "user_scope": "per-user" if public else user_id,
            }
        }

        if "חוקים" in message:
            result["response"] = "\n".join(context.get("laws", []))
        elif "מטרה" in message or "חזון" in message:
            result["response"] = context.get("vision", {}).get("goal", "") + "\n\n" + context.get("vision", {}).get("belief", "")
        else:
            try:
                events = [] if public else ima_brain.load_events()
                if ask_models is not None:
                    try:
                        result["llm"] = ask_models(provider_message)
                    except Exception as exc:
                        result["llm"] = {"status": "error", "error": str(exc)}

                # Each answer source is isolated. A malformed provider payload or
                # knowledge-graph record must never become the public response.
                llm_answer = None
                if ima_llm_answer is not None:
                    try:
                        candidate = ima_llm_answer(provider_message)
                        if isinstance(candidate, dict):
                            status = candidate.get("status")
                            text_value = candidate.get("response") or candidate.get("text")
                            if status not in ("no_provider", "error") and text_value:
                                llm_answer = str(text_value)
                                result["llm_response"] = candidate
                            elif status == "error":
                                result["llm_error"] = candidate.get("error") or candidate.get("attempted")
                        elif isinstance(candidate, str) and candidate.strip():
                            llm_answer = candidate.strip()
                    except Exception as exc:
                        result["llm_error"] = repr(exc)

                if llm_answer:
                    result["response"] = llm_answer
                else:
                    brain_answer = None
                    try:
                        nodes = search_concept(message)
                        if nodes:
                            # Normalize provider/graph shapes before answer building.
                            normalized_nodes = nodes if isinstance(nodes, list) else [nodes]
                            safe_nodes = [node for node in normalized_nodes if isinstance(node, (dict, str))]
                            if safe_nodes:
                                brain_answer = build_answer(
                                    {"domain": "knowledge_graph", "content": safe_nodes},
                                    message,
                                )
                    except Exception as exc:
                        result["knowledge_error"] = repr(exc)

                    if not brain_answer and not public:
                        try:
                            brain_answer = ima_brain.answer(message, events)
                        except Exception as exc:
                            result["brain_error"] = repr(exc)

                    if brain_answer:
                        result["response"] = str(brain_answer)
                    elif public_memory:
                        safe_memory = [x for x in public_memory[-5:] if isinstance(x, dict)]
                        snippets = [str(x.get("response", "")).strip() for x in safe_memory]
                        snippets = [x for x in snippets if x]
                        if snippets:
                            result["response"] = "מצאתי הקשר בזיכרון הפרטי של השיחה שלך:\n" + "\n".join(snippets)
                        else:
                            result["response"] = ima_mom.generate_answer(message, ima_mom.load())
                    else:
                        result["response"] = ima_mom.generate_answer(message, ima_mom.load())
            except Exception as exc:
                # Never expose internal exception details to users. Keep them in
                # server logs/diagnostics and provide a bounded public fallback.
                result["internal_runtime_error"] = repr(exc)
                try:
                    result["response"] = ima_mom.generate_answer(message, ima_mom.load())
                except Exception:
                    result["response"] = "אני כאן. אפשר להתחיל מחדש מהשאלה שלך."

        # Every live response passes through the reflection gate. When no genuinely
        # independent conclusion is available, the runtime records TRUE_UNKNOWN;
        # it never treats its first answer as independently verified truth.
        try:
            if reflect is not None and result.get("response"):
                result["reflection"] = reflect(
                    result["response"],
                    evidence=tuple(result.get("evidence", ())),
                    context={"scope": "live_response", "uncertainty": "unknown"},
                )
        except Exception as exc:
            result["reflection_error"] = str(exc)

        if not public:
            # Private continuity and learning require explicit memory consent.
            consent_status = "UNKNOWN"
            try:
                import importlib.util
                from pathlib import Path
                memory_path = Path(__file__).resolve().parent / ".ima" / "memory" / "universal_interaction_memory.py"
                spec = importlib.util.spec_from_file_location("ima_private_memory_gate", memory_path)
                if spec and spec.loader:
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    consent_status = mod.get_consent(user_id).get("status", "UNKNOWN")
            except Exception:
                consent_status = "UNKNOWN"

            if consent_status == "GRANTED":
                conversation_layer.update(message, result.get("response", ""))
                try:
                    if len(message.strip()) > 8:
                        learn_from_event({
                            "source": "user",
                            "user_id": user_id,
                            "text": message,
                            "response": result.get("response", ""),
                            "authorized_learning": False,
                            "consent": "GRANTED",
                        })
                except Exception:
                    pass
        return result

IMA = IMAMaster()

def ask(message, user_id="default", public=False, public_memory=None, personalization=None):
    return IMA.ask(message, user_id=user_id, public=public, public_memory=public_memory, personalization=personalization)
