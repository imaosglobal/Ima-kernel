# IMA — Multi-Intelligence Interoperability

Status: canonical architecture direction
Date: 2026-11-22

IMA should be able to interoperate with current and future legitimate AI systems, models, agents, and hosts without making any one provider a dependency.

## Canonical contract

Each connected intelligence/host is an adapter around a common contract:

request → identity/authorization → capability discovery → action/inference → evidence → provenance → result → IMA

Supported directions:
- IMA → connected intelligence
- connected intelligence → IMA
- intelligence ↔ intelligence, only through an IMA-mediated, authorized session when permitted
- device/browser → IMA verified state
- IMA → device/browser only with user authorization

## Initial integration targets

Prioritize standards/open interfaces and officially supported APIs/connectors for:
- OpenAI / ChatGPT
- Anthropic / Claude
- Google / Gemini
- Microsoft / Copilot
- open-source/local models and agent runtimes
- future MCP-compatible hosts and agents

Do not claim a live integration until credentials, API access, permissions, implementation, and runtime verification are confirmed.

## Design rules

1. MCP is an interoperability protocol, not the identity of IMA.
2. IMA remains provider-neutral.
3. No provider receives another user's private data without explicit authorization and an appropriate connector boundary.
4. Preserve provenance and distinguish model output from verified external evidence.
5. Prefer reversible/free development paths.
6. Do not create a parallel browser/action system; reuse LIVE-001/BrowserGlass/Device Bridge.
7. New providers plug into the adapter layer; they do not create separate IMA products.
8. Future intelligences should be addable without redesigning the core.

## Capability registry

Track each intelligence with:
provider, host/model, interface, capabilities, directionality, auth state, data boundary, cost, rate limits, evidence quality, runtime status, last verification, and blocker.

Status values:
DISCOVERED → ELIGIBLE → CONNECTED → RUNTIME-VERIFIED → DEGRADED/BLOCKED

## Immediate work

Discover officially supported, lawful connection paths for the initial targets; implement only those that can be done with existing authorized connectors or free/open interfaces; then runtime-verify and record evidence.
