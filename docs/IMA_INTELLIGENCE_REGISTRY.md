# IMA Intelligence Registry

Last verified: 2026-11-22

| Intelligence / host | Interface path | IMA direction | Status | Evidence / blocker |
|---|---|---|---|---|
| OpenAI / ChatGPT | MCP Apps / custom MCP | IMA↔ChatGPT | ELIGIBLE-BUT-ACCOUNT-BLOCKED | Official OpenAI docs confirm custom MCP and MCP connections; this user's Free ChatGPT runtime eligibility remains under support Cases #20595626/#19768893. |
| OpenAI API / Agents | Remote MCP / Responses / Agents API | IMA↔OpenAI model | DISCOVERED | Official API supports remote MCP servers; requires application/API authorization. |
| Microsoft Copilot Studio | MCP / MCP Apps / A2A | IMA↔Copilot | DISCOVERED | Microsoft documents MCP tools/resources, MCP Apps in supported Copilot surfaces, and MCP/A2A channels; account/tenant entitlements required. |
| Anthropic / Claude | MCP / API | candidate | DISCOVERED | Adapter target; connection requires Anthropic account/API authorization. |
| Google Gemini | API / MCP-compatible ecosystem | candidate | DISCOVERED | Adapter target; connection requires Google account/API authorization. |
| Open-source/local models | local/OpenAI-compatible/MCP adapters | IMA↔model | DISCOVERED | Prefer free/local runtimes where technically feasible; runtime depends on device/server resources. |
| Future MCP/A2A hosts | standards adapters | bidirectional | FUTURE-READY | Add through the same registry/adapter contract; never create a parallel IMA system. |

## Rule

A provider is only marked CONNECTED or RUNTIME-VERIFIED after actual authorized credentials/configuration and a successful live test. Discovery is not connection.

## Shared contract

request → authorization → capability discovery → intelligence call → evidence/provenance → result → IMA

For agent-to-agent exchange:

IMA → intelligence A → authorized handoff → intelligence B → verified result → IMA

No provider may implicitly receive private data belonging to another provider/user/session.
