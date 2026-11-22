# LIVE-001 Host Capability Manifest

## Purpose
LIVE-001 is one canonical Interactive Window contract. Platform hosts expose capabilities through adapters rather than creating separate window systems.

## Capability model
Each host reports supported window surfaces, geometry, authorized context, input modalities, authorization scope, verification evidence, and continuity identity.

## Capability lifecycle
DISCOVERED → ELIGIBLE → AUTHORIZED → ACTIVE → VERIFIED → REVOKED

An adapter MUST NOT report a capability as active merely because an API exists. LIVE-001 requires a runtime capability test and evidence.

## Host adapters

### Web
Implemented baseline: movable, resizable, mini, split, fullscreen, detachable browser window, persistent geometry and user-scoped timeline.

### Android
Native host path: supported multi-window/PiP/overlay surfaces where the OS grants them. Accessibility and overlay permissions are explicit user capabilities. The native host must preserve the same LIVE-001 identity and timeline contract.

### Windows
Native host path: topmost/resizable/multi-monitor surfaces, global shortcut where authorized, optional transparency and accessibility integration. Cross-application context is capability-gated.

### iPadOS/macOS
Use only supported windowing, split/window management, accessibility and extension mechanisms. No assumption of unrestricted above-all-app behavior.

### Spatial / future devices
Map the same logical window into AR/VR/spatial anchors, wearables, vehicles, robots or future displays through capability adapters.

## Universal context contract
User → Window → IMA → authorized context/intelligence/device → IMA → Window → User

Every exchange carries identity, authorization scope, minimum-necessary context, provenance, evidence, uncertainty and verification status.

## Security boundary
LIVE-001 must never bypass OS permissions, application security, DRM, anti-cheat, authentication or other platform controls. Assistance in games/software is permitted only through supported interfaces, accessibility, APIs or authorized visual/context observation.

## Acceptance test
For every host adapter:
1. discover capabilities;
2. request authorization;
3. connect;
4. run capability test;
5. run safe action test;
6. verify post-action state;
7. record evidence in the per-user timeline;
8. monitor;
9. improve;
10. re-test.

This manifest is an implementation contract, not proof that every listed host capability is currently connected.
