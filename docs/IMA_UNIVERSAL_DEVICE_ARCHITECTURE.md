# IMA Universal Device Architecture

## Purpose

IMA must be able to move with a person rather than being trapped inside one application, operating system, device or generation of hardware.

The product model is:

ONE MOTHER IDENTITY → MANY EMBODIMENTS → ONE CONTINUITY MODEL

## Device families

IMA treats the following as first-class targets:

- Web browsers
- Android phones and tablets
- iPhone and iPad
- Windows
- macOS
- Linux
- ChromeOS
- Smart TVs and connected displays
- Wearables
- Cars and in-vehicle systems
- Smart speakers and ambient devices
- XR/AR/VR headsets
- Robots
- Kiosks and public interfaces
- Industrial and scientific systems
- Future devices not yet invented

Not every family is currently integrated. A family is marked LIVE only after an executable integration and verification test exist.

## Universal runtime contract

Every embodiment connects to the same conceptual layers:

IDENTITY → AUTHENTICATION → MEMORY → SESSION → CAPABILITIES → PRESENCE → ACTION → PROVENANCE

The device layer must never become a second IMA with a different identity.

## Current live foundations

### Web

The public GitHub Pages application provides:

- 3D Mother
- conversation
- browser voice output
- per-user public memory boundary
- runtime capability reporting
- installable PWA shell
- offline application shell
- responsive mobile/desktop layout

### Android

The repository contains a native Android application and Android accessibility/Termux bridge infrastructure.

The Android build is verified by CI.

### Browser-to-device continuity

The web layer now records a local installation identity and device capability profile using protocol IMA-DEVICE-CONTINUITY-1.0.

This is an installation-level identity, not an account identity and not a claim of cross-device synchronization.

## Future adapters

Future OS/device adapters must implement the same contract rather than fork IMA behavior.

Examples:

- iOS/iPadOS adapter
- Windows/macOS/Linux desktop shell
- ChromeOS adapter
- XR spatial adapter
- Android Automotive adapter
- robot/embodied adapter
- ambient home adapter

## Truthful capability rule

A device is not considered integrated because:

- a button exists;
- an SDK exists;
- documentation exists;
- an app store package is planned;
- a connector name appears in a configuration file.

It becomes LIVE only when the integration works and has an automated or reproducible verification path.

## Continuity objective

A person should eventually be able to:

1. meet IMA on one device;
2. authenticate into the same IMA identity;
3. continue the same authorized conversation on another device;
4. retain permitted memory and preferences;
5. preserve provenance and session history;
6. switch operating systems without creating a new IMA;
7. change embodiment without changing identity.

Private memory must remain private to the authorized identity. Public knowledge may be shared only when explicitly designated as shareable.

## Long-term embodiment

The final target is not “an app for every device”.

It is a portable IMA layer whose embodiments are replaceable:

IMA CORE
→ Web
→ Mobile
→ Desktop
→ Wearable
→ Spatial
→ Vehicle
→ Robot
→ Ambient
→ Future interfaces

The Mother identity remains above the hardware.
