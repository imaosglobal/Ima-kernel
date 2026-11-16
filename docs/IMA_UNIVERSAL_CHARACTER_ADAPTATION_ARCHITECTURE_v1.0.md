# IMA Universal Character Adaptation Architecture v1.1
Date: 2026-11-16
Status: prepared / not activated in public UI

## Purpose
Make one canonical IMA identity adapt to present and future displays without creating separate characters or parallel product identities.

## Non-negotiable model
One identity, one canonical scene/character definition, many presentation adapters.

Identity layers:
1. IMA identity — name, provenance, values, voice, interaction contract.
2. Character semantic model — proportions, landmarks, expressions, gestures, materials, animation states, accessibility descriptions.
3. Canonical scene representation — portable scene graph and animation data.
4. Platform adapters — web/mobile/desktop/XR/native/game/film/low-power renderers.
5. Interaction adapters — touch, pointer, keyboard, controller, hand tracking, gaze, voice, accessibility.
6. Delivery policy — device capability, bandwidth, battery, thermal budget, screen size, latency, privacy and permission.
7. Runtime verification — actual capability detection and observed rendering/interaction results.

## Device adaptation ladder
- 2D fallback: semantic portrait/logo + accessible controls.
- Small mobile: compact character, touch targets, low texture/geometry budget, portrait/landscape adaptation.
- Tablet/desktop: richer 3D, pointer/keyboard, optional multi-panel layout.
- TV/kiosk: distance-readable UI, controller/remote navigation, simplified interaction.
- AR mobile: camera composition, world-scale placement, anchors/depth when supported.
- VR/MR/XR: stereo rendering, 6DoF, spatial UI, hand/controller/gaze input, comfort constraints.
- Smart glasses: constrained field of view, persistent spatial anchors only when supported, glanceable interactions.
- Future displays: capability-negotiated adapter rather than hard-coded device assumptions.
- Low-power/legacy: static/2D/low-poly fallback with identical semantic identity.

## Host adaptation: ChatGPT and other containers
IMA must distinguish IMA capability from the host surface that displays it.

Host tiers:
- Native ChatGPT mobile screen sharing: use the host's user-approved live screen/video channel when available; this is a viewing path, not automatically a device-control permission.
- ChatGPT MCP Apps on supported web hosts: use the canonical ui resource and MCP Apps bridge for interactive IMA UI.
- IMA public web/PWA: use the same semantic actions and device-aware rendering contracts.
- Future hosts: negotiate capabilities rather than assuming a specific ChatGPT UI.

OpenAI currently documents screen sharing for eligible mobile users through Advanced Voice, while current Live voice does not itself support screen sharing. Screen sharing is therefore treated as a host capability that must be detected at runtime, not as an IMA guarantee. A host screen stream does not grant IMA authority to act on the device.

## Asset strategy
Canonical source assets should support interoperable delivery:
- glTF/GLB for portable real-time delivery.
- OpenUSD/USDZ where scene interchange, high-fidelity authoring or Apple spatial delivery requires it.
- Separate LODs, texture resolutions, animation tiers and optional effects.
- Avoid baking platform-specific behavior into the identity asset.

## Runtime selection
At runtime calculate: display × graphics × input × spatial × network × power × accessibility × permissions × host.
Select the smallest presentation tier that preserves intended identity and interaction.
The renderer must never assume XR, WebGPU, WebGL2, AR, depth, hand tracking or spatial anchors exist. Detect, request permission where appropriate, verify, then activate.

## Rendering tiers
T0 semantic/2D; T1 lightweight 3D; T2 full web 3D; T3 AR; T4 immersive XR; T5 high-fidelity/native/spatial.
Each tier has explicit performance budgets and a fallback.

## Interaction contract
Every platform maps its native input to the same semantic actions: focus → select → open conversation → speak/type → navigate → cancel → go back → help.
A tap, controller select, gaze activation or hand pinch may produce the same semantic action when authorized and supported.

## Screen-sharing contract
Screen sharing and device control are separate capabilities: VIEW_SCREEN → IDENTIFY_SURFACE → REQUEST/VERIFY_AUTHORITY → ACTION → OBSERVE_RESULT → REFRESH.
A screen stream may be read-only. Device actions require an independently authorized control channel and an observed acknowledgement. Never infer control authority from the existence of a video stream.

## Film / virtual production compatibility
The character should remain exportable into professional DCC/VFX pipelines rather than being locked to a website renderer. Preserve skeletal structure, materials, animation clips, naming, provenance and version metadata so future use in virtual production, cinematics and offline rendering can reuse the same identity.

## Accessibility
Character presence is enhancement, never the only information channel. Every meaningful action and state has a semantic/2D equivalent. Respect reduced motion, contrast, captions, screen readers, keyboard navigation and non-spatial interaction.

## Security and agency
Device adaptation never grants authority. Rendering, sensing, interaction and action permissions remain separate. A device may display IMA without being authorized to control it.

## Future-proofing rule
Do not design for an imagined universal device. Design stable contracts and portable representations, then add adapters when a real platform becomes available and testable.

## Current gate
The public site remains on the restored stable implementation. This architecture is preparation only.
3D/spatial activation is gated on LIVE-001 runtime proof: MCP handshake → widget render → BrowserGlass connection → fresh Android frame → authorized action → observed result → visual refresh → repeatable cross-host behavior.

## Evidence sources used for this preparation
- OpenAI Help Center: ChatGPT Voice / screen sharing
- OpenAI ChatGPT developer documentation
- W3C WebXR Device API
- Khronos glTF/OpenXR ecosystem
- Android MediaProjection documentation
- Android XR developer guidance
- Meta Horizon OS / WebXR guidance
- OpenUSD ecosystem guidance
- Genymobile scrcpy
No source above is treated as proof that IMA itself supports that platform.