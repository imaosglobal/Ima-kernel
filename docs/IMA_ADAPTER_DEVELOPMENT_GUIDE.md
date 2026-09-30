# IMA Adapter Development Guide

## Rule

Build one adapter per real provider or protocol, but keep the IMA core provider-neutral.

## Minimum implementation

An adapter must expose:
1. metadata
2. capability list
3. authorization requirements
4. health check
5. request validation
6. execution boundary
7. normalized response
8. provenance
9. audit event
10. revocation path
11. automated tests

## Examples

Smart home:
Matter -> devices -> inventory/status/control where authorized.

XR:
WebXR -> browser immersive session.
OpenXR -> native headset runtime.

Delivery:
merchant/order -> delivery provider -> tracking -> confirmation.

Robot:
manufacturer SDK -> permitted robot capabilities -> safety policy -> human authorization.

## Testing

Every adapter needs:
- schema test
- authorization test
- failure test
- timeout/rate-limit test
- provenance test
- capability truth test
- revocation test
- live smoke test when credentials and provider environment exist

## No fake integrations

Source code, documentation or a public API must not be interpreted as a LIVE integration. LIVE requires an authorized connection and reproducible verification evidence.
