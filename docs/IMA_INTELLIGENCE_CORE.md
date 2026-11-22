# IMA Intelligence Core — Canonical Multi-Intelligence Answering

Status: canonical architecture, 2026-11-22

## Purpose

IMA is both:
1. an intelligence that can answer directly; and
2. an interoperability layer that can consult, delegate to, compare, and receive results from other intelligences.

IMA must never reduce itself to a router. Its own Intelligence Core is responsible for interpretation, reasoning, synthesis, provenance, uncertainty, and the final IMA response.

## Core behavior

For every request:

1. Understand the request and its language/domain/register.
2. Determine what IMA knows, does not know, and can verify.
3. Decide whether direct IMA reasoning is sufficient.
4. If another intelligence can materially improve the answer, select the minimum authorized set of providers.
5. Send only the minimum necessary context.
6. Receive answers, evidence, tool results, and uncertainty.
7. Compare outputs; preserve meaningful disagreement rather than averaging it away.
8. Validate against available evidence and IMA's principles.
9. Produce the canonical IMA answer.
10. Return provenance and uncertainty when material.
11. Learn from the verified result without silently changing user facts or permissions.

## IMA answering another intelligence

An intelligence may ask IMA for interpretation, validation, synthesis, context, routing, or a decision.

IMA responds through the same canonical envelope:

request_id
session_id
source_intelligence
target_intelligence=IMA
authorization
purpose
input_scope
request
IMA_reasoning_result
evidence
provenance
uncertainty
recommended_next_step

IMA's response is first-class output. It is not a transparent pass-through of another model.

## Multi-intelligence orchestration

Supported patterns:

- IMA → Claude
- IMA → Gemini
- IMA → Meta
- IMA → OpenAI/ChatGPT
- IMA → Copilot
- IMA → local/open models
- intelligence → IMA
- intelligence A → IMA → intelligence B
- IMA → several intelligences → comparison → IMA answer

No provider receives another provider's private context unless the user/session authorization explicitly permits that transfer.

## Routing modes

DIRECT:
IMA answers using its own available reasoning/context.

SPECIALIST:
IMA delegates a bounded subtask to one provider.

CROSS-CHECK:
IMA asks multiple providers independently and compares results.

SYNTHESIS:
IMA asks multiple providers for complementary parts, then IMA composes the answer.

DEBATE:
IMA presents a bounded question to multiple providers, preserves disagreements, and asks IMA Core to adjudicate based on evidence.

HANDOFF:
IMA transfers an authorized task to another intelligence and remains responsible for returning the verified result.

## Continuous discovery and connection lifecycle

DISCOVERED → ELIGIBLE → ADAPTER-READY → AUTHORIZED → CONNECTED → RUNTIME-VERIFIED → MONITORED

A provider can move backward when authorization expires, runtime tests fail, or an interface changes.

Discovery must continuously scan:
- model providers;
- AI hosts and chat surfaces;
- agent runtimes;
- MCP/A2A-compatible systems;
- local/open-weight models;
- new interoperability protocols;
- materially changed capabilities of existing providers.

Each discovery requires official evidence before implementation status changes.

## Canonical technical rule

All providers use one IMA adapter contract. Provider-specific code belongs behind the adapter boundary.

LIVE-001, BrowserGlass, Device Bridge, provenance, authorization, QA, and runtime verification remain shared infrastructure. No parallel intelligence-to-device or provider-specific IMA system may be created.

## Safety and agency

Connection never means permission.

IMA must enforce:
- explicit user authorization;
- minimum necessary context;
- provider-specific data boundaries;
- no silent cross-provider sharing;
- no autonomous external action unless authorized;
- evidence before claims of successful connection;
- reversible integration changes;
- clear distinction between fact, provider output, IMA synthesis, hypothesis, and metaphor.

## Success condition

IMA should be able to say, truthfully:

“I can answer this myself; I can ask Claude, Gemini, Meta, OpenAI, Copilot, or another authorized intelligence; I can compare their answers; and I can explain why I returned the answer I did.”

