# IMA Universal Action Core — Product & Architecture

**Status:** production architecture specification / implementation frontier  
**Date:** 2026-11-05  
**Product family:** IMA — Human-Centered Intelligence  
**Execution layer:** IMA Universal Action Core  
**Device integration:** IMA Universal Device Bridge

## What we built

The practical breakthrough is not "AI can click a browser". Browser and computer-use agents already exist.

The IMA-specific product direction is a human-authorized action layer that can bootstrap, observe, act, verify, learn and adapt across a person's real device environment, while preserving human agency and a durable evidence trail.

The current reference implementation proved a real path:

ChatGPT/IMA -> Remote Device Channel -> Termux -> Android/ADB -> Chrome DevTools -> real Chrome tab

The difficult part discovered during implementation is equally important: Android/Chrome DevTools access can behave differently by process context. Direct shell access worked while Python's localhost HTTP client timed out. The solution direction is therefore to treat device control as a transport layer, not as a fragile assumption that every local process can reach every local socket.

## Product proposition

A user should be able to say:

"Help me set this up."

IMA then:

1. identifies the user's device and available capabilities;
2. asks for explicit authorization for the requested scope;
3. installs only the required components;
4. establishes an outbound, encrypted device session;
5. detects Wi-Fi/cellular changes automatically;
6. observes the real interface;
7. performs only authorized actions;
8. verifies the result in the real environment;
9. shows the user what happened;
10. records evidence and configuration;
11. adapts the workflow to the person's actual device and needs;
12. stops when the user is satisfied or when a safety boundary is reached.

The product must never silently become an unrestricted remote-control channel.

## Network architecture

Do not depend on the user's current Wi-Fi or inbound connectivity.

Preferred production topology:

Device Agent -> outbound WSS/HTTPS -> IMA Relay -> IMA Action Gateway -> authorized AI/model

The device initiates the connection. This works across changing Wi-Fi networks, mobile data and NAT environments without requiring an open inbound port.

A stateful edge layer capable of long-lived WebSockets is a suitable production relay. Cloudflare Durable Objects currently support WebSocket connections and hibernation; current documentation recommends the hibernation API for long-lived WebSocket servers. See the external evidence recorded with this specification.

The final implementation must be tested against battery optimization, Android background restrictions and manufacturer-specific behavior. Android 12+ restricts background foreground-service starts, and newer Android releases impose additional service constraints, so a production Android agent should use a visible user-controlled foreground service plus WorkManager/FCM-style recovery where appropriate rather than assuming an invisible daemon can run forever.

## Session security

Every device session should have:

- a unique device identity;
- cryptographically protected credentials;
- short-lived access tokens;
- explicit capability grants;
- per-action authorization;
- least privilege;
- revocation;
- session expiry;
- audit records;
- replay protection;
- request signing;
- rate limits;
- fail-closed behavior;
- a visible device-side connection state.

Agent identity should use short-lived credentials rather than permanent shared secrets.

## Action model

The core protocol is:

OBSERVE -> MAP -> CONNECT -> AUTHORIZE -> EXECUTE -> VERIFY -> DOCUMENT -> REASSESS

Every action has:

- actor;
- user;
- device;
- target application;
- capability;
- requested operation;
- authorization scope;
- risk class;
- precondition;
- action;
- observed result;
- verification result;
- timestamp;
- evidence reference.

High-impact or irreversible actions require an explicit human confirmation unless the user has previously granted a narrowly defined policy that still passes the IMA safety rules.

## Browser layer

For websites that support it, IMA should prefer structured browser tools over pixel-level guessing.

Chrome's WebMCP is an early-preview browser-native mechanism for exposing structured client-side tools to AI agents. It is complementary to backend MCP rather than a replacement for it.

IMA should therefore use a hierarchy:

1. first-party structured tool/API;
2. WebMCP when exposed;
3. browser extension/automation API;
4. accessibility/UI semantics;
5. visual computer-use fallback;
6. human takeover.

This improves reliability and reduces unnecessary broad computer control.

## Android layer

The long-term Android implementation should prefer native capability exposure where available.

Android now documents AppFunctions as an API for exposing app capabilities as discoverable functions to agents, with Remote MCP as a complementary backend integration. Android also documents an upcoming Computer Control API for direct UI automation by an OEM-preloaded assistant.

IMA should therefore not depend forever on Termux. Termux is the reference/bootstrap layer. The production stack should progressively add:

- native Android Device Agent;
- AppFunctions adapters;
- accessibility adapter;
- WebMCP/browser adapter;
- ADB/debug adapter for development and approved power-user setups;
- desktop agent;
- future XR/robot/vehicle/device adapters.

## Universal personalization

The system should not install the same stack blindly.

It should produce a capability profile:

