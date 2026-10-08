# IMA ↔ n8n Agent Interoperability — 2026-10-08

## Source-backed signal

n8n's September 25, 2026 Agents release describes a reusable Agent model with instructions, models, channels/triggers, tools, Skills, sub-agents, Knowledge, Memory and reviewable Sessions. Agents can use MCP servers, n8n tools/nodes and existing workflows as tools, and workflows can call the same published Agent through a Message an Agent node. n8n also documents approvals, per-tool credentials, draft/published versions and execution logs.

## IMA relevance

This is a concrete interoperability candidate for IMA's existing agent/MCP architecture:

- MCP interoperability
- workflow-as-tool boundaries
- reusable agent identity across channels
- skills and knowledge packaging
- memory/session provenance
- sub-agent composition
- approvals and scoped credentials
- execution evidence and reviewable logs
- scheduled execution without granting unrestricted autonomous authority

## Required IMA test sequence

1. Observe the official n8n capability and current implementation.
2. Compare against IMA's MCP, agent, memory, learning and evidence architecture.
3. Define the smallest reversible contract test.
4. Test locally and in CI.
5. Verify externally where applicable.
6. Adopt only a measured improvement.
7. Record the decision and rejected alternatives.

## Proposed contract tests

- n8n_mcp_tool_boundary: an IMA agent can discover/use an n8n-exposed tool only within explicitly granted scope.
- n8n_workflow_as_tool: an n8n workflow can represent a narrowly scoped IMA action without transferring broad credentials to the agent.
- n8n_approval_gate: sensitive actions require an explicit approval state before execution.
- n8n_execution_provenance: tool calls retain timestamp, input/output classification, source and result status sufficient for IMA evidence records.
- n8n_agent_reuse: the same logical agent configuration can be referenced across more than one trigger/channel without creating conflicting identity or memory semantics.
- n8n_memory_boundary: n8n session memory remains separated from IMA personal/shared memory unless an explicit contract grants synchronization.

## Adoption gate

Research evidence does not enable an integration. No n8n credential, workflow, agent or external action is considered enabled until a source-specific implementation exists, tests pass, and external/runtime verification is recorded.

## Current decision

RESEARCH_CANDIDATE — add to IMA's interoperability matrix and daily adaptation queue; do not claim production integration.

## Provenance

Primary source: n8n official blog, "Introducing n8n Agents", published 2026-09-25. Additional official n8n MCP documentation/blog material reviewed 2026-10-08.
