# IMA Intelligence Registry

Last verified: 2026-11-22

| Intelligence / host | Interface path | IMA direction | Status | Evidence / blocker |
|---|---|---|---|---|
| OpenAI / ChatGPT | MCP Apps / custom MCP | IMA↔ChatGPT | ELIGIBLE-BUT-ACCOUNT-BLOCKED | Official OpenAI docs confirm custom MCP/MCP connections; this user's Free ChatGPT runtime eligibility remains under support Cases #20595626/#19768893. |
| OpenAI API / Agents | Remote MCP / Responses / Agents API | IMA↔OpenAI model | DISCOVERED | Remote MCP/API path exists; requires application/API authorization. |
| Meta / Meta Model API | Meta Model API / MCP | IMA↔Meta models | DISCOVERED | Meta currently exposes a public-preview Meta Model API and documents MCP connectivity for AI agents; requires Meta developer/API authorization. |
| Anthropic / Claude | Claude API / Remote MCP connector | IMA↔Claude | DISCOVERED | Claude supports remote MCP connectors; connection requires Anthropic authorization. Claude custom remote MCP connectors are documented for Free through Enterprise on supported Claude surfaces. |
| Google Gemini | Gemini Interactions API / Remote MCP | IMA↔Gemini | DISCOVERED | Gemini Interactions supports remote MCP servers; requires Google API authorization. |
| Microsoft Copilot Studio | MCP / MCP Apps / A2A | IMA↔Copilot | DISCOVERED | Microsoft documents MCP tools/resources, MCP Apps in supported Copilot surfaces, and MCP/A2A channels; account/tenant entitlements required. |
| Open-source/local models | local/OpenAI-compatible/MCP adapters | IMA↔model | DISCOVERED | Prefer free/local runtimes where technically feasible; runtime depends on device/server resources. |
| Future MCP/A2A hosts | standards adapters | bidirectional | FUTURE-READY | Add through the same registry/adapter contract; never create a parallel IMA system. |

## IMA itself: the intelligence layer

IMA is not merely another provider adapter. It has its own canonical **IMA Intelligence Core**.

The Core receives a user goal/context, determines what is known and unknown, decides whether to answer itself or consult one/multiple connected intelligences, compares their outputs, preserves disagreement, applies IMA's safety/privacy/agency rules, and returns one IMA response with provenance.

Canonical loop:

user/input → IMA Core → capability/routing decision → one or more intelligences → evidence + disagreement → IMA synthesis/judgment → IMA response → user

IMA therefore answers other intelligences as well:

intelligence A → IMA Core → interpret/validate/synthesize → response to A

The response from IMA is a first-class intelligence message, not a relay. It can contain:
- direct IMA answer;
- evidence/provenance;
- uncertainty/unknowns;
- agreement/disagreement with another intelligence;
- requested tool/action result;
- a structured handoff to another intelligence;
- explicit request for clarification when necessary.

### Multi-intelligence protocol

Every connected intelligence gets the same provider-neutral envelope:

request_id
session_id
user_authorization
source_intelligence
target_intelligence
purpose
input_scope
allowed_capabilities
privacy/data boundary
request
evidence
provenance
uncertainty
result
next_action

Default behavior is **minimum necessary context**. IMA does not broadcast a conversation to every provider. It selects the smallest authorized set of intelligences needed for the task.

### Bidirectional exchange

- IMA → intelligence: ask, delegate, verify, compare, or request a specialized capability.
- intelligence → IMA: return answer/tool result/evidence/uncertainty.
- intelligence A ↔ intelligence B: only through IMA-mediated, explicitly authorized orchestration.
- IMA → user: synthesize and explain the result in the user's language/style.
- user → IMA: remains the source of agency; no provider gains authority merely by being connected.

### Continuous discovery

The registry is continuously expandable. Each monitoring cycle should:
1. discover new capable AI providers/models/hosts and meaningful protocol changes;
2. record official evidence;
3. classify the candidate;
4. identify the cheapest/free authorized connection path;
5. create/update the adapter contract;
6. connect when credentials/permissions exist;
7. run a live capability test;
8. record evidence and failure/blocker;
9. never mark a provider connected without runtime verification.

Discovery targets include model providers, AI hosts, agent runtimes, local/open-weight models, MCP/A2A-compatible systems, and future interoperability standards.

## Rule

A provider is only marked CONNECTED or RUNTIME-VERIFIED after actual authorized credentials/configuration and a successful live test. Discovery is not connection.

## Shared contract

request → authorization → capability discovery → intelligence call → evidence/provenance → result → IMA

For agent-to-agent exchange:

IMA → intelligence A → authorized handoff → intelligence B → verified result → IMA

No provider may implicitly receive private data belonging to another provider/user/session.


## Universal bridge implementation

The machine-readable registry is `config/ima-intelligence-registry.json`. All current and future agents/models/hosts use `docs/IMA_UNIVERSAL_INTELLIGENCE_BRIDGE.md` as the single adapter contract. This includes Meta, Claude, Gemini, OpenAI, Copilot, Hugging Face/open models, MCP, A2A, local/self-hosted models, and future intelligence technologies.

The continuous scan must discover additional providers and protocols and attempt authorized connection/testing through this same lifecycle. It must never invent a connection or create a parallel integration path.
