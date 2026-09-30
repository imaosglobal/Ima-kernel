# IMA Universal Adapter SDK

## Status

Architecture and contracts are implemented. Individual provider integrations become LIVE only after authorization and executable verification.

## Adapter interface

An adapter implements:
- identity
- discovery
- capability declaration
- authorization
- health check
- request validation
- execution
- result normalization
- provenance
- revocation
- audit record

## Capability lifecycle

DISCOVERED -> SPECIFIED -> IMPLEMENTED -> TESTED -> VERIFIED -> LIVE

A registry entry MUST never infer LIVE from the existence of source code.

## Universal request

Every external action is represented as:

intent
context
constraints
required_knowledge
requested_capabilities
authorization
confirmation
execution
result
provenance
learning_update

## Safety boundary

Read-only knowledge operations can be automated when permitted.

Consequential operations such as purchases, publication, advertising spend, physical-device control, childcare supervision, medical workflows, vehicle control, security controls and external communications require explicit authorization and the confirmation level defined by the integration.

## Protocol targets

Initial protocol families:
- HTTPS/REST
- WebSocket
- Webhooks
- OAuth 2.x / OpenID Connect where supported
- WebXR
- OpenXR
- Matter
- Android intents/deep links
- embeddable web components
- future provider-specific SDKs

## XR

WebXR support is detected at runtime before an immersive session is offered. OpenXR is the native cross-platform target for supported XR devices.

## Smart home

Matter is the vendor-neutral smart-home target. Vendor-specific bridges remain possible where an authorized API exists.

## Delivery

Delivery providers use a common order/tracking contract. Provider selection remains explicit and regional availability is part of capability state.

## Partnership

Each provider connection records:
provider, API version, scope, permissions, geography, terms, test evidence, last verification and lifecycle state.

## Truth rule

IMA can say:
- planned
- implemented
- tested
- verified
- live

only when the corresponding evidence exists.

Never claim that IMA controls a service, device, platform or organization merely because an adapter specification exists.
