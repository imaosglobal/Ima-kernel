# IMA Competitive Intelligence

## Operating rule
IMA is developed alongside competing assistants and agent systems. Competitor capabilities are inputs for testing, interoperability, and improvement; they are not claims that IMA already has those capabilities.

## Current comparison set
- OpenAI ChatGPT Work / Agents API: long-running work, tools, files, subagents, app workflows.
- Anthropic Claude: coding, computer use, long-context reasoning, document/presentation workflows.
- Google Gemini: multimodality, action-oriented models, Search and agent experiences.
- Perplexity Computer: multi-model orchestration, connectors, background/recurring work, computer use.
- Multi-provider systems: OpenRouter, Ollama, OpenClaw-style gateways, and provider-agnostic agent kernels.

## IMA integration target
1. Provider-neutral conversation contract.
2. Explicit provider capability registry.
3. Route tasks to available models/tools instead of pretending all providers are connected.
4. Preserve IMA memory, provenance, policy, and user control across providers.
5. Record which provider/tool actually executed each operation.
6. Add adapters only when credentials, APIs, or an authorized connector are available.
7. Benchmark IMA workflows against relevant alternatives and keep dated evidence.

## Verification rule
A provider is marked `available` only after a real authenticated request or connected-tool operation succeeds. A name appearing in UI/configuration is not evidence of connectivity.

## Safety rule
No credential harvesting, unauthorized access, deceptive impersonation, destructive synchronization, or copying proprietary implementation. Interoperability must use documented/public interfaces or authorized connectors.
