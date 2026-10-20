# IMA Physical Integrations

This directory is the vendor-neutral integration layer for physical devices.

## Target classes

- humanoid robots: Figure, Agility Robotics, Apptronik, 1X, Unitree, UBTECH, Boston Dynamics, Tesla and future vendors
- smart glasses/headsets
- smart watches
- smart clothing
- smart homes and appliances
- vehicles
- traffic infrastructure
- future connected devices

The repository provides the common contract and reference adapter. It does **not** claim that IMA is already installed in third-party products.

Each real vendor integration requires one of:
- an official public API/SDK
- a supported local protocol/bridge
- an app integration
- an OEM/manufacturer agreement
- a standards-based interface

The first implementation should therefore be additive: connect to the existing controller rather than replacing it.

## Integration registry

Vendor adapters should be added under:
`integrations/physical/vendors/<vendor>/<model>/`

Every adapter must declare its capabilities and authority level and must implement an emergency-stop path where the device supports one.

## Design objective

Make IMA portable across bodies without making IMA dependent on any single robot manufacturer.
