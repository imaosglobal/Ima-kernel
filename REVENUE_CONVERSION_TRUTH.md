# IMA — Revenue Conversion Truth Contract

Updated: 2026-10-30

## Rule

A Google Ads conversion must represent a real, attributable customer action. The static page `subscription-confirmation.html` is **not** proof of payment.

## Required chain

`ad → landing → meaningful action → real checkout → verified payment → conversion value`

## Current state

- Google Ads account: `477-713-2721`
- Campaign: `IMA — בינה אנושית לכולם`
- Campaign ID: `24409551537`
- Authorized experiment ceiling: **100 ILS total**
- Current verified campaign delivery data: 0 impressions, 0 clicks, 0 spend, 0 conversions, 0 conversion value.
- Current primary status observed: `PENDING`.
- No verified payment provider/checkout flow is present in the repository search.
- Therefore no revenue conversion should currently be declared as paid revenue.

## Implementation gate

Do not optimize Google Ads for subscription value until a real payment provider is connected and its successful payment event can redirect to the confirmation page or otherwise send a verified conversion event.

Do not assign monetary value to page views, Google sign-ins, chat opens, or visits unless a business rule explicitly defines them as non-revenue conversions.

## Economics

Track at minimum:

- verified ad spend
- verified paid transactions
- verified revenue
- directly attributable payment/platform costs
- net return
- ROAS = verified conversion value / verified ad spend

Scale only after verified positive economics. Never increase the authorized 100 ILS ceiling without fresh explicit authorization.

## Operating loop

Measure → identify → improve → test → verify → stop waste → strengthen what works → measure again.

The same evidence standard applies to IMA's product, UX, content, YouTube, marketing, sales, partnerships and future capabilities.
