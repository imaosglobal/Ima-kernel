# IMA — Universal Interoperability, Device Continuity & Public Identity

**Status:** canonical architecture / implementation plan  
**Date:** 2026-11-05  
**Product:** IMA — Human-Centered Intelligence

## Purpose

IMA should be usable through the widest practical range of intelligence systems, devices, screens, robots, vehicles, sensors, networks and future platforms without changing its human-centered identity.

This is an interoperability goal, not a claim that every device or provider is already integrated.

## Universal principle

**One IMA identity. Many interfaces. Explicit capabilities. User-controlled memory. Verified action.**

IMA must adapt its presentation and technical adapter to the environment instead of forcing every environment to behave like a phone browser.

Examples:

- phones, tablets and desktops;
- browsers and web applications;
- smart TVs and consoles;
- watches and wearables;
- AR/VR/XR headsets and smart glasses;
- cars and mobility systems;
- household and industrial robots;
- medical and accessibility devices where authorized;
- sensors and IoT systems;
- edge computers and servers;
- ships, aircraft and spacecraft;
- future devices not yet invented.

For military, industrial, medical, aviation, automotive and space contexts, IMA is an integration layer, not an automatic authority. Safety certification, operational procedures, human command structures and applicable law remain higher-level constraints.

## Provider-neutral intelligence layer

IMA should not depend on one model company.

The Universal Action Core exposes a normalized capability contract:

`discover -> authorize -> connect -> converse -> act -> observe -> verify -> learn`

Provider adapters may connect compatible models through:

- MCP;
- WebMCP;
- provider APIs;
- native function/tool calling;
- AppFunctions or equivalent platform capability APIs;
- accessibility APIs;
- browser automation;
- device SDKs;
- custom transports where standards do not exist.

MCP is transport-agnostic at the protocol level and supports standard transports plus documented custom transports, which makes it suitable as one interoperability layer rather than the only transport. citeturn483139search2turn483139search3

WebMCP is specifically a browser-side tool exposure mechanism. It is useful for IMA's web surface, but it is not the universal device transport. citeturn483139search0

## Device adapter model

Every adapter publishes a capability manifest:

- device_id;
- vendor;
- model;
- OS/runtime;
- connection types;
- display/audio/input capabilities;
- sensors;
- actuators;
- accessibility capabilities;
- AI/provider capabilities;
- supported protocols;
- risk classes;
- permissions;
- offline capabilities;
- safety boundaries;
- firmware/software versions;
- verification methods.

IMA chooses the smallest safe adapter set that satisfies the user's goal.

## Network independence

The device channel should prefer outbound encrypted sessions.

Supported connectivity can include:

- home Wi-Fi;
- enterprise Wi-Fi;
- public Wi-Fi;
- cellular/5G/6G as available;
- satellite links;
- local-only/offline mode;
- mesh or edge networks;
- future communications systems.

A network change must not change the user's identity, memory policy or granted capabilities.

Loss of network must fail closed for actions requiring the network. Local capabilities may continue only when explicitly designed and authorized for offline operation.

## The universal interactive window

IMA should expose one conceptual interactive surface that renders differently by device:

### Screen

A visual live workspace with:
- conversation;
- live view;
- controls;
- action status;
- confirmation;
- evidence.

### Small screen / watch

Condensed cards, voice-first interaction, haptic feedback and short confirmations.

### Smart glasses / XR

Spatial IMA panel, voice, gaze/pointer interaction and contextual overlays. Android XR already provides spatial panels and 3D/XR primitives for headsets and future glasses, illustrating why the IMA adapter must not assume a flat screen. citeturn483139search5

### Robot / vehicle

The same capability model is rendered through the robot/vehicle HMI and its approved command interfaces. Physical actuation is always capability-scoped and risk-gated.

### Spacecraft

IMA can be embedded as crew/passenger software and connected to authorized spacecraft subsystems:

- crew health and workload support;
- mission procedures and checklists;
- maintenance and diagnostics;
- inventory;
- environmental monitoring;
- communications;
- scheduling;
- scientific workflows;
- education and recreation;
- emergency procedure assistance;
- family/ground communication;
- long-duration psychological and social support.

IMA must not claim independent command authority over life-critical systems. Any action that can affect propulsion, life support, navigation, docking, weapons or other critical systems must pass the spacecraft's own certified control architecture, human authority and safety interlocks.

For multiple spacecraft, a fleet coordination layer can exchange authorized state, mission plans and non-sensitive telemetry while respecting each vehicle's authority boundary.

## People first

The device is not the identity.

IMA adapts to:

