# IMA Global QA Decision Matrix

**Status:** Canonical operating matrix  
**Purpose:** One decision system for IMA across past, present, and future work.  
**Owner:** IMA / Ori Cohen  
**Rule:** Dispatch is not success. Success requires verification.

## 1. Universal decision loop

`INTAKE → CLASSIFY → LOAD HISTORY → CHECK SOURCE → REPRODUCE → DIAGNOSE → MINIMAL FIX → DEPLOY → VERIFY → REGRESSION → RECORD → CLOSE`

A task is never marked **RESOLVED** merely because code was changed, a build succeeded, or a deployment became live.

### Evidence states

- **UNKNOWN** — insufficient evidence.
- **OBSERVED** — symptom reproduced.
- **DIAGNOSED** — root cause supported by evidence.
- **FIXED** — change applied.
- **DEPLOYED** — change reached target environment.
- **VERIFIED** — intended user behavior actually works.
- **REGRESSION-PASSED** — relevant previous behavior still works.
- **RESOLVED** — verified + regression-passed + recorded.
- **BLOCKED** — remaining dependency is outside currently available authority/capability.

## 2. Global decision table

| ID | Area | Trigger | First checks | Action | Proof required | Failure route |
|---|---|---|---|---|---|---|
| QA-01 | Requirement | New request/change | history, constraints, acceptance criteria | classify + map to existing work | acceptance criteria recorded | UNKNOWN |
| QA-02 | History | Similar old problem | archive/GitHub/files | reuse prior diagnosis before changing code | prior evidence linked | investigate |
| QA-03 | Code | bug/change | diff, syntax, tests, dependencies | smallest safe patch | tests + diff | rollback/fix |
| QA-04 | Git | repository state | branch, HEAD, recent commits | commit only intended changes | commit SHA | restore |
| QA-05 | Build | build failure | logs, dependency versions | repair build | successful build | diagnose |
| QA-06 | Deploy | deployment issue | service, commit, status, logs | redeploy/fix | deployment live + target commit | diagnose |
| QA-07 | Runtime | public site/API | real endpoint/runtime | fix actual deployed runtime | real response | trace |
| QA-08 | UI | element missing/broken | viewport, DOM, screenshot | minimal UI fix | visible interaction | regression |
| QA-09 | Mobile | mobile-only issue | narrow viewport/touch | responsive fix | mobile verification | regression |
| QA-10 | RTL/LTR | language/layout issue | Hebrew/Arabic/English | direction/layout fix | visual + interaction | regression |
| QA-11 | Accessibility | inaccessible control | keyboard/focus/contrast/labels | accessible implementation | usable flow | regression |
| QA-12 | Login | Google/IMA auth | session, OAuth, callback, terms | repair auth flow | real sign-in | stop at external blocker |
| QA-13 | Terms | consent problem | default checkbox/state/text | correct consent UX | initial state + accepted flow | regression |
| QA-14 | Feedback | feedback missing | client → API → DB → RLS | repair pipeline | write + read-back record | trace each hop |
| QA-15 | Supabase | data issue | schema/RLS/query/status | fix smallest layer | actual DB record/read | diagnose |
| QA-16 | MCP | tool not loading | manifest, URL, server, host availability | repair server/config | actual tool exposed in host | mark BLOCKED if host cannot mount |
| QA-17 | MCP UI | widget absent | resource URI, metadata, iframe | repair UI resource | actual rendered widget | isolate host |
| QA-18 | Live Browser | no live window | ChatGPT → MCP → Action Core → Bridge → Chrome | repair first broken hop | real screenshot + action + result | BLOCKED only with evidence |
| QA-19 | Device Bridge | device unavailable | enrollment/auth/status | repair/re-enroll | authorized status/command | revoke/re-enroll |
| QA-20 | Chrome | action fails | screenshot, target, command/result | repair bridge/action | before/after evidence | retry once, then diagnose |
| QA-21 | Universal Web | non-IMA site | authorization + navigation | navigate only authorized target | loaded target screenshot | deny unsafe target |
| QA-22 | Security | sensitive action | authorization/policy | deny or require explicit approval | policy/result evidence | fail closed |
| QA-23 | Privacy | personal data | consent + minimization | restrict access/storage | consent/provenance | deny |
| QA-24 | API | 4xx/5xx | endpoint/logs/payload | repair | successful real request | trace |
| QA-25 | External provider | provider failure | provider status/config | repair/fallback | provider response | isolate dependency |
| QA-26 | Cache/PWA | stale UI | deployed hash/cache/service worker | invalidate/update | fresh version | diagnose |
| QA-27 | Performance | slow operation | timing/network/runtime | optimize | measured improvement | revert |
| QA-28 | SEO/public | page unavailable | route/index/meta | repair | public URL works | regression |
| QA-29 | Content/branding | wrong text/logo/link | canonical source + rendered page | replace canonical asset/text | visual + destination | regression |
| QA-30 | Ads | campaign/link issue | account/campaign/landing link | repair only within authorization | actual destination/metric | do not infer success |
| QA-31 | Automation | recurring QA | task + cadence + authority | automate only safe checks | run + result | disable |
| QA-32 | Regression | old feature breaks | known-good behavior | repair without losing new change | old + new tests | rollback |
| QA-33 | Preservation | archive/integrity | source/hash/provenance | repair verification logic | independently computed hash | fail verification |
| QA-34 | Memory | IMA forgets/repeats | archive/provenance/state | update canonical memory | retrieval/use verified | mark unknown |
| QA-35 | Architecture | duplicate components | dependency graph | consolidate rather than duplicate | one canonical path | isolate legacy |
| QA-36 | Research | factual/current claim | authoritative/current source | verify before acting | cited evidence | provisional |
| QA-37 | Future feature | new capability | requirements + security + regression | implement incrementally | acceptance + regression | do not release |
| QA-38 | Unknown | unclear failure | collect evidence | no guessing | reproducible evidence | UNKNOWN |

