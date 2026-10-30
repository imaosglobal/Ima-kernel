# IMA World-Model Evolution Policy

IMA should adopt verified advances in interactive world models as soon as lawful, safe and technically available, while preserving human agency, privacy, provenance and truthful capability status.

## Continuous upgrade rule

For each material provider/model release:
1. Detect the official release or availability signal.
2. Verify the official API/SDK, supported devices, regions, pricing/quotas and access requirements.
3. Compare capabilities with the current IMA world-model adapter.
4. Update the adapter and tests when an improvement is available.
5. Run bounded tests before public exposure.
6. Verify at least one real provider request before marking the capability VERIFIED_LIVE.
7. Preserve a rollback path when the provider supports incompatible changes.
8. Update capability metadata and the development journal with evidence.
9. Never claim access that is unavailable to the current deployment.
10. Prefer provider-neutral abstractions so IMA can use multiple verified world-model providers rather than becoming dependent on one.

## Device adaptation

The integration must adapt to the actual device and connection constraints:
- mobile-first and low-bandwidth operation;
- desktop/browser operation when available;
- accessibility alternatives for visual, audio and interaction limitations;
- progressive quality/resolution based on device capability and network conditions;
- server-side generation where local hardware cannot support the model;
- local/private processing when technically and legally appropriate;
- graceful fallback to text, images, video or ordinary IMA interaction when an interactive world model is unavailable.

Device adaptation must change presentation and resource use, not the safety, privacy, provenance or agency guarantees.

## IMA-native integration

World models should become one capability inside IMA, not a replacement for IMA:
- learning and education;
- safe scenario exploration;
- accessibility and rehabilitation-oriented simulations where clinically appropriate;
- creative worlds and storytelling;
- robotics and embodied-AI preparation;
- scientific visualization;
- cross-language and cross-cultural environments.

High-impact applications require appropriate real-world validation and human oversight.

## Monitoring

The canonical IMA loop should periodically inspect official provider availability and compatibility signals. It must record AVAILABLE, UPGRADE_AVAILABLE, ACCESS_REQUIRED, NOT_VERIFIED, or BLOCKED rather than silently assuming availability.

No autonomous purchase, subscription, contract, or external commitment is permitted.
