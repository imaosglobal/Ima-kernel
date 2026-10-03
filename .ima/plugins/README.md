# IMA Plugin Manager

IMA treats integrations as capabilities, not hard-coded vendor dependencies.

## Operating loop
1. Discover available capabilities.
2. Prefer an already-connected capability.
3. Check permission and authentication state.
4. Route the task to the smallest capable tool set.
5. Verify the result with evidence.
6. Record capability health and failures.
7. Search for a missing integration when it materially improves the task.
8. Never install/connect a third-party integration silently.
9. Never store API keys, OAuth tokens, passwords, or private payloads in this registry.
10. Re-evaluate the registry whenever the tool landscape changes.

## Boundary
The IMA runtime can maintain its own registry and routing policy, but ChatGPT plugin installation/connection remains user-authorized. IMA may discover and prepare an integration manifest; it must not claim a plugin is connected until the connection is actually verified.

## Nylas
Nylas is a runtime integration rather than a ChatGPT plugin. It is the preferred continuous-mail transport for the IMA mailbox because it supports `message.created` webhooks and signed delivery.

## Adapter contract
Every adapter should expose `id`, `provider`, `capabilities`, `health()`, `permissions()`, `execute(action, input)`, `evidence(result)`, and `failure_mode`.