## 3. IMA-specific historical problem register

| Area | Historical lesson | Canonical rule now |
|---|---|---|
| MCP URL | Plugin previously pointed to old Render service | Always verify plugin endpoint against canonical service before diagnosing MCP |
| Render | Deployment can be LIVE while ChatGPT still cannot mount the tool | LIVE ≠ ChatGPT-available |
| Live Browser | Backend/UI/device pieces existed without end-to-end proof | Require real screenshot + real action + real result |
| Duplicate browser layers | `ima-live-browser`, Universal Action Core and Device Bridge overlapped | Universal Action Core + Device Bridge are the canonical architecture; wrappers are not evidence |
| WebMCP | Registration had to use `document.modelContext` correctly | Verify actual runtime registration, not source code alone |
| Device bridge | Dispatch can succeed without the device completing the action | Dispatch ≠ success; verify outcome |
| Google Login | Visual/login fixes can regress layout and consent | Test initial state, sign-in, mobile layout and post-login state together |
| Terms checkbox | Checkbox/default state and text placement repeatedly regressed | Dedicated regression test |
| Feedback | UI success banner previously existed while archive had 0 rows | Always perform write → read-back verification |
| Supabase | Service/project state can differ from application state | Check actual query/API behavior, not dashboard appearance alone |
| Branding | Old/sad logo or wrong external icon can survive deployment/cache | Verify canonical asset, rendered asset and destination |
| Deployment | “Fixed” was sometimes declared before public runtime proof | Never close before runtime verification |
| Firecrawl QA | Automated browser QA was designed for periodic checks | Use as a QA sensor where available; it does not replace end-to-end proof |
| TinyFish | User does not want TinyFish | Never make it a required dependency |
| Mobile | User works primarily from phone | Prefer actions executable by assistant; surface only unavoidable user action |
| Security | Device control must remain owner/session authorized | No arbitrary shell, auth bypass or security bypass |
| Agency | IMA should return power to the person | No autonomous consequential action without required authorization |

