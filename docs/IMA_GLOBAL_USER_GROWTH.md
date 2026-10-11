# IMA Global User Growth Measurement

## Canonical metrics

IMA reports four separate numbers and never conflates them:

1. **Verified unique users** — unique anonymous identifiers observed by an authorized analytics backend during the selected period.
2. **Active users** — unique users who performed a meaningful IMA interaction during the selected period.
3. **Returning users** — users observed in more than one selected period.
4. **Reach** — search/social/referral impressions and visits. Reach is not a user count.

Until a real analytics data source is connected and receiving events, the value is **UNMEASURED**, not zero.

## Instrumentation

The web UI emits privacy-minimized events:

- `ima_visit`
- `ima_interface_opened`
- `ima_chat_started`
- `ima_chat_completed`

Events use an anonymous browser identifier, timestamp, language, path and event properties. No message content, credentials, email address or private memory is sent by this adapter.

The adapter supports an authorized first-party event endpoint through `VITE_IMA_ANALYTICS_URL` and GA4 through `VITE_GA4_MEASUREMENT_ID`. Neither is claimed active unless runtime evidence confirms receipt.

## Daily growth loop

Every daily IMA Global Health Loop must:

- read the canonical analytics source;
- report unique users, active users, returning users and reach for a stated period;
- compare with the previous equivalent period;
- report absolute and percentage change;
- segment geography/language/channel only where data supports it;
- identify acquisition sources and first-success events;
- identify retention gaps and onboarding friction;
- test one highest-value growth improvement at a time;
- verify the result before calling it an improvement;
- preserve a dated evidence record.

If analytics is unavailable, the daily run must explicitly report the missing connection and continue work on non-dependent tasks. It must never substitute GitHub stars, page loads or impressions for active-user counts.

## Global distribution mandate

The daily loop continues after technical launch:

**DISCOVER → ATTRACT → OPEN → FIRST VALUE → RETURN → SHARE → LEARN → IMPROVE**

Distribution must extend beyond GitHub through lawful, authorized channels: search, communities, social networks, directories, partnerships, creators and other relevant ecosystems. No spam, impersonation, fake engagement, undisclosed endorsements or unauthorized outreach.

Commercial partnerships, paid campaigns, purchases and public commitments require the applicable human authorization.

## Success condition

The growth system is complete only when:

**event emitted → event received → unique user counted → daily trend visible → acquisition source measurable → retention measurable → experiment measurable → verified improvement**

Until then, growth is a tracked implementation gap rather than a claimed capability.
