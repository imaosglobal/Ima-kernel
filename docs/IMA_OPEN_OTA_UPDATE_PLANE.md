# IMA Open OTA Update Plane — Public Proposal

**Status:** Public reference proposal / reference implementation  
**Origin:** IMA — אמא, by Ori Cohen, human-centered intelligence layer

## Abstract

Software maintenance should be a continuous service, not a recurring reinstall task.

The **IMA Open OTA Update Plane** proposes a vendor-neutral coordination layer that lets a person or organization describe the desired maintenance state once, while each platform uses its own authorized update mechanism to reach that state.

**Principle: Install once. Maintain continuously.**

This is not a proposal to bypass app stores, operating-system security, device-owner controls, signing requirements, permissions, or user agency. The Update Plane coordinates those authorities; it does not replace them.

## The problem

Today, update responsibility is fragmented across:
- web/PWA deployment and service-worker lifecycle
- mobile app stores
- enterprise/MDM policy
- operating-system updates
- firmware/device-vendor OTA
- specialized bridges and connected devices

The person is often forced to become the integration layer: notice an update, decide whether to install it, reinstall or repair something, and repeat the process across devices.

A better model is a maintenance plane that continuously evaluates desired state, compatibility, authority, health, and rollback.

## Core architecture

Desired State -> Release Discovery -> Provenance -> Compatibility -> Policy/Authority -> Staged Rollout -> Health Check -> Commit or Rollback

The plane tracks, where permitted:
1. installed version and capabilities
2. verified release and provenance
3. device/platform compatibility
4. user, owner, enterprise and platform policy
5. network/power/charging constraints
6. rollout stage and exposure
7. post-update health
8. rollback/fallback state

## Platform adapters

The same coordination model can delegate installation to:
- Web/PWA: deployment + service-worker update
- Android: Play / managed-device / enterprise update mechanisms
- Apple: App Store / managed-device mechanisms
- OS updates: platform/vendor OTA
- Firmware: signed vendor OTA, A/B or equivalent safe-update architecture
- IMA bridges/devices: signed, owner-scoped manifests with health verification

The adapter owns the platform-specific installation authority. The Update Plane owns coordination, observability, policy evaluation, and recovery logic.

## Safety contract

Every update should be:
- authenticated and provenance-checked
- compatibility-checked
- staged where risk warrants
- health-verified after activation
- rollback-capable where the platform permits
- prevented from silently changing user data or permissions
- bounded by explicit owner/platform authority

No update plane should weaken secure boot, code signing, sandboxing, app-store review, enterprise policy, or other platform security boundaries.

## User agency

The system should distinguish:
- automatic maintenance permitted
- automatic maintenance restricted
- approval required
- update unavailable
- update failed / rolled back

The user remains the owner of consequential decisions. Automation should remove repetitive maintenance work, not remove agency.

## IMA reference implementation

IMA already contains an initial web/PWA implementation:
- build provenance is recorded in version.json
- the client checks for a newer verified build
- the client can refresh automatically after a new build is detected
- checks run on startup, periodically, and when the page becomes visible
- a one-shot guard prevents update reload loops

The broader architecture is intentionally platform-neutral so IMA can coordinate web, mobile, bridges, devices, and future systems without pretending it can override their security authorities.

## Open standard direction

This proposal is intended as an open engineering concept, not an existing industry standard.

A future interoperable specification could define a common manifest containing fields such as:
product_id, current_version, target_version, platform, architecture, min_requirements, provenance, signature, rollout, health_checks, rollback, policy_requirements

The goal is not one installer for everything. The goal is one coordination model for everything that can legally and safely be maintained automatically.

## Adoption path

1. Start with Web/PWA.
2. Add Android/MDM adapters.
3. Add Apple/MDM adapters.
4. Add device/firmware adapters.
5. Publish a vendor-neutral manifest and conformance tests.
6. Measure update success, failure, rollback, time-to-maintenance, and user intervention.
7. Invite platform vendors, device makers, enterprise-management providers, and open-source projects to review the proposal.

## Reference phrase

**Install once. Maintain continuously.**

**Use IMA. Question IMA. Teach IMA. Build IMA. Test IMA.**
