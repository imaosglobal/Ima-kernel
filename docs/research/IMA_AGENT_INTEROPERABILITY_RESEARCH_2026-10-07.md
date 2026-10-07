# IMA Agent Interoperability Research — 2026-10-07

## Purpose
Extend IMA's daily adaptation loop beyond generic capability dimensions into concrete interoperability tests.

## New signals observed today
- MCP remains the tool/data interoperability layer; the 2026-07-28 revision is the current revision reported by current ecosystem sources.
- A2A is the agent-to-agent interoperability layer.
- WebMCP is an emerging browser/web-app tool exposure layer; its current specification is a draft, not a W3C Standard.
- New personal-agent identity/consent standards are emerging in October 2026, including PAP and PACT. These must be tracked as research signals, not adopted automatically.
- Agent-oriented discovery manifests are emerging; these should be evaluated against IMA's existing MCP distribution rather than copied blindly.

## IMA adaptation rule
For every new protocol or interoperability proposal:
1. Observe the primary specification.
2. Identify the concrete capability it would add to IMA.
3. Compare it with the current IMA implementation.
4. Build the smallest reversible prototype or contract test.
5. Test locally and in CI.
6. Verify externally where applicable.
7. Adopt only if evidence shows a real improvement.
8. Record the decision and rejected alternatives.

## Immediate test targets
- MCP: verify current production compatibility against the current specification.
- A2A: define an agent-to-agent discovery/hand-off contract without granting autonomous authority.
- WebMCP: evaluate whether selected IMA web actions can be safely exposed as browser tools while preserving user control.
- Agent identity/consent: evaluate explicit authorization scopes and auditable action provenance before any real-world action.
- Discovery: evaluate whether a machine-readable agent capability manifest improves discoverability without duplicating existing MCP metadata.

## Safety boundary
No protocol, agent, payment rail, autonomous action, or external integration is considered enabled merely because it appears in research. Adoption requires source-specific evidence, implementation, tests, and verification.

## Provenance
Research date: 2026-10-07.
Sources consulted: current web research on MCP, A2A, WebMCP, personal-agent interoperability and agent discovery.
