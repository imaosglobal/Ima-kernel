# IMA Voice Security Policy

## Purpose
IMA may create or transform speech and singing only for an authorized voice profile.

## Consent
- A personal voice profile requires explicit consent from the speaker.
- A profile is private by default and is never inferred from a person's name, photo, or public presence.
- Third-party voice imitation is blocked unless the speaker has explicitly authorized the profile.

## Identity boundaries
- Human identity, voice profile, source recordings, generated speech, singing conversion, and final media are separate asset classes.
- A generated file must never be presented as an authentic historical recording when it is synthetic.

## Prohibited use
IMA must refuse voice generation intended for impersonation, fraud, deception, authentication bypass, fabricated testimony, or evasion of biometric controls.

## Provenance
Every authorized voice profile records, where available:
- consent status and timestamp
- source asset identifiers
- source URL or storage reference
- processing method/provider/model
- creation timestamp
- content hash
- revocation state

## Revocation
The profile owner can revoke a voice profile. Revocation blocks new generation and marks dependent assets as revoked where the provider permits.

## Retention and transport
- Private by default.
- Minimize raw-audio retention.
- Prefer short-lived signed media URLs for transport.
- Never place private raw recordings or provider credentials in source control.
- Git stores metadata and policy, not private raw voice recordings.

## Generation controls
- Speech generation may use an authorized custom voice.
- Singing conversion requires an authorized singing source and an authorized voice profile.
- The system must not silently substitute another person's voice when a requested personal voice is unavailable.

## Audit
Record security-relevant decisions and provenance without retaining unnecessary raw audio.

## IMA default
If consent, ownership, identity, provenance, or authorization is unclear, do not generate the voice.
