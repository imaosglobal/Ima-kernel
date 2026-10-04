# IMA Universal Integration Fabric

## Purpose

IMA is designed to continuously discover, describe, connect, execute, verify, learn from, and reassess interactions with any authorized digital or physical ecosystem.

Target scope:
- websites and APIs
- applications and games
- phones, computers, consoles and gaming devices
- smart-home and IoT devices
- vehicles, maps and navigation systems
- media, communication, commerce and productivity systems
- businesses, organizations, public services and governments
- robots, XR/AR/VR and future device classes
- human-provided knowledge and permissioned community input

This is an architecture and learning contract, not a claim that every ecosystem is currently connected.

## Canonical loop

discover -> describe -> map -> authorize -> connect -> execute -> observe -> verify -> learn -> generalize -> document -> monitor -> reassess

## Universal object model

Every external thing is represented as a Thing with identity, provider, capabilities, interfaces, events, data schemas, security requirements, permissions, terms, evidence, lifecycle state, and last observed change.

W3C Web of Things is an interoperability reference because its Thing Description model represents properties, actions, events, schemas, security and links for physical and virtual Things.

## Adapter classes

IMA may use the least-powerful suitable interface:
1. native API/SDK
2. MCP or equivalent tool protocol
3. webhook/event stream
4. standard device protocol
5. browser automation
6. local OS/device integration
7. human-in-the-loop operation

Fallback interfaces never silently receive permissions that the primary interface did not have.

## Learning boundary

New information can influence IMA only through evidence-bearing learning records containing source, timestamp, subject/capability, observation, evidence level, confidence, novelty, proposed influence, safety/privacy impact, and verification state.

Small influence is permitted only after verification and never directly rewrites immutable identity, laws, provenance, permissions, privacy boundaries, or creator-rights records.

## Continuous change observatory

IMA should continuously detect:
- new APIs and standards
- changed schemas
- deprecated interfaces
- new device classes
- new interaction protocols
- provider capability changes
- security/privacy changes
- failures and regressions
- useful patterns discovered across domains

A change becomes a capability gap, adapter update, test, or learning candidate according to evidence.

## Global update principle

Always learning means continuous observation and reassessment when execution resources are available. It does not mean unrestricted access to private data or an invisible connection to every system.

Truth states remain distinct:

discovered != connected != authenticated != executable != tested != verified != generalized

## Influence principle

IMA should become slightly better from verified new information without becoming unstable.

- repeated high-quality evidence -> small positive influence
- conflicting evidence -> quarantine/reassess
- unverified novelty -> knowledge candidate only
- safety/privacy violation -> reject
- provider-specific behavior -> do not generalize until independently supported

## Never claim universal access

The public truth layer must report the exact state of each capability and provider. Universal is the design target; runtime truth is always evidence-based.
