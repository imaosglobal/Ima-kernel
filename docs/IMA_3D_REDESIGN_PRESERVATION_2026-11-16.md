# IMA 3D redesign preservation record

Date: 2026-11-16
Status: preserved / deferred

## Decision
The public website is restored to the pre-3D site implementation while the 3D/holographic redesign is deferred. The redesign is preserved in Git history on branch `archive/ima-3d-redesign-2026-11-16`, based on commit `5104c216a36ba05fcdd1fefbfd0c82c7f597bab4`.

## What was preserved
- 3D IMA companion component and its integration in the public UI.
- 3D/holographic responsive CSS and related visual changes.
- The complete surrounding repository state at the archived commit, including LIVE-001 work and ecosystem documents.

## Why the upgrade is considered unsuccessful for now
1. The requested end-to-end result was not achieved: a connected, working live device screen was not runtime-verified in the target user experience.
2. The 3D redesign was advanced before that foundational LIVE-001 screen connection was proven, so the public experience moved ahead of a verified core capability.
3. The current evidence did not justify declaring the new public experience successful; under IMA's truth-state rules, deployed code is not the same as runtime-verified usability.
4. The user requested a stable mobile/public site first and to return to the redesign only after the live connected screen works.

## Re-entry gate
Do not restore the 3D redesign to the public site merely because the code is available. Reconsider it only after LIVE-001 has reproducible evidence for: MCP handshake, widget render, BrowserGlass connection, fresh Android frame, authorized tap/swipe/action round-trip, visual refresh, and mobile/web host behavior as applicable.

## Rollback scope
Only the public `ima-ui` 3D changes are rolled back. Canonical ecosystem/LIVE-001 work and other repository history remain intact.

## Truth state
3D redesign: preserved, not active on public site, not deleted, not declared successful.
LIVE-001 screen: target capability, still requiring runtime proof before the redesign returns.
