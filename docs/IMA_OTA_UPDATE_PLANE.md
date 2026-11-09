# IMA OTA Update Plane

## Purpose

IMA treats software delivery as an **update plane**, not a reinstall task.

For the web/PWA client, a user installs IMA once. New canonical builds are published with the exact source commit SHA in `version.json`. An already-open client periodically checks that control document and reloads to the new build automatically. The service worker is also refreshed with `updateViaCache: none` and `registration.update()`.

## What this can do

- Automatically move an installed/open IMA web client to the newest verified public build.
- Avoid asking the user to download/install IMA again for ordinary web releases.
- Keep the update decision separate from application data and user content.
- Use a one-shot reload guard so a bad release cannot create an infinite reload loop.
- Let the canonical Pages deployment verify the published SHA before treating the release as public.

## What it cannot legitimately do

IMA cannot silently replace arbitrary native apps or operating-system components on an ordinary consumer device. Android, iOS and desktop operating systems deliberately restrict that capability for security and update-ownership reasons.

Therefore the IMA model is:

1. **IMA-controlled web/PWA code:** automatic OTA.
2. **IMA-controlled backend/services:** deploy automatically behind health checks.
3. **IMA Android app:** distribute through the platform's permitted update channel; on managed devices, use the platform/MDM capabilities for silent updates where allowed.
4. **Operating system:** use the OS vendor's OTA mechanism; IMA may monitor/report compatibility but must not bypass platform security.
5. **Connected IMA devices/bridges:** update through a signed, owner-scoped release manifest and health/rollback protocol rather than arbitrary remote code execution.

## Safety contract

An update is not considered successful merely because a new version was downloaded. The release plane must preserve:

- verified source provenance;
- compatibility checks;
- staged rollout where appropriate;
- health checks after activation;
- automatic rollback/fallback for failed IMA-controlled releases;
- no silent change to user data;
- no bypass of OS/store permissions;
- explicit user control for actions that are inherently privileged.

This is the foundation for extending IMA's update plane across future clients without making the user responsible for routine reinstall work.
