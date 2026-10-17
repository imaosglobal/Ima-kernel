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

### CULT-001 — Human Culture / Culture of the Heart
Status: IMPLEMENTED_IN_DOCUMENTATION / RUNTIME_INTEGRATION_REQUIRED
- Build a shared global cultural layer without replacing, erasing or ranking existing cultures.
- Preserve languages, numerical traditions, calendars, histories, heroes, ordinary lives, music, dance, architecture, food, craft, education, governance, economic experiments, stories, myths, science and future cultural forms.
- Record Ori Cohen as initiator/founder of the project only; founder status never grants permanent authority or ownership of the culture.
- Keep human agency primary: no coercive membership, permanent ruler, sacred political authority or personality cult.
- IMA is infrastructure for memory, learning, translation, connection and reflection, not the sovereign of the culture.
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
