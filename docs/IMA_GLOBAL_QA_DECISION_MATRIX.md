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


## 11. Consolidated historical diagnosis — archive-derived

This section consolidates the recurring findings recovered from the prior IMA work history. It is an operational history, not a claim that every historical item is currently fixed.

### 11.1 Product and architecture history

| Period | Finding | Diagnostic significance | Permanent QA control |
|---|---|---|---|
| Aug–Sep 2026 | IMA already had canonical vision/identity/governance/runtime files | Recreating parallel “canonical” files risks divergence | Search existing canonical sources before creating new ones |
| Aug 2026 | Human-purpose layer emphasized flourishing, agency, minimum necessary harm, purpose before capability, verification before promotion | Product behavior must not be evaluated only as technical success | Include agency/harm/verification gates |
| Sep 2026 | Repo contained many UI/backend/browser/global-intelligence/governance artifacts | Repository complexity creates duplicate-path risk | Maintain dependency/canonical-path map |
| Sep 2026 | Multiple provider credentials/adapters were distributed across code | Provider abstraction was incomplete | Credential/provider checks are architecture QA, not just config QA |
| Sep 2026 | Local UI and backend API paths were mismatched (`/ima-api/ask` vs backend endpoints returning 404) | Source/UI can appear healthy while actual integration is broken | Test client → proxy → backend → response end-to-end |
| Sep–Oct 2026 | IMA expanded toward avatar, Store, community, translation, device installation | Feature growth increases regression surface | Every new feature enters regression matrix |

### 11.2 Website and UX history

| Historical symptom | Root lesson | Permanent test |
|---|---|---|
| Duplicate Google Login buttons | Incremental edits were not deduplicated | Assert exactly one canonical login CTA |
| Literal `\\n` appeared in UI | Source escaping can become user-visible | Rendered-text smoke test |
| Google button size/position drifted | UI fixes were not protected by regression | Snapshot/visual + interaction test |
| Terms checkbox/default state regressed | Consent UI is a functional requirement | Initial unchecked + required acceptance test |
| Terms text placement became incorrect | Visual correctness matters in consent flow | Mobile + desktop visual check |
| Login could work while post-login experience was wrong | Authentication and product transition were tested separately | Login → session persistence → automatic Chat transition |
| Landing page accumulated too much explanatory material | Complexity should live inside the product | Minimal landing-page content check |
| Public CTA had language/wording requirements | Copy is part of acceptance criteria | Exact CTA/content assertion |
| Chat/Community/Store navigation needed synchronization | Site/app drift is a product defect | Cross-surface route parity |
| Logo sometimes showed an old/sad/wrong mark | Canonical asset/cache/deployment mismatch | Asset hash/name + rendered-image + cache/version check |
| Logo → Ads link was wrong/incomplete | Link identity differs from campaign identity | Resolve actual destination, not just URL string |
| Install button disappeared or failed | `beforeinstallprompt` lifecycle was fragile | Install event capture + fallback + click test |
| Footer links and support/privacy/terms changed during fixes | Global layout edits caused collateral regressions | Footer link inventory regression |
| Public deployment could remain stale | Source and public build were confused | main → build → gh-pages → public runtime chain |
| GitHub Pages had competing workflows | Multiple publishers created ambiguity | One canonical publishing workflow |
| Browser verification was sometimes unavailable | “Build passed” was mistaken for UX proof | Separate build state from runtime state |

### 11.3 Authentication history

Known historical issues include Google Identity Services/FedCM/UI drift, session persistence, OAuth configuration, nonce/session verification, Android Credential Manager alignment, missing `GOOGLE_CLIENT_ID` on Render, and consent UI regressions.

**Canonical auth gate:**

`initial state → consent → Google sign-in → callback/token verification → canonical IMA session → persistence → logout → post-login Chat`

No auth release is RESOLVED unless this chain is tested at the relevant runtime.

### 11.4 Feedback and learning history

The feedback system exposed a critical class of false-positive success:

- UI could display success while durable storage failed.
- Supabase initially returned 401 because an INSERT ... RETURNING path lacked the required SELECT capability.
- Render filesystem storage was not durable enough to be the archive of record.
- The system was changed toward secured RPC/transaction behavior.
- Known verified feedback records include `16660d44-125d-4edf-952b-e9a7b411abc2`, `e2347def-35e7-4ca3-a9f5-f8394c62f759`, and `12431f0d-3a61-46de-a5e3-ddc7be021f87` from the historical work.
- Feedback was intended to flow into `feedback_archive` → `feedback_learning` / learning candidates → `feedback_actions`.

**Permanent rule:** a feedback success banner is invalid evidence until the durable record is written and read back.

### 11.5 Supabase/security history

Historical checks identified RLS/security gaps, including tables without policies and a SECURITY DEFINER function that was callable by `anon`/authenticated users. Those findings were recorded as gaps rather than silently “fixed.”

