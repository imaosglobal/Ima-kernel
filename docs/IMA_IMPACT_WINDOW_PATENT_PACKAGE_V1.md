# IMA Impact Window — Patent Package v1

Inventor attribution: Ori Cohen
Working title: IMA Impact Window — חלון ההשפעה
Technical family: Personal Interactive Intelligence Window (PIIW)
Date: 2026-11-22
Status: private preparation package; not a patent filing and not legal advice.

## 1. Invention thesis

A user-scoped interactive intelligence space that persists across host contexts and devices and can:

1. discover host capabilities;
2. obtain explicit authorization for context access, intelligence transfer and action;
3. observe minimum-necessary authorized context;
4. route bounded tasks to one or more authorized intelligence providers;
5. return the result through IMA;
6. execute authorized actions;
7. observe the post-action state;
8. verify whether the intended state was actually achieved;
9. record a privacy-preserving chronological evidence chain for the individual user;
10. carry the logical window identity and relevant authorized continuity across host surfaces and devices;
11. learn/improve from verified outcomes;
12. adapt to new hosts without creating a separate product/window architecture.

## 2. Technical problem

Existing assistants, overlays, browser agents, accessibility tools and cross-device systems generally solve subsets of the problem: interaction, context capture, action execution, cross-device continuity, or AI assistance. The proposed system treats the interactive window, intelligence federation, authorization, action, verification and user timeline as one canonical control/evidence loop.

## 3. Canonical loop

User request
→ context discovery
→ capability negotiation
→ authorization
→ minimum-necessary context transfer
→ IMA decision
→ specialist intelligence task if needed
→ authorized action
→ post-action observation
→ verification
→ evidence/timeline event
→ learning signal
→ improvement
→ re-test.

## 4. Proposed independent-claim concepts for attorney review

### Claim family A — Personal interactive intelligence window
A computer-implemented system comprising a user-associated interactive window, a host capability adapter, an intelligence orchestration layer and a verification/timeline subsystem, wherein the logical window identity remains associated with the user while the window is represented on different host surfaces; the system obtains authorized context, invokes an authorized intelligence operation, optionally executes an authorized action, observes a resulting state and records an event linking the request, authorization, action, result and verification.

### Claim family B — Verified action timeline
A method comprising receiving a user request through a persistent interactive intelligence window; creating a user-scoped event chain; recording authorization scope; performing an authorized action; observing post-action state; determining a verification status; and appending the verification result to the chronological event chain, with sensitive content minimized or transformed before persistence.

### Claim family C — Provider-neutral intelligence federation
A method in which IMA receives a task, determines whether a direct response or specialist/cross-check/synthesis/debate/handoff mode is appropriate, invokes one or more authorized intelligence endpoints through provider-neutral adapters, receives provenance/evidence/uncertainty, synthesizes or preserves disagreement, and returns the result to the same user window without granting silent provider-to-provider access.

### Claim family D — Adaptive host continuity
A method in which a logical user window is mapped to different host surfaces according to runtime-discovered capabilities, including web, detached window, split surface, native overlay, compact/PiP, external display or spatial surface, while preserving the authorized session/window identity and timeline continuity.

### Claim family E — Verified learning
A system that uses verified post-action outcomes as learning/improvement signals, distinguishing claimed completion from observed completion and preventing an unverified action from being treated as a successful training signal.

## 5. Dependent-claim dimensions to investigate

- per-user identity and authorization scope;
- per-session and per-device identifiers;
- minimum-necessary context;
- privacy redaction/hashing;
- provenance and evidence source;
- explicit permission states;
- capability lifecycle;
- cross-device handoff;
- multi-display;
- accessibility tree context;
- screenshot/visual context;
- selected text/DOM context;
- active application context;
- external intelligence arbitration;
- disagreement preservation;
- safe-action classes;
- post-action state comparison;
- replayable/redacted audit events;
- pause/stop/kill control;
- user-controlled observation boundaries;
- host fallback when a capability is unavailable;
- future platform adapters.

## 6. Novelty / prior-art risk map

The following are high-priority references for attorney review, not conclusions of invalidity:

1. US10560761B2 — cross-device assistant handoff/context continuity. It overlaps with assistant continuity across computing platforms.
2. US20250356857A1 — cross-device application control using AI, contextual information and authorized execution. It overlaps with cross-device AI action and context routing.
3. US20250199829A1 / WO2025128247A1 — screen understanding and AI assistance based on foreground/background windows and screenshots. It overlaps with context-aware screen assistance.
4. US20250165264A1 — digital assistant interaction window associated with a web page/plugin and user authorization. It overlaps with contextual assistant windows.
5. US20240385860A1 — interactive window for a digital assistant with page-associated plugins. It overlaps with assistant interaction windows.
6. US20260351254 — extensible conversational agent with application, device, user and cross-device context. It overlaps with multi-context agent architecture.
7. US20260188475 — cross-session memory and multiple AI agents. It overlaps with persistent user memory and multi-agent access.
8. US2024213064A1 — interaction window associated with multiple components and drag/insertion behavior. It overlaps with interactive assistant/window UX.
9. Existing open-source overlay systems demonstrate that movable/topmost/click-through AI overlays are independently implementable and therefore should not be the sole novelty thesis.

The strongest candidate distinction is therefore NOT “an AI floating window.” The protection strategy should focus on the combined technical mechanism: persistent user-scoped window identity + capability negotiation + explicit authorization + provider-neutral intelligence federation + authorized action + post-action verification + chronological user-scoped evidence chain + adaptive host continuity + verified learning.

## 7. Prior-art search tasks for counsel

Search patent databases and non-patent literature for combinations of:
- persistent interactive intelligence window;
- personal AI window with host continuity;
- AI overlay action verification;
- user-scoped action/event timeline;
- AI agent post-action verification;
- provider-neutral multi-agent orchestration with authorization;
- cross-device persistent agent window;
- capability negotiation for AI UI surfaces;
- verified outcome as learning signal;
- privacy-preserving agent audit timeline.

For each reference record: publication number, priority date, applicant, relevant claims, overlapping element, differentiating element, jurisdiction/status.

## 8. Product embodiments

1. Web floating window.
2. Detached browser window.
3. Android split/PiP/native overlay where permitted.
4. Windows topmost/resizable/multi-monitor host where permitted.
5. iPadOS/macOS supported window/extension surfaces.
6. External display.
7. AR/VR/spatial surface.
8. Accessibility-first surface.
9. Game/software assistance through supported APIs/accessibility/authorized visual context only.
10. Cross-device handoff.
11. Multiple authorized intelligences behind IMA.
12. Offline/local intelligence adapter.
13. Future host/device adapter without changing the canonical contract.

## 9. Security and agency limitations

No bypass of OS permissions, application security, authentication, DRM or anti-cheat. No silent sharing between providers. No autonomous external action outside explicit user authorization. The system must distinguish requested, attempted, completed and verified states.

## 10. Evidence package

Maintain:
- Git commit chronology;
- signed/dated invention disclosure;
- architecture documents;
- runtime screenshots/videos;
- test logs;
- per-user timeline examples using synthetic/test accounts;
- capability manifests;
- prior-art matrix;
- claims chart;
- inventor contribution log;
- commercialization/contact log;
- disclosure/publication log.

## 11. Filing strategy for counsel

Evaluate:
A. first national filing in Israel;
B. first U.S. filing if strategically preferable;
C. priority-claiming PCT within the applicable 12-month priority period;
D. later national-phase decisions based on market and search results.

Do not publicly disclose enabling technical details before the first filing unless counsel confirms the disclosure is safe.

## 12. Commercialization

Potential revenue channels:
- licensing;
- OEM/OS partnerships;
- AI-provider integrations;
- accessibility partnerships;
- enterprise deployments;
- paid pilots;
- SDK/API licensing;
- patent-backed investment;
- acquisition.

Patent rights alone do not create revenue. Commercial value requires enforceable claims, market demand and counterparties.

## 13. Impact / Nobel-level research target

The long-term scientific/social objective is a universal human-agency layer: technology that increases a person's ability to understand, create, decide and act across languages, devices, applications and intelligence providers while preserving human agency, privacy and verifiable evidence.

The measurable research program should test:
- accessibility outcomes;
- learning outcomes;
- task completion;
- error reduction;
- time saved;
- user autonomy;
- cross-language performance;
- cross-device continuity;
- verification accuracy;
- false-completion rate;
- privacy leakage;
- dependence versus capability gain.

No Nobel claim is made. The objective is independently measurable global impact.

## 14. Current implementation truth

Implemented now:
- canonical LIVE-001 web window;
- movable/resizable/minimized/split/fullscreen/detached modes;
- persistent browser-session identity;
- authenticated user-scoped timeline retrieval;
- privacy-preserving timeline recording;
- authenticated client endpoint for window lifecycle events;
- provider-neutral intelligence architecture;
- host capability manifest;
- invention disclosure.

Not yet universally implemented:
- native above-all-app surfaces on every OS;
- every current/future intelligence connection;
- every device adapter;
- patent filing/grant;
- independent patentability opinion.

## 15. Immediate next actions

1. Obtain professional patentability/prior-art review.
2. File the first application before further enabling public disclosure if counsel recommends.
3. Capture runtime evidence for the web implementation.
4. Build the first native host adapter with the same contract.
5. Expand the timeline UI to show request → authorization → action → result → verification.
6. Add capability negotiation and authorization UI.
7. Continue scanning current and future intelligence providers and connect only when authorized and runtime-verified.
8. Begin licensing/partnership conversations after the protection strategy is secured.

Status: ACTIVE DEVELOPMENT / IP PREPARATION.