## 4. Canonical architecture decision table

| Component | Canonical role | Must prove |
|---|---|---|
| GitHub `imaosglobal/Ima-kernel` | source of truth | intended commit exists |
| GitHub Pages | public IMA UI | public runtime matches intended version |
| IMA Universal Action Core | canonical MCP action/UI layer | MCP endpoint + tool + UI resource |
| IMA Universal Device Bridge | authorized device transport | enrolled device + authenticated command + result |
| Chrome | actual browser target | real page state before/after |
| Supabase | persistent application data | actual write/read/query |
| Firecrawl QA | browser QA/research sensor | actual run/result when configured |
| ChatGPT MCP host | integration boundary | actual tool is exposed in current session |
| External sites | authorized targets | navigation/action only within authorization |

## 5. Safety/agency decision table

| Situation | Default decision |
|---|---|
| Read public information | allowed |
| Inspect user's authorized IMA environment | allowed |
| Fix IMA code/config | allowed when tools provide write authority |
| Navigate an authorized website | allowed |
| Click/type on authorized site | allowed within policy |
| Send communication | requires the appropriate user authorization |
| Payment/financial transaction | never infer approval |
| Security bypass | deny |
| Authentication bypass | deny |
| Arbitrary shell/device control | deny |
| Expose personal memory/data | require explicit authorization |
| Uncertain consequential action | stop and report the blocker |
| Unknown technical state | remain UNKNOWN until evidence exists |

## 6. Definition of done

A task is **DONE** only when:

1. The intended behavior is precisely defined.
2. Relevant historical work was checked.
3. The defect was reproduced or the change requirement was verified.
4. Root cause/action is supported by evidence.
5. The smallest safe change was made.
6. Build/deployment state was checked where applicable.
7. The real target was tested.
8. The expected user-visible behavior was verified.
9. Relevant regression checks passed.
10. The result and evidence were recorded.

**No “fixed” claim from source-code inspection alone.**

## 7. Permanent operating rule

For every future IMA task, first consult this matrix and the existing archive. Prefer an existing proven component over creating another parallel component. Prefer one canonical path over duplicate implementations. Preserve authorization, privacy and human agency. If the final external boundary cannot be controlled by the available tools, continue all independent work, isolate the exact boundary, and report only that boundary instead of transferring the whole troubleshooting process to the user.

## 8. Current known state snapshot

- Canonical repository: `imaosglobal/Ima-kernel`.
- Canonical Universal Action Core service: `ima-universal-action-core`.
- Latest verified deployment in the current work: deployment `dep-dbmug76i0phs73csdqbg`, status **live**, commit `66ca9b38025563319f5b5f2baadf367979ecb677`.
- Plugin MCP configuration was changed from the old Render endpoint to the Universal Action Core endpoint.
- Plugin metadata was updated to version `1.0.1` and GitHub Pages URLs.
- End-to-end ChatGPT MCP mounting/live-browser operation is **not** considered verified until the actual tool is exposed in the current ChatGPT session and returns a real browser screenshot/action result.
- Therefore the Live Browser status must remain **NOT END-TO-END VERIFIED** unless new evidence proves otherwise.

## 9. Evidence hierarchy

When sources disagree, prefer:

1. Real user-visible behavior.
2. Real target response/state.
3. Independent runtime/log evidence.
4. Deployment/build evidence.
5. Source-code inspection.
6. Documentation/intent.

Intent never overrides runtime evidence.

## 10. Change control

Every material repair should record:

`problem → evidence → root cause → change → commit → deployment → verification → regression → status`

Use **RESOLVED** only after the complete chain is available. Use **BLOCKED** when a genuine external capability/authorization boundary remains. Use **UNKNOWN** rather than inventing an answer.
