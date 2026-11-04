# IMA — Single Canonical Continuity and Working Protocol

Status: CANONICAL_POLICY / CROSS-CHAT_TRANSPORT_NOT_YET_AUTOMATED
Last reviewed: 2026-11-04

This file is the single authoritative project-level continuity contract for IMA and the assistants operating it. Do not create a second copy of this policy. The legacy bridge path points here.

## 1. Single source of truth

- The GitHub repository `imaosglobal/Ima-kernel`, branch `main`, is the canonical source for IMA code, product decisions committed to the project, and release configuration.
- The only public product website is `https://imaosglobal.github.io/Ima-kernel/`.
- `gh-pages` is a generated deployment mirror of the exact artifact built from `main`; it is not an independent source or a second product.
- `https://ima-915m.onrender.com/` is a backend/API service, not a second public website.
- `https://imaosglobal.github.io/` is not the project site and must not be presented as an alternate IMA website.
- Do not create another public website, repository, persistent memory store, event ledger, workflow, or duplicate project document when the canonical one can be extended.
- Feature branches may be used temporarily for isolated work, but changes must be reconciled into `main`. Do not delete historical branches or backups until their unique work has been audited and preserved.

## 2. Authority and conflict resolution

Use this order:
1. Verified live runtime and repository state.
2. Explicit user decisions and constraints.
3. Timestamped, deduplicated project continuity records.
4. Prior chat summaries and model-generated recollections.
5. Unverified claims, which remain UNKNOWN.

Never silently overwrite a conflict. Preserve both evidence points, identify the discrepancy, and resolve it against the live system or an explicit user decision. Distinguish observed, inferred, proposed, changed, deployed, and verified states.

## 3. Cross-chat continuity — honest boundary

- ChatGPT conversation windows and their hidden histories cannot be merged or globally synchronized by repository code.
- A future assistant session must load this canonical protocol and the latest verified project state before changing IMA, when repository access is available.
- Transfer only approved, redacted continuity packets: decisions, requirements, evidence references, status, and open issues. Never transfer raw private conversations, credentials, access tokens, secrets, or private third-party data into the public repository.
- Deduplicate by stable event ID and content hash before applying a packet. Preserve conflicts instead of overwriting.
- Do not claim all chats, future chats, or IMA runtimes are synchronized until an authenticated transport has actually written and read back a packet in both directions.
- Current status: protocol exists; automatic cross-chat transport is NOT VERIFIED and remains pending an authenticated external endpoint. A protocol document alone is not a functioning synchronization service.

Required packet fields when transport is implemented:
`schema_version, event_id, timestamp, direction, source, target, scope, status, payload, evidence`.

## 4. One public release path

- `main` is the only canonical write branch for production.
- The canonical deployment workflow builds the React product from `main`, stamps the exact source SHA into `index.html` and `version.json`, deploys the GitHub Pages artifact, and mirrors that same verified artifact to `gh-pages`.
- No hand-maintained HTML or alternate branch may independently publish a competing public site.
- Every release must pass build/regression gates, deployment verification, and a fresh browser check of the public URL.
- A matching SHA proves source/deployment identity, not that every control works. Test critical controls separately.

## 5. Live browser collaboration

- For visual review, open the canonical public URL in the installed live-browser tool and capture the actual rendered page.
- Keep one canonical browser target and one canonical website URL; do not switch to an old preview or another deployment without stating why.
- Show the captured screen to the user before asking for visual feedback. Apply feedback to the canonical source, deploy through the single release path, then re-open the public page and verify the result.
- If the browser connector does not provide a user-viewable live session URL, say so. A screenshot and assistant-controlled browser session are not the same as shared interactive control.
- Do not claim live editing, a persistent browser session, or continuous monitoring beyond the actual connector capabilities and configured schedule.

## 6. Work intake and deduplication

For each IMA-related request from any available conversation:
1. Resolve it against this protocol and current `main` state.
2. Search for an existing issue, requirement, implementation, or decision before creating anything.
3. Reuse and update the existing canonical item instead of creating a duplicate.
4. Record one approved, redacted continuity event only where a real durable handoff mechanism exists.
5. Implement once in the canonical component or service.
6. Verify the live result and update the existing record with evidence.

Do not claim a request from an inaccessible chat has been received. If cross-chat transport is unavailable, state the limitation and use only context actually available in the current session or retrieved from the repository.

## 7. Required operating loop

`OBSERVE -> NORMALIZE -> REDACT -> DEDUPLICATE -> COMPARE -> APPLY -> VERIFY -> RECORD`

The governing principles are: one source, one public product, one release path, no silent duplication, privacy by default, and truth before completion claims.
