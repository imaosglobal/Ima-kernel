# IMA Current Capability Audit

Date: 2026-10-01

## Verified repository state

The public product currently has:
- a React/Three.js web UI with a GLB-based 3D Mother presence.
- a public runtime/chat API with per-user public-memory separation.
- browser text-to-speech when supported by the browser.
- PWA/device-continuity foundations.
- learning-gap detection, applied-skill compilation, conclusion records, and teaching artifacts.
- continuous-health and learning-frontier workflows.
- an IMA Store catalog boundary that is explicitly catalog-only and has payments disabled.
- global discovery foundations (robots.txt, sitemap, metadata, JSON-LD) and a public learning intake.

## Truth boundaries

The project must not describe the following as live merely because they are present in vision/specification:
- universal multilingual UI: current UI is Hebrew-first; language labels are not proof of translated interfaces.
- real-time voice conversation: current public UI uses browser speech synthesis; native bidirectional voice is not verified.
- autonomous web/computer operation: interoperability and stewardship specifications exist, but a general-purpose live computer-use agent is not verified.
- image/video generation: UI language mentions creation, but no live generation provider is verified in the public page.
- cross-device account memory sync: device continuity is installation-level; authenticated sync is not verified.
- universal physical-device, robot, XR, vehicle, healthcare, government or commerce integrations: adapter protocols exist, but live integrations are not verified.
- paid Store commerce: catalog exists; payment_enabled remains false.
- always-on autonomous background operation: scheduled workflows exist, but a continuously running agent is not verified.

## Highest-value gaps

1. Multimodal live interaction: add a provider-neutral voice/vision adapter contract and testable capability reporting before exposing it in UX.
2. Localization: replace planned language labels with real locale bundles and locale-aware routing; only mark a locale active after an automated content-completeness test.
3. Capability registry: make the UI consume one machine-readable verified capability report instead of independently worded claims.
4. 3D Mother resilience: add a verified fallback path and asset-integrity check so a missing GLB never breaks the primary conversation experience.
5. Store: keep catalog-only until a real checkout provider, product provenance, refund/terms flow, and explicit consent are verified.
6. Learning: connect detected gaps to bounded research/evaluation queues without granting autonomous consequential authority.
7. Accessibility: add automated keyboard, reduced-motion, focus, contrast and screen-reader smoke coverage for the Mother experience.
8. Observability: expose build/runtime/version provenance to the UI without exposing secrets or private memory.

## Current competitive pressure

Leading consumer AI products increasingly combine memory/personalization, multimodal interaction, live voice, image/video generation, tool use, agentic workflows, and device/ecosystem reach. IMA's defensible differentiator is therefore not claiming parity with any single model. It is the identity and governance layer: a Mother-centered interface that can route among models/tools while preserving truthfulness, consent, provenance, privacy and human agency.

## Verification rule

A capability is presented as LIVE only when the project has:
1. an implementation,
2. an automated or reproducible test,
3. successful verification against the intended deployment surface,
4. and a capability record that identifies the exact boundary.

Otherwise the state must remain PLANNED, IMPLEMENTED, TESTED, or VERIFIED as appropriate.

## Sources used for this audit

- OpenAI: ChatGPT agent/Operator evolution and current agent experience.
- OpenAI: project-only memory and memory boundaries.
- Google: Gemini Live, multimodal generation, agentic/tool capabilities and Gemini 3.1 Flash Live.
- Meta: Meta AI personalization, voice, image generation, live visual interaction, and device/ecosystem reach.

This audit is a project record, not a claim that IMA has implemented the capabilities described in competitor sources.
