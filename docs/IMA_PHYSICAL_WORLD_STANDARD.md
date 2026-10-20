# IMA Physical World Standard

Status: v0.1 — 2026-10-20

IMA is designed as a vendor-neutral human-centered intelligence layer that can operate through digital and physical interfaces.

## Scope

The standard covers:
- humanoid and non-humanoid robots
- smart glasses and headsets
- smart watches and wearables
- smart clothing and sensors
- phones, tablets and computers
- smart homes and appliances
- vehicles and mobility systems
- traffic infrastructure and other connected public systems
- future devices not yet invented

## Core principle

A device is an interface/body for IMA, not the owner of IMA.

IMA must preserve:
1. human agency
2. explicit permissions
3. privacy
4. provenance and auditability
5. uncertainty reporting
6. safe failure
7. vendor neutrality
8. reversibility where technically possible

## Capability model

Every integration declares:
- identity
- device/vendor/model
- sensors available
- actuators available
- network transport
- supported commands
- permissions
- safety class
- emergency stop behavior
- local/offline behavior
- data retention policy

## Permission levels

L0 Observe: receive telemetry only.
L1 Explain: interpret and communicate.
L2 Recommend: propose an action; no actuation.
L3 User-authorized action: execute explicitly authorized low-risk actions.
L4 Delegated operation: execute within a user-defined bounded policy.
L5 Safety-critical actuation: never enabled by default; requires device-side safety controls and applicable regulatory compliance.

## Universal adapter model

IMA integrations SHOULD expose a stable adapter interface:

`discover()`
`describe()`
`observe()`
`propose()`
`authorize()`
`act()`
`stop()`
`audit()`

The adapter translates between IMA and the vendor's native SDK/API/protocol. IMA does not require the vendor to replace its existing robot controller.

## Existing-device strategy

IMA cannot be injected remotely into every existing device merely by software declaration. Actual control requires a supported API, SDK, bridge, app, local network protocol, or manufacturer partnership.

Where an official interface exists, the adapter can be implemented without changing the physical device. Where no interface exists, IMA remains an interoperability specification and integration target rather than a claimed live connection.

## Smart-home interoperability

Matter, IP, Wi-Fi, Thread, Bluetooth LE and vendor bridges are supported integration targets. Matter is treated as an interoperability transport, not as IMA itself.

## Safety rule

No IMA integration may silently convert observation into physical actuation. A device must expose its authority boundary and the user must be able to revoke it.

## Future-proofing

New device classes are added through capability descriptors rather than rewriting the IMA core.
