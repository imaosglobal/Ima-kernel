# IMA XR Universal Adapters

## Target

IMA should have one spatial identity with platform adapters rather than separate XR products.

## Current industry interfaces

- Meta Horizon OS supports native Android, OpenXR, WebXR, Meta Spatial SDK, Unity and Unreal.
- Apple visionOS supports windows, volumes and immersive spaces.
- OpenXR provides a cross-vendor foundation for immersive devices.

## IMA strategy

Primary portable layer:

WEB → WebXR → OpenXR/native adapters

This allows IMA to start as the existing web experience, then progressively become spatial without changing Mother identity.

## XR embodiment

In XR, Mother can:

- appear as a 3D person;
- remain beside the user as an ambient presence;
- become a room-scale companion;
- speak with spatial audio;
- respond to hand/controller/gaze input where permitted;
- place knowledge, creation and tools into spatial panels;
- move between windowed and immersive modes;
- adapt scale and distance for accessibility;
- preserve the same identity and authorized continuity.

## Privacy boundary

Camera, microphone, eye tracking, hand tracking, room maps and spatial anchors are sensitive capabilities.

IMA must request only what is needed, explain why it is needed, and never treat sensor access as permission for unrelated surveillance.

## Integration ladder

1. LIVE: responsive 3D web experience.
2. LIVE FOUNDATION: PWA/WebXR-ready architecture.
3. NEXT: Meta Horizon OS WebXR/PWA validation.
4. NEXT: OpenXR native shell.
5. NEXT: visionOS native spatial shell.
6. FUTURE: shared spatial continuity between XR ecosystems.

Every stage gets an executable verification before being marked LIVE.
