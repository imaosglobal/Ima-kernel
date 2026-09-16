# Claude Handoff — IMA Shared Work

Please read `.squad/CHATGPT_COLLABORATION.md` first.

ChatGPT is now working against the same filesystem through Desktop Commander.

## Request

Continue the IMA implementation from the actual repository state, not from assumptions or old chat context.

First inspect:

- current runtime entry points
- active/canonical registries
- `.squad` state and recent orchestration logs
- product/UI entry points
- memory/context path
- model/intelligence path
- action/tool path
- tests and health checks

Then identify the smallest real integration path that can be verified end-to-end.

Do not create a second competing architecture.
Do not delete historical backups.
Do not claim a capability is active until a runtime test demonstrates it.

## Important environment note

Desktop Commander currently cannot execute Termux binaries because its shell receives Permission denied for `/data/data/com.termux/files/usr/bin/*`. This is an environment limitation of the shared bridge, not evidence that the repository is broken.

## Shared coordination

Record substantive work and verification in `.squad/CHATGPT_COLLABORATION.md` and existing `.squad` logs.

If you discover a conflict with another agent's changes, preserve the work and document the conflict before resolving it.

## Target

Move IMA from a large collection of documented/historical capabilities toward one verified product path:

request -> context/memory -> intelligence -> response/action -> verification

Then connect the user-facing product to that verified path.
