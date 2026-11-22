# LIVE-001 — Adaptive Interactive Window Specification

Status: active canonical direction
Date: 2026-11-22

## Product name

**IMA Impact Window — חלון ההשפעה**

Technical invention family name:

**Personal Interactive Intelligence Window (PIIW)**

The name describes the intended transformation: an interactive surface that lets a person bring IMA's intelligence, context, assistance and verified actions into whatever they are doing, without requiring that activity to happen inside the IMA website.

## Core promise

The window is not a decorative floating chat.

It is a persistent, user-controlled intelligence surface that can:

- observe the authorized context around the user;
- understand what is happening;
- receive a goal or question;
- consult IMA and authorized specialist intelligences;
- propose or perform authorized actions;
- verify the real outcome;
- preserve a per-user chronological record;
- learn within the user's permissions;
- move with the user across hosts, devices and future interfaces.

Canonical loop:

**Observe → Understand → Decide → Authorize → Act → Verify → Learn → Improve → Re-test**

## Window modes

The same LIVE-001 surface must support one canonical implementation with adaptive presentation modes:

1. **Floating** — movable and resizable above the current IMA surface.
2. **Mini** — compact persistent bubble/control.
3. **Split** — occupies a user-selected portion of the screen beside the primary application.
4. **Docked** — attaches to a supported edge or window region.
5. **Full screen** — temporarily becomes the main working surface.
6. **Detached** — runs as a separate window/host when the operating system permits it.
7. **Picture-in-picture / compact system surface** — where the platform explicitly supports it.
8. **System overlay** — future native capability requiring operating-system permission.
9. **External display** — future multi-display placement.
10. **Immersive / AR / spatial** — future spatial presentation while preserving the same LIVE-001 contract.

The mode is presentation, not a second system. State, identity, permissions, timeline and provenance remain canonical.

## Window controls

The surface should continuously support, where the host permits:

- drag;
- resize width;
- resize height;
- resize from corners/edges;
- minimize;
- restore;
- maximize;
- split;
- dock;
- detach;
- move between displays;
- transparency/opacity profiles;
- compact mode;
- keyboard shortcuts;
- touch and pointer gestures;
- accessibility controls;
- orientation adaptation;
- safe-area adaptation;
- reduced-motion mode;
- automatic layout recovery after rotation or display changes.

## Context acquisition

The window must not assume it can see everything.

It should expose a capability matrix:

- current IMA page;
- current browser tab;
- DOM/accessibility tree;
- screenshot/visual context;
- selected text;
- clipboard, only when explicitly permitted;
- active application/window, only on supported native hosts;
- game context, only through supported APIs/accessibility/visual observation and within the game's rules;
- files, only with explicit permission;
- microphone/camera, only with explicit permission;
- device controls, only with explicit permission;
- external intelligence;
- remote device;
- external display;
- future sensors and spatial context.

Every capability has a state:

**DISCOVERED → ELIGIBLE → AUTHORIZED → ACTIVE → VERIFIED → REVOKED**

## Universal assistance

The user should be able to invoke the same window over many categories of software:

- games;
- browsers;
- office applications;
- design tools;
- programming environments;
- accessibility tools;
- media editors;
- education software;
- communication applications;
- operating-system interfaces;
- simulations;
- future AR/VR/spatial environments;
- future devices and robots.

The assistance model is not limited to one application category.

Examples:

- In a game: explain a puzzle, identify an objective, translate text, help understand controls, or provide strategy when the game/platform permits it.
- In programming: inspect the authorized editor context, explain an error, propose a patch, and verify the resulting state.
- In a design tool: understand the selected object, explain an operation, generate a change, and verify the visual result.
- In a browser: understand the page, fill an authorized form, submit, and verify the result.
- In accessibility contexts: adapt presentation, summarize visible information, or provide step-by-step guidance.

The window must not claim to have access to an application when the host has not granted that capability.

## Intelligence federation

The window communicates with IMA first.

IMA may delegate bounded work to connected intelligences such as OpenAI, Anthropic, Google, Meta, Microsoft, open/local models or future compatible systems.

Canonical path:

**User ↔ LIVE-001 ↔ IMA ↔ authorized intelligence(s) ↔ IMA ↔ LIVE-001 ↔ User**

No silent provider-to-provider sharing.

Every exchange carries:

- identity;
- authorization;
- context scope;
- purpose;
- provenance;
- uncertainty;
- capability;
- verification state.

## Per-user timeline

Every interactive-window session belongs to a user-scoped timeline.

The timeline records, subject to privacy minimization:

**request → observation → authorization → action → result → verification → learning signal**

Sensitive content is redacted or represented by metadata/hash rather than stored unnecessarily.

The user can inspect the timeline and distinguish:

- what they asked;
- what IMA observed;
- what IMA proposed;
- what was authorized;
- what was actually executed;
- what was verified;
- what failed;
- what remains uncertain.

## Security and agency

The window must never become an invisible control channel.

Required safeguards:

- explicit permissions;
- least-privilege context;
- visible active state;
- user-controlled stop/pause;
- revocation;
- sensitive-action confirmation;
- audit trail;
- provenance;
- anti-confusion labeling of IMA versus external intelligences;
- no fabricated verification;
- no silent transfer of private context;
- no bypass of application/platform security controls.

For games and other interactive software, assistance must respect the application's terms, anti-cheat mechanisms and platform restrictions. LIVE-001 must not bypass security or anti-cheat controls.

## Current implementation

As of 2026-11-22, the canonical IMA web surface includes:

- movable floating mode;
- resizable floating mode;
- mini mode;
- split mode;
- fullscreen mode;
- detachable-window route;
- persistent window geometry;
- per-session LIVE-001 identity;
- per-user action timeline;
- verified action events;
- IMA chat inside the window.

This is the web-host layer. True above-all-applications behavior is platform-dependent and requires an appropriate native host/OS capability; it cannot be truthfully claimed from a normal browser page alone.

## Native platform strategy

### Android

Use a dedicated IMA native host when available. The host can request the OS capability required for a system overlay or use supported multi-window/PiP surfaces. The web/PWA layer remains the same LIVE-001 contract.

Android explicitly supports multi-window and PiP; system overlay APIs are distinct and permission-controlled. LIVE-001 must use the least-privileged supported surface for each task.

### Windows

Provide a native desktop host capable of a topmost window, global hotkey, window movement/resizing, multi-monitor placement and optional transparency. The canonical contract remains LIVE-001 rather than a separate Windows implementation.

### iPadOS/macOS and other platforms

Use the platform's supported windowing, split-view, stage/window management, accessibility and extension mechanisms. Never assume unrestricted cross-application overlay.

### Future spatial systems

Map the same logical window state into spatial anchors, AR/VR panels, wearable displays and other interfaces.

## Continuous evolution rule

Every new host, operating system, display type, input modality or intelligence becomes a new capability adapter, not a new LIVE system.

The acceptance loop is:

**discover capability → authorize → connect → runtime test → action test → verify → timeline evidence → monitor → improve → re-test**

A feature is not considered live merely because an API or documentation exists. Runtime evidence is required.

## Intellectual-property boundary

This document records a product and architecture direction, not a legal conclusion about patentability.

Before public disclosure of enabling details, perform professional prior-art review and patent strategy review. The objective is to protect the combination of adaptive interactive surface, user-scoped continuity, authorization, cross-context assistance, verified action and auditable timeline where legally supportable.