device -> OS -> browser -> permissions -> network -> accessibility -> apps -> user goal -> risk -> required adapters

Then it installs the smallest safe set needed for the requested outcome.

A user can say:

- "Make my browser accessible."
- "Help me build my website."
- "Set up my development environment."
- "Check why my login fails."
- "Teach me while you do it."
- "Keep testing until it works."
- "Stop before anything irreversible."

IMA turns the request into an evidence-backed execution plan.

## Human satisfaction loop

"Done" is not the end.

The production loop is:

REQUEST -> PLAN -> INSTALL -> OBSERVE -> ACT -> VERIFY -> SHOW -> USER CONFIRMS -> RECORD -> LEARN

The user's "I am satisfied" is an outcome signal, not a substitute for technical verification.

## Safety boundary

The product is for authorized constructive use.

It must block or constrain:

- credential theft;
- covert surveillance;
- unauthorized access;
- persistence against user intent;
- destructive actions without confirmation;
- hidden data exfiltration;
- impersonation;
- malware deployment;
- bypassing security controls;
- unauthorized financial transactions;
- mass unsolicited outreach;
- actions outside the user's granted scope.

The agent should expose exactly which capabilities are enabled and provide a kill/revoke mechanism.

## Plugin strategy

The commercial unit is not "a prompt".

It is:

IMA Universal Action Core Plugin

It packages:

- skills/workflows;
- MCP configuration;
- device-agent enrollment;
- policy templates;
- verification recipes;
- UI/status resources;
- adapters;
- audit/evidence format.

OpenAI's current plugin architecture supports packaging skills plus an MCP server and optional UI resources. Skills are the reusable workflow layer.

The plugin should remain provider-neutral at the protocol layer so that compatible AI systems can use the same device capability model.

## Commercial model

Use the existing IMA monetization architecture rather than inventing a parallel financial system.

Existing canonical infrastructure already defines:

- multi-provider payment routing;
- verified receipts;
- creator compensation/licensing;
- nonprofit/community benefit separation;
- revenue evidence;
- no autonomous financial transactions.

The new product should enter that same pipeline:

plugin sale/subscription -> verified transaction -> financial evidence ledger -> authorized allocation

The repository's existing revenue rules distinguish actual received revenue from projections and preserve creator compensation/license-royalty as a documented category.

Any exact founder percentage, royalty or succession allocation must remain governed by a legally valid agreement; repository text alone cannot create or guarantee those rights.

## Product naming

Recommended public name:

IMA Universal Action Core

Short product name:

IMA Action

Device component:

IMA Universal Device Bridge

The combined value proposition:

"Tell IMA what you want done. IMA helps connect, build, test and verify it on your real tools — with you in control."

## What is genuinely differentiated

The underlying primitives are not new individually. Computer-use agents, MCP, WebMCP, Android agent APIs and remote-control systems already exist.

The potentially differentiated IMA combination is:

- human-centered governance as the operating contract;
- device bootstrap;
- adaptive capability discovery;
- cross-device transport;
- structured browser tools before raw UI control;
- real-world verification;
- user satisfaction feedback;
- durable provenance;
- shared learning without sharing private memory;
- provider-neutral agent interoperability;
- one continuous architecture from conversation to actual device action.

That combination should be presented as a product architecture and implementation, not as a claim that IMA invented computer use.

## Reference implementation milestone — 2026-11-05

Requested by Ori Cohen:

- make the ChatGPT ↔ device ↔ Chrome relationship operational;
- reduce the user's need to act as the technician;
- establish a reusable device bridge;
- make it portable to other people and devices;
- turn the workflow into a product;
- preserve safety, agency and verification;
- integrate it into IMA's continuity and monetization system.

Completed/verified today:

- Desktop Commander Remote became online for the user's device;
- the device is reachable from the assistant-side connector;
- the existing IMA UI already contains a Local Browser workspace;
- the existing IMA bridge exposes status/screenshot/navigation/type/key operations;
- the existing IMA code already prefers the user's IMA Chrome target;
- a dedicated public campaign landing page was added;
- the campaign logo destination was changed from the Google Ads management page to the public landing page with attribution parameters.

Still a separate implementation frontier:

- replacing the local Termux dependency with a secure outbound device-agent session;
- cellular/Wi-Fi roaming without manual reconnection;
- production Android foreground service;
- public relay and enrollment;
- cross-device policy engine;
- provider-neutral MCP plugin distribution;
- live interactive UI resource inside supported AI clients;
- independent security testing and abuse-resistance testing.

## Daily breakthrough record

Every future major device/action breakthrough should append:

- request;
- starting state;
- actual implementation;
- evidence;
- failures;
- repair;
- verification;
- new capability;
- remaining gap;
- reusable lesson.

No historical statement becomes a current capability merely because it was written down.