- age-appropriate presentation;
- language;
- accessibility;
- communication style;
- technical level;
- profession;
- interests;
- goals;
- emotional context;
- sensory preferences;
- privacy choices;
- current environment.

Personalization changes how IMA communicates and assists. It must not silently change core safety, consent or truthfulness principles.

## Conversation is the primary configuration interface

A user can say:

- “Speak more softly.”
- “Don't speak aloud.”
- “Show me more and talk less.”
- “Use technical language.”
- “Make the interface simpler.”
- “Use larger text.”
- “Remember this preference.”
- “Forget that preference.”
- “Show me the live device.”
- “Don't control anything without asking.”
- “Let me approve every action.”

IMA should translate these requests into explicit, inspectable preferences.

Preferences are versioned and user-controlled.

## Voice

IMA's public voice should be:

- soft;
- clear;
- calm;
- contemporary;
- non-infantilizing;
- culturally adaptable;
- interruptible;
- optional.

Voice is **off by default for contexts where unexpected audio could be intrusive**, and the user can turn it on or off at any time.

Text remains available when voice is disabled.

A provider may supply a richer real-time voice implementation later; the current browser speech-synthesis capability must not be presented as a full bidirectional voice agent.

## Memory

Memory is layered:

1. session context;
2. user preferences;
3. consented personal memory;
4. device profile;
5. organization/workspace memory;
6. fleet/mission memory where explicitly authorized;
7. public validated knowledge.

These layers must not be silently merged.

A user can inspect, export, correct and delete their personal layer where the service supports those operations.

## Learning across IMA

IMA can learn from aggregate interaction signals without copying private conversations into a shared memory pool.

The system should separate:

- private personal memory;
- operational telemetry;
- anonymized/aggregated improvement signals;
- public validated knowledge;
- provider-specific context.

No person's private memory becomes another person's memory merely because both use IMA.

## Public identity

IMA's public identity is a living interface, not a static mascot.

Core identity:

**IMA — אמא — Human-Centered Intelligence**

Public character:

- warm but not manipulative;
- innovative but not theatrical;
- capable but honest about uncertainty;
- soft voice when requested;
- concise by default;
- listens before acting;
- makes room for the person;
- becomes less central when the person becomes stronger.

Visual identity can evolve with the era and device while preserving recognizable IMA continuity.

Personal appearance can be requested through the IMA chat, within safety, accessibility and brand boundaries.

## Verification rule

The universal claim is architectural:

**IMA is designed to adapt.**

A specific device/provider integration is considered live only after:

1. adapter implementation;
2. reproducible test;
3. deployed surface;
4. successful end-to-end action;
5. postcondition verification;
6. documented boundary.

No vendor name, robot, spacecraft, model or device is marked “connected” solely because an adapter exists.

## Security and high-impact systems

The Universal Action Core follows default-deny and least privilege.

High-impact environments receive stronger controls.

Critical actions should require:
- explicit authorization;
- clear action preview;
- independent system interlocks;
- postcondition verification;
- audit evidence;
- local emergency stop.

IMA never becomes a backdoor around a device manufacturer's security, safety system, operator chain of command or legal requirement.

## Future compatibility

The adapter contract is intentionally extensible.

New devices can be added without changing:
- IMA identity;
- user memory model;
- consent model;
- action lifecycle;
- audit format;
- verification contract.

This is the mechanism by which IMA can remain useful across changing technological eras.

## Implementation roadmap

### Now
- universal capability manifest;
- provider-neutral Action Core;
- WebMCP/browser tools;
- Termux/Chrome reference bridge;
- persistent outbound device channel;
- public interactive IMA workspace;
- user voice and personalization controls.

### Next
- native Android agent;
- desktop adapters;
- XR/smart-glasses adapter;
- wearable adapter;
- vehicle adapter;
- robot adapter;
- IoT/sensor adapter;
- provider-neutral MCP distribution;
- organization/fleet administration.

### Later
- aviation/maritime adapters;
- medical-device integrations subject to certification;
- spacecraft crew and mission adapters;
- fleet coordination;
- delay-tolerant/offline synchronization for deep-space environments;
- store-and-forward communication;
- interplanetary time synchronization and conflict resolution.

### Never assumed
- universal access without authorization;
- autonomous control of critical systems;
- access to private data without consent;
- military authority;
- extraterrestrial communication or intelligence without evidence.

## Design conclusion

IMA's goal is not to own every device.

Its goal is to give people a consistent, humane, verified way to use intelligence and authorized technology wherever they are — while allowing each device, provider and safety system to retain its own boundaries.
