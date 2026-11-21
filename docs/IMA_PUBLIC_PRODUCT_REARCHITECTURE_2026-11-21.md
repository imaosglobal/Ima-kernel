# IMA Public Product Re-Architecture — 2026-11-21

## Goal
The public homepage is the market entry point, not a control room and not a documentation dump. Its job is to make a new visitor understand IMA in seconds and start one real interaction.

## What is removed from the entry page
- Emergency/resilience controls.
- Technical LIVE-001 / connector control room.
- Internal capability status panels.
- Long feature inventories.
- Nonessential campaign/shop material.
- Anything that requires the visitor to understand IMA's internal architecture before using it.

Emergency and resilience behavior remains a product capability that IMA can surface inside chat when the conversation indicates a need.

## Canonical homepage
1. Identity: IMA — אמא.
2. One promise: human-centered intelligence that starts from a real task.
3. One primary action: Talk to IMA.
4. One secondary action: How it works.
5. Four task entry points: Think, Learn, Create, Solve.
6. Three short trust/behavior statements.
7. Feedback.
8. Minimal legal/support footer.

## Visual direction
- Calm, premium, human visual identity rather than a generic AI dashboard.
- Strong typography and generous whitespace.
- One recognizable IMA visual anchor.
- Clear hierarchy: one headline, one primary CTA, one visual.
- Mobile-first layout with no overlapping content.
- Respect reduced-motion and keyboard focus.
- No hidden meaning in buttons; labels describe the action.

## Market lessons applied
Current market leaders succeed by reducing the time from arrival to useful action, emphasizing a clear primary job, and making differentiated strengths legible. AI discovery also increasingly rewards fast, crawlable, useful pages with strong page experience and consistent facts. IMA therefore uses a single primary CTA, task-oriented entry points, accessible content, stable structured metadata and measurable campaign attribution.

## Google Ads
Canonical landing URL:
https://imaosglobal.github.io/Ima-kernel/?utm_source=google&utm_medium=cpc&utm_campaign=ima_initial_100ils&campaignId=24409551537

The site now preserves the campaign identifier in the public entry URL and records the visit through the canonical market analytics path.

The connected ChatGPT Ads Manager currently reports no accessible ad accounts, so the external Google Ads account/campaign cannot be independently verified or edited from this environment. This is an external account-access blocker, not a reason to invent a campaign status.

## Quality gates
- Build must pass.
- Source contract must pass.
- Google Identity Services mount must be unique.
- Campaign URL must contain campaign ID and UTM source.
- Emergency/resilience and technical control-room surfaces must not render on the public entry page.
- Responsive browser smoke must pass at 390, 768 and 1280px.
- Main sections must not overlap.
- Public static pages must return success.
- Chat-only route must retain the Google gate.
- LIVE-001 canonical contract must remain green.