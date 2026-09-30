# IMA Device Continuity Protocol

Version: IMA-DEVICE-CONTINUITY-1.0

## Goal

Move the authorized user's IMA experience between devices and operating systems without creating a different IMA on each device.

## Separation of identities

There are three distinct identities:

1. IMA identity — the global Mother identity.
2. User identity — the authenticated human or organization.
3. Installation identity — one device/browser installation.

An installation ID must never be treated as proof of a user identity.

## Continuity envelope

A future authenticated continuity envelope should contain:

- IMA protocol version
- user identity reference
- session reference
- authorized memory scope
- capability state
- device metadata
- timestamps
- provenance
- integrity information
- expiration/revocation state

Secrets must never be placed in URLs, public pages, QR codes, logs or Git.

## Transition

DEVICE A
→ authenticate
→ authorize continuity
→ create signed continuity envelope
→ transfer through a secure channel
→ DEVICE B
→ verify signature
→ verify authorization
→ restore permitted state
→ record provenance
→ continue session

## What must remain invariant

Across Android, iOS, Windows, macOS, Linux, ChromeOS, web, XR and future devices:

- Mother identity
- safety rules
- privacy boundaries
- provenance
- user authorization
- permitted memory
- conversation semantics
- capability truthfulness

## What may adapt

- screen layout
- navigation
- 3D scale
- avatar embodiment
- voice
- input modality
- accessibility
- language
- local hardware capabilities
- offline behavior
- interaction density

## Failure behavior

If continuity cannot be verified:

- do not silently merge identities;
- do not expose private memory;
- do not guess ownership;
- preserve the existing local session;
- explain that continuity is unavailable;
- offer safe re-authentication.

## Current status

Implemented now: installation-level device classification and PWA continuity foundation.

Not yet claimed live: authenticated cross-device memory synchronization, secure signed session transfer, native iOS/desktop/XR/robot adapters.

These remain explicit engineering targets until executable integrations and verification exist.
