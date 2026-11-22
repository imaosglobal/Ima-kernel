# IMA Universal Intelligence Bridge

Status: canonical implementation contract — 2026-11-22

IMA must connect any authorized intelligence, agent, model, host, or future interoperability technology through one canonical bridge. Provider-specific interfaces stay behind adapters; IMA remains the intelligence and policy layer.

## Canonical message
request_id | session_id | source | target | purpose | authorization | minimum-necessary context | request | capabilities | evidence | provenance | uncertainty | result | next_action

## Provider adapter lifecycle
DISCOVERED → ELIGIBLE → ADAPTER-READY → AUTHORIZED → CONNECTED → RUNTIME-VERIFIED → MONITORED

A provider may only enter CONNECTED/RUNTIME-VERIFIED after an authorized live call succeeds. A documented API or protocol is not proof of a live connection.

## Adapter classes
- OpenAI / ChatGPT / OpenAI API / Agents
- Anthropic / Claude
- Google / Gemini
- Meta / Meta AI / Meta Model API
- Microsoft / Copilot / Copilot Studio
- Hugging Face / open-weight models / Spaces
- Local and self-hosted OpenAI-compatible endpoints
- MCP hosts and MCP servers
- A2A-compatible agents
- Future model/agent/host protocols
- Specialized intelligences: search, vision, speech, code, video, robotics and domain systems

## IMA response to another intelligence
IMA is a first-class endpoint, not a transparent proxy. It can answer from its own context/reasoning, validate claims, add context, identify contradictions, synthesize outputs, refuse unauthorized transfers, request clarification, return evidence/provenance/uncertainty, delegate bounded specialist work, and return verified results.

## Inter-intelligence rule
Provider A never receives Provider B private context by default. Canonical path: Provider A → IMA → authorized Provider B → IMA → Provider A. Only minimum authorized data crosses each boundary.

## Future-proofing
Adding a provider requires registry entry, adapter declaration, capability mapping, authorization mapping, runtime verification test, and monitoring rule. No provider may create a parallel IMA routing system, browser bridge, or intelligence core.