# IMA Master Requirements & Continuity Ledger

## Purpose

This is the canonical reconciliation point for IMA requirements gathered from the project's historical direction and subsequent development cycles. It is not a second backlog or scheduler. The single IMA Global Health Loop reconciles new requests against this ledger, existing issues, workflows, product code, tests and deployment state.

## Non-negotiable operating rule

Every new IMA request is:
1. timestamped;
2. matched against an existing requirement or given a stable new requirement ID;
3. connected to the existing canonical implementation rather than creating a duplicate;
4. traced through implementation, test, deployment and live verification;
5. synchronized back into the shared ledger;
6. carried forward until verified or explicitly closed.

A request is never considered complete merely because documentation exists.

## Historical product direction

- IMA is one global human-centered intelligence identity with many interfaces.
- IMA began from the creator's vision of a game-like operating system: interactive, playful, visual, learnable and usable across devices.
- The long-term target is seamless continuity across web, mobile, computers, consoles, XR/VR, robots, vehicles, drones and future interfaces where technically and legally possible.
- Personalization may change presentation, language, accessibility and permitted private memory, but not canonical IMA identity.
- Conversations, learning, tools, games, creation and device capabilities should feel like one coherent system rather than disconnected products.
- Cross-device continuity must preserve authorized user state and must never expose private memory to shared learning without authorization.
- Learning must be evidence-led: unknown -> research -> test -> verify -> teach -> regression.
- IMA must distinguish implemented, tested, deployed and verified-live capabilities.
- Safety, privacy, consent, accessibility, provenance and human agency are release gates.
- Website and app must share the same canonical identity, design language, capabilities and release truth.
- UI must be tested beyond source-code correctness: links, buttons, keyboard/touch interaction, responsive layout, text wrapping, loading/error states, accessibility, motion, media assets, chat, authentication and device-specific behavior.
- Authentication must remain a persistent product capability, not disappear because a release changes the UI.
- Google authentication must use Google's supported identity flows, server-side token verification and one user identity across supported web/mobile surfaces.
- Android Google sign-in should use Credential Manager rather than the deprecated legacy Android Google Sign-In API.
- Trend-to-Brand must validate the real operating environment, real user problem, integration, safety/compliance, economics and future scale before recommending production.
- Universal Conversation & Interaction Memory is canonical, consent-gated, chronological, provenance-aware and user-controlled.
- Public learning and private memory remain separate.
- Distribution should expand systematically through legitimate channels and partnerships, never through spam, impersonation, unauthorized publication or fabricated traction.
- Global user metrics must use real instrumentation and never treat missing analytics as zero users.
- The daily operating loop remains the single cross-domain orchestrator; historical job names are aliases or retired paths, not additional daily systems.


### CREATIVE-001 — Creative Bridge / Gap-to-Structure Engine
Status: IMPLEMENTED_IN_CODE / TESTED_PENDING_LIVE
- IMA can model a meaningful gap between domains as a hypothesis, connect it, test it and verify it with evidence.
- Unverified bridges remain hypotheses and are never promoted to established capability without evidence.
- Canonical loop includes a creative-bridge test task and records diagnostics for each run.
- Runtime/CI verification remains required before marking live.

### DIAG-001 — Canonical Loop Findings & Diagnosis
Status: IMPLEMENTED_IN_CODE / TESTED_PENDING_LIVE
- Every canonical loop cycle records pass/fail/error findings and a next diagnostic action.
- Failures instruct the system to inspect actual logs before changing code.
- Diagnostics are evidence about a run, not proof of deployment or live capability.

### FORESIGHT-001 — Continuous Long-Horizon Foresight & Present Preparation
Status: IMPLEMENTED_IN_CODE / TESTED_PENDING_LIVE
- IMA models plausible futures for each meaningful subsystem across NOW, 90-day, one-year, multi-year and long horizons.
- Futures are hypotheses, not predictions.
- Each trajectory records signals, prerequisites and safe present actions.
- The canonical loop evaluates these trajectories continuously and may prepare IMA now for capabilities that become plausible later.
- No future assumption is treated as runtime proof.

## Current priority gates

### AUTH-001 — Persistent Google authentication
Status: IMPLEMENTED_IN_CODE / RUNTIME_CONFIGURATION_GAP
- Web: Google Identity Services button.
- Backend: Google ID-token verification and signed IMA session.
- Android: Credential Manager bridge to the same backend identity.
- Required external configuration: a real Google Web OAuth client ID with the public web origin authorized, then GOOGLE_CLIENT_ID on the canonical Render service.
- Verification required: real browser login, session persistence, logout, chat authorization, Android login, cross-device identity continuity.

### UX-001 — Continuous interface verification
Status: IN_PROGRESS
- Source-level visual contracts added.
- Daily QA expanded.
- Browser-level interaction matrix still requires real browser execution for every interactive control.

### DEVICE-001 — One identity across devices
Status: IN_PROGRESS
- Web session, Android bridge and device continuity exist in separate layers.
- They must converge on the same canonical identity/session and capability registry.
- Future device adapters must reuse this identity contract rather than inventing parallel accounts.

### PRODUCT-001 — Game-like IMA OS
Status: IN_PROGRESS
- 3D presence, modes, chat, device continuity and native Android shell exist.
- Future engines and interfaces must be capability adapters under the same identity and learning loop.


### PRES-001 — Intergenerational memory & historical preservation
Status: IMPLEMENTED_IN_DOCUMENTATION / RUNTIME_INTEGRATION_REQUIRED
- Preserve human names, lives, oral histories, languages, art, science, philosophy and cultural memory across generations.
- Distinguish primary evidence, textual tradition, historical interpretation, cultural memory, myth/theology, hypothesis and unknown.
- Preserve provenance, source variants, uncertainty, translations, transformations, hashes where appropriate, and original/derivative relationships.
- Never silently replace an original with an AI-generated translation, summary, restoration or interpretation.
- Preserve ordinary lives as well as rulers and famous figures.
- Historical teaching must retain both the value of cultural memory and the limits of the evidence; ancient or repeated claims are not automatically facts.
- Use the Sumerian King List as a canonical example of layered memory: historical place/person traditions intertwined with mythic, theological, ideological and numerical traditions.
- Corrections extend provenance rather than erase the record of prior belief.
- Private personal stories remain private unless explicitly authorized for broader preservation.
- Runtime capability requires the existing PLANNED -> IMPLEMENTED -> TESTED -> DEPLOYED -> VERIFIED_LIVE gates.
- Canonical specification: [IMA Intergenerational Memory & Historical Preservation Charter](IMA_INTERGENERATIONAL_MEMORY_AND_HISTORICAL_PRESERVATION_CHARTER.md).

### DIST-001 — Lawful Global Distribution
Status: IMPLEMENTED_IN_CODE / TESTED_PENDING_LIVE
- Public Culture of the Heart page is published in the repository and linked from the public entry point.
- The unified loop prepares a provenance-bearing distribution queue.
- External social/press/community posting remains gated by authorized accounts/connections and platform/legal rules; no claim of autonomous universal posting is made.
- Non-spam, no impersonation, no manipulation and attribution rules are explicit.

### LOOP-001 — Single Canonical IMA Loop
Status: IMPLEMENTED_IN_CODE / TESTED_PENDING_LIVE
- Runtime identity context is injected into IMA behavior: one global IMA identity, an uncertain/updateable world model, and isolated user context by default.
- All periodic IMA maintenance, learning, reflection, preservation, culture, web intelligence, evolution, QA and lawful distribution preparation must reconcile through `.ima/loop/unified_loop.py`.
- The single scheduler is `.github/workflows/ima-unified-loop.yml`, hourly in Asia/Jerusalem.
- Event-driven CI may remain for immediate push/PR verification; it is not a second periodic loop.
- Every explicitly authorized request to add something to “the loop” belongs in this canonical contract.
- Private conversations are not automatically imported into IMA. Cross-conversation learning requires an explicit authorized ingestion path.
- Runtime behavior remains subject to TESTED → DEPLOYED → VERIFIED_LIVE evidence.

### CULT-001 — Human Culture / Culture of the Heart
Status: IMPLEMENTED_IN_CODE / TESTED_PENDING_LIVE
- Build a shared global cultural layer without replacing, erasing or ranking existing cultures.
- Preserve languages, numerical traditions, calendars, histories, heroes, ordinary lives, music, dance, architecture, food, craft, education, governance, economic experiments, stories, myths, science and future cultural forms.
- Record Ori Cohen as initiator/founder of the project only; founder status never grants permanent authority or ownership of the culture.
- Keep human agency primary: no coercive membership, permanent ruler, sacred political authority or personality cult.
- IMA is infrastructure for memory, learning, translation, connection and reflection, not the sovereign of the culture.
- Executable cultural policy lives in `core/human_culture.py` and is injected into the provider-neutral LLM prompt through `core/human_intelligence.py`.
- Regression coverage lives in `tests/test_human_culture.py`; continuous health and the daily learning review execute it.
- Live runtime behavior still requires deployment verification on the canonical production surface.
- Canonical charter: [IMA Human Culture Charter](IMA_HUMAN_CULTURE_CHARTER.md).
- Daily refinement follows the single Global Health Loop; it must not create a second scheduler: [IMA Human Culture Daily Loop](IMA_HUMAN_CULTURE_DAILY_LOOP.md).
- Runtime capability requires PLANNED -> IMPLEMENTED -> TESTED -> DEPLOYED -> VERIFIED_LIVE.

### HISTORY-001 — Historical request reconciliation
Status: ACTIVE
- This ledger is the canonical reconciliation anchor.
- Each future cycle must reconcile historical requests before adding new architecture.
- Duplicate implementations must be merged, retired or explicitly justified.

## Verification vocabulary

PLANNED -> IMPLEMENTED -> TESTED -> DEPLOYED -> VERIFIED_LIVE

Never skip a state in reporting. A failed or blocked state records evidence and the next action instead of being silently marked complete.


### GROWTH-001 — Real Global User Growth & Retention
Status: IMPLEMENTED_IN_CODE / RUNTIME_CONFIGURATION_REQUIRED
- Growth is now a first-class domain of the single unified loop.
- IMA measures real visits, starts, authenticated users, returning users, feedback, retention and voluntary sharing only through instrumented or independently verified sources.
- Missing analytics remain UNKNOWN rather than zero.
- Public feedback endpoint exists; project learning from feedback remains governance-gated.
- App-store ratings/reviews are never fabricated and are counted only from verified store evidence.
- Growth work must improve usefulness, accessibility, localization, discoverability, onboarding and retention—not vanity metrics.
- Daily/monthly/yearly/decadal continuity is reconciled by the same canonical scheduler.
- External distribution remains lawful, non-spam, consent-respecting and authorized.
- Canonical specifications: `docs/IMA_GLOBAL_GROWTH_AND_USER_TRUTH.md`, `docs/IMA_USER_FEEDBACK_AND_REPUTATION.md`.
\n### ULE-001 — Universal Learning, Capability Discovery & Self-Application\nStatus: IMPLEMENTED_IN_CODE / TESTED_PENDING_LIVE\n- IMA treats every human knowledge domain and every newly accessible capability as a candidate for discovery, evidence, testing, verification, teaching and bounded self-application.\n- Domains preserve people, works, sources, methods, disputes, uncertainty and interdisciplinary connections without flattening distinct disciplines.\n- Emerging domains remain PROPOSAL until evidence and human review justify promotion.\n- Capabilities use PLANNED -> DISCOVERED -> CONNECTED -> TESTED -> DEPLOYED -> VERIFIED_LIVE.\n- Every verified capability has a USE path for authorized IMA work and a TEACH path for people; self-application uses the same release gates.\n- Provider independence is mandatory: record alternatives, cost class, license, privacy review and unresolved gaps.\n- This requirement is executed by the existing single canonical loop; no second periodic scheduler is permitted.\n- Canonical implementation: core/universal_learning_engine.py, core/capability_substitution.py, docs/IMA_UNIVERSAL_LEARNING_ENGINE.md.\n\n### SELF-001 — Verified Capability Self-Application\nStatus: IMPLEMENTED_IN_CODE / TESTED_PENDING_LIVE\n- A capability learned by IMA can be evaluated for bounded use on IMA itself after VERIFIED_LIVE status.\n- Self-application follows INSPECT -> PLAN -> CHANGE -> TEST -> VERIFY -> CARRY_FORWARD and cannot bypass normal deployment or safety gates.\n- Examples include improving site architecture, embedded chat, commerce, education, accessibility and other verified technical capabilities.\n- Canonical implementation: core/capability_self_application.py and docs/IMA_SELF_APPLICATION_PROTOCOL.md.\n

### PROV-001 — From Imagination to Verifiable Capability / First-Priority Provenance
Status: DOCUMENTED / RUNTIME_INTEGRATION_REQUIRED
- Recorded on 2026-10-18 at the explicit request of Ori Cohen.
- IMA records Ori Cohen as the first recorded initiator of this specific IMA formulation: human imagination -> technological possibility -> verified capability -> responsible human use -> intergenerational continuity.
- The record applies to IMA's global layer and benefits all users subject to privacy, consent, safety and evidence rules.
- IMA must preserve prior art and independent precedent and must not convert this provenance record into an unsupported legal monopoly claim.
- Capability history must distinguish imagined, proposed, implemented, tested, deployed and verified-live states.
- Canonical specification: `docs/IMA_FIRST_PRIORITY_PROVENANCE.md`.


### FIN-001 — Finance, Nonprofit Governance, Creator Succession & Monetization Evidence
Status: IMPLEMENTED_IN_CODE / TESTED_PENDING_LIVE
- The single canonical Global Health Loop now runs an evidence-only monetization readiness audit.
- The audit covers creator-to-commerce readiness, actual-revenue truth, finance/nonprofit separation, creator compensation/royalty separation, and the no-autonomous-spending gate.
- Actual revenue is never inferred from views, followers, eligibility, estimates or projections.
- No payment, donation, transfer, subscription, advertising spend, sponsorship commitment or purchase is executed by the loop.
- The canonical surplus order remains: refunds/chargebacks/required taxes -> verified transaction/platform fees -> authorized operating expenses -> documented creator compensation/license royalty -> required reserve -> nonprofit mission reinvestment -> authorized humanitarian/community benefit.
- IMA's nonprofit status remains unregistered unless independently verified legal evidence exists.
- Creator provenance remains permanently attributed to Ori Cohen / creator_001; heirs are never inferred.
- Live monetization still requires external account eligibility, enrollment, payout permissions and platform evidence. Documentation and source code do not prove that money can currently be received.
- Verification command: `python scripts/ima_monetization_readiness.py`.


### FIN-002 — PayPal as Primary Payment Provider
Status: IMPLEMENTED_PENDING_HUMAN_ACCOUNT_ACTIVATION
- Stripe is no longer the canonical payment-provider route for IMA.
- PayPal is the primary global online payment route, subject to country/account/product eligibility.
- Israel is supported by PayPal's official business/payment services.
- Live account verification, bank linkage, compliance approval and payout evidence remain human-controlled external prerequisites.
- No credentials are stored in the repository and no autonomous transaction is permitted.


### FIN-003 — Multi-Provider Payment Router
Status: IMPLEMENTED_PENDING_LIVE_PROVIDER_ACTIVATION
- IMA no longer treats one payment provider as a permanent dependency.
- The canonical routing model supports PayPal, Google Pay, Apple Pay, GitHub Sponsors, YouTube, Open Collective and future provider adapters.
- Google Pay is modeled as a wallet layer that requires a supported payment processor/gateway; it is not itself the settlement provider.
- When multiple verified providers are available, the checkout may expose a user/provider choice subject to country, currency, product, device, compliance and provider availability.
- A new provider can be added as an adapter without changing the financial ledger or Unified Global Health Loop.
- Actual revenue remains evidence-only: no account, button, Merchant ID, eligibility or estimate is treated as revenue.
- No autonomous transaction, transfer, purchase, donation, subscription, sponsorship or payout is permitted.
- No payment credentials are stored in the repository.
- Canonical implementation specification: `docs/IMA_PAYMENT_PROVIDER_STANDARD.md`.