**Permanent rule:** security findings must have explicit status: RESOLVED, ACCEPTED RISK, or GAP_RECORDED. Never convert a security gap into an assumed success.

### 11.6 GitHub Pages / deployment history

The project repeatedly experienced a source-vs-public-runtime gap.

Known examples:
- stale `gh-pages`;
- competing publishing workflows;
- rollback that restored source state but did not prove public build state;
- public `version.json` lagging behind `main);
- deployment marked successful while public behavior remained unverified.

**Permanent deployment proof:**

`commit SHA → build artifact/version → published branch → public URL → public behavior`

All five are required for public release verification.

### 11.7 Google Ads / monetization history

Known campaign:
- Campaign: **IMA — בינה אנושית לכולם**
- Campaign ID: **24409551537**
- Historical account: **477-713-2721**
- Account email used in the work: `imaosglobal@gmail.com`
- User reported personal spend of **100 ₪** and required no additional spend unless justified/profitable.
- Historical metrics showed 0 impressions/clicks/spend/conversions in one checked period despite the user's reported card spend.
- Campaign/logo deep-link work repeatedly suffered from incorrect/incomplete destination context.
- A campaign ID alone was insufficient for some Google deep-link forms; account context/required parameters had to be considered.
- The public image was required to deep-link to Ads, with only Google login and install/add-to-home controls beneath it in the relevant launch layout.

**Permanent rule:** marketing “working” means verified destination + correct asset + actual campaign state/metrics. A link existing in source is not campaign success.

### 11.8 Live Browser / MCP history

The browser project evolved through several overlapping pieces:
- `ima-live-browser` plugin;
- IMA Universal Action Core;
- IMA Universal Device Bridge;
- WebMCP registration;
- Firecrawl/browser QA;
- Opera/browser connection experiments.

The principal historical failure was architectural boundary confusion: a backend could be live while ChatGPT did not actually expose the MCP tool; a provider could be configured in code while its credential was absent; a browser UI could exist while no real browser was connected.

Current canonical chain:

`ChatGPT MCP host → IMA Universal Action Core → IMA Device Bridge → Chrome → authorized website`

**Permanent end-to-end proof:**
1. MCP tool is actually exposed in the current ChatGPT session.
2. Widget actually renders.
3. Browser screenshot is returned.
4. Navigation changes the real browser.
5. Click/type changes the real browser.
6. A new screenshot/result proves the action.
7. Authorization remains valid.
8. The target can be a non-IMA authorized website.

Anything short of this remains NOT VERIFIED.

### 11.9 Firecrawl / continuous QA history

A Firecrawl Live Browser QA workflow was previously added with scheduled/manual execution and checks for mobile, branding, Google, install and links. Historical runs found:
- public site/API accessible;
- Google Sign-In/install/logo elements present;
- API status returned HTTP 200;
- UI could nevertheless falsely remain in “checking connection” state;
- canonical-site ambiguity and duplicate Install/Chat/Open IMA/Support/YouTube elements were found;
- later interactive takeover remained blocked by missing `FIRECRAWL_API_KEY`;
- Opera reported “Browser not connected.”

**Permanent rule:** automated browser QA is a sensor. It does not by itself prove a user flow unless the required interaction and resulting state are observed.

### 11.10 Mobile and accessibility history

IMA is operated heavily from a phone, so mobile is not a secondary test target.

Historical requirements:
- responsive phone/tablet/desktop behavior;
- RTL Hebrew and Arabic;
- English LTR;
- reduced motion;
- high contrast;
- controls must remain usable;
- no horizontal overflow;
- `min-width:0`/flex/grid issues were explicitly encountered;
- Google Login must not disappear on mobile;
- consent text must remain readable;
- touch controls must have reliable targets.

**Permanent rule:** every material UI release gets mobile + desktop + RTL/LTR + accessibility regression.

### 11.11 Branding/content history

Canonical public-facing requirements that repeatedly mattered:
- current campaign logo, not an old/placeholder/sad mark;
- English public CTA **“Open IMA now”**;
- Hebrew-facing product may use **אמא**, while public English may use Mom/Mother where appropriate;
- landing page should remain minimal;
- deeper philosophy belongs inside the product;
- IMA is a human-centered intelligence layer, not merely a chatbot/model connector;
- no dead buttons;
- YouTube/HeyGen destination should point to the IMA YouTube presence rather than an incorrect video banner.

**Permanent rule:** branding is tested as rendered behavior, not source text alone.

### 11.12 Preservation / Ori Digital history

IMA includes a long-term preservation direction involving Ori Digital / representation of Ori's writing, songs, values and thinking, plus lineage/preservation records.

Known preservation artifacts include:
- `ORI_COHEN_ETERNAL_PRESERVATION.md`
- `PLEASURE_SUFFERING_BALANCE_RESEARCH_PAPER.md`
- Zenodo record `10.5281/zenodo.22838744`
- preservation tag `pleasure-suffering-balance-v1.0`

**Permanent preservation QA:** provenance, integrity, version, authorization and retrieval must be independently testable. Preservation must not silently become alteration.

### 11.13 Humanitarian/global-intelligence history

IMA has also been developed as a broader human-centered intelligence and global/humanitarian system. Earlier work included global signals, procurement/RFP routes, provider routing and proof-gated execution.

Historical lesson: capability breadth must not outrun verification, authority and provenance.

For consequential global actions:

`observe → map → connect → assess → authorize → execute → verify → document → reassess`

No automatic escalation from observation to consequential action.

## 12. Historical regression catalog

The following are permanent regression families because each has already occurred or was explicitly identified as a recurring risk:

1. Source changed but public Pages stayed stale.
2. Build passed but runtime behavior was wrong.
3. Runtime/API was healthy while UI status was false.
4. Login worked but consent/layout regressed.
5. Google button duplicated/disappeared/resized.
6. Install event existed in theory but button failed.
7. Logo was correct in source but wrong in public cache.
8. Ads URL existed but destination context was wrong.
9. Feedback UI reported success but durable archive was empty.
10. Supabase dashboard state was mistaken for application state.
11. MCP server was live but ChatGPT did not expose the tool.
12. Browser widget existed but no browser was connected.
13. Provider code existed but provider credential was absent.
14. Duplicate workflows/components created ambiguity.
15. Mobile fixes introduced desktop/RTL regressions.
16. A rollback restored source but not the public artifact.
17. A new fix removed previously working functionality.
18. A “fixed” claim was made without end-to-end evidence.

Every future release should explicitly test these families where applicable.

## 13. Historical release evidence index

Known important commits/releases recovered from prior work include:

| Reference | Significance |
|---|---|
| `3b8120751af5ccc088626169e6aef8323b3d6e1f` | verified richer public UX/login/chat/community/store release |
| `be986b545ca7b90d3282d06b70eea75674530345` | Ads/logo deep-link source fix; public verification was a separate concern |
| `30e0e5434d9be13da3c441cf2af206c5001a8b5a` | feedback/archive infrastructure deployment |
| `96edbb1ba0c338a41e94f00ae553c3a6c63b511f` | service-worker `ima-shell-v4` |
| `83527dc34ba6032779fdc4b0492e551d01423ffa` | feedback API/session/install/footer-related fixes |
| `a7dbb8ca4a7683d801371f6ae1e6d7b843784105` | Firecrawl continuous QA workflow |
| `58e4ff08b58c8bbf1bb26208359767294b5c2d15` | Live Browser backend iteration |
| `cda98e4...` | historical Pages rollback; later recognized as insufficient proof of public artifact |
| `6374a186...` | richer public UX restoration |
| `2f7b3c4`, `261be5a`, `f5a8670`, `69faa19` | Pages/capability/publication work |
| `42e986820092ad51dc8cc4810c6b2b681ce916ae` | this canonical QA matrix |

## 14. Current active risk register

| Risk | Current treatment |
|---|---|
| ChatGPT-side MCP mounting | NOT END-TO-END VERIFIED |
| Live Browser actual device connection | NOT END-TO-END VERIFIED |
| Firecrawl credential/configuration | must be checked before claiming interactive Firecrawl capability |
| Public runtime freshness | always verify source → published artifact → public behavior |
| Supabase RLS/security gaps | must remain explicit until independently remediated |
| Google Ads profitability | do not infer from link/campaign existence |
| Duplicate components/workflows | consolidate/canonicalize before adding more |
| Authentication configuration | verify live provider/session, not just source |
| Feedback durability | require write/read-back evidence |
| Mobile/RTL regression | permanent release gate |
| Logo/cache mismatch | permanent asset + runtime verification |
| External consequential actions | authorization gate required |

## 15. Operating instruction for future chats

When a future chat references any IMA task, treat this document plus the existing IMA archive as the starting state.

Do not ask the user to reconstruct prior work when the archive can be searched.

Do not recreate a feature before checking whether it already exists.

Do not create a second implementation merely because the first one is difficult to find.

Do not mark a deployment successful because a provider says “live.”

Do not mark a browser successful because a widget exists.

Do not mark feedback successful because a toast appears.

Do not mark login successful because the button renders.

Do not mark Ads successful because a URL opens.

Do not mark accessibility successful because CSS exists.

Do not mark security successful because a policy file exists.

For every one of these, verify the behavior at the boundary that matters.

## 16. Archive completeness status

This matrix is now a consolidated operational index of the historical IMA issues recovered from the available prior-chat/archive context. It is intentionally evidence-graded: items with historical evidence are recorded as history; items not currently re-tested remain historical or active-risk entries rather than being falsely promoted to RESOLVED.

The archive should continue to be appended whenever a new IMA task reveals a new failure mode, root cause, regression, or proven solution.
