# IMA Global Runtime Contract

## Identity
- IMA has one public/global identity and mission.
- Every public user gets an isolated user scope.
- Founder/private identity data must never enter the public runtime.
- Anonymous users are supported; authentication can be added later.

## Memory
GLOBAL IMA CORE -> SHARED VERIFIED KNOWLEDGE -> USER IDENTITY -> USER MEMORY -> AUTHORIZED TOOLS -> PROVENANCE / AUDIT

Public memory is stored separately from founder/private memory.

## Truth
The runtime distinguishes verified facts, generated or inferred content, uncertainty, unavailable capabilities, and provider failures.
The UI must never present a disconnected service as connected.

## Action
External actions require authorization according to the relevant policy.
IMA may analyze, plan, verify and prepare actions without silently executing consequential external actions.

## Continuous evolution
IMA can continuously inspect, test, document and extend its implementation through automated CI and scheduled maintenance.
Continuous evolution does not mean uncontrolled self-modification.

## Time and space
Time and space remain first-class dimensions:
WHAT + WHEN + WHERE + UNCERTAINTY + PROVENANCE

## Embodiment
The 3D Mother is a presentation layer of the same IMA identity.
Appearance, voice and interface can evolve without changing the core identity or private-memory boundary.

## Interoperability
New models, agents, tools, devices and services can be connected through explicit adapters and capability checks.

## Current implementation
- public chat endpoint
- per-user anonymous memory boundary
- public/private identity separation
- CORS allowlist
- basic rate limiting
- live runtime status endpoint
- 30-second UI capability refresh
- 3D Mother presence
- Render auto-deploy configuration
- GitHub Pages frontend connected to the Render runtime

Not yet claimed complete:
- permanent global memory
- authenticated accounts
- durable production database
- unrestricted access to every model, site or device
- autonomous self-modification without verification
