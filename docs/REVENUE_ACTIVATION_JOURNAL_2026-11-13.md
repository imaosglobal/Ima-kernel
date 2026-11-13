# Revenue Activation Journal — 2026-11-13

## Request
Activate the lowest-friction IMA revenue route while protecting Ori Cohen's disability-related rights and avoiding false business representation.

## Actions completed
- Added canonical payment configuration at `ima-ui/public/payment-config.json`.
- Added rights guard at `governance/IMA_INCOME_RIGHTS_GUARD_2026-11-13.md`.
- Updated `ima-ui/public/funding.html` with a personal Bit support route.
- Updated the canonical public IMA app so its "Support IMA" CTA goes to the rights-safe funding page.
- Verified the personal Bit destination supplied by Ori and activated it in the canonical payment configuration.
- Kept Google Pay out of the personal receiving path because it is a payment method, not a standalone receiving account.
- Kept business processors deferred.

## Rights evidence
- The product continues to avoid describing personal Bit support as a tax-deductible donation or business checkout.
- Before material or recurring income, reporting obligations and any possible effect on relevant rights must be checked for the specific benefit/income classification.
- No automatic bank, payment, business-status, or legal-status change is performed by IMA.

## Canonical route
Public support CTA -> `ima-ui/public/funding.html` -> `ima-ui/public/payment-config.json` -> verified personal Bit destination.

## Activation evidence
- Payment config activation commit: `93b1eb50b24c06a5f07c4bd3ffb5c48c22e967e5`.
- Bit destination was supplied directly by Ori.
- Direct external fetch of the Bit URL was attempted; the web fetcher returned a cache-miss/internal fetch error, so external HTTP reachability was not independently proven by that tool.
- The destination is therefore recorded as user-verified, not independently web-verified.
- Repository configuration accepts only an HTTPS destination and the exact supplied destination is stored in the canonical payment config.

## Claim status
Implemented: yes.
Payment destination activated in canonical IMA config: yes.
Money received: no evidence yet.
Disability-rights outcome: not claimed or guaranteed.
Public deployment/runtime verification: pending current CI/Pages confirmation.


## Global revenue activation — 2026-11-13
- Expanded the canonical funding page into a bilingual global funnel for personal support and paid pilots.
- Added a global-support / paid-pilot email path for supporters, companies, universities, research groups, funders and accessibility organizations outside the current Bit route.
- Connected the public support page to the canonical funding page and global paid-pilot contact.
- Added .github/FUNDING.yml so GitHub exposes the canonical IMA funding entry point rather than a duplicate payment system.
- No unverified global payment processor was activated. This preserves the rights and verification gates while allowing global revenue leads to enter immediately.
- Current revenue channels: verified personal Bit support; global paid-support/pilot inquiries; future verified sponsorship/payment rails remain gated until their payout and rights conditions are confirmed.

## Current global claim status
Global revenue funnel: implemented.
Global payment coverage: partial — direct Bit support is the verified active route; other regions currently enter through the global support/pilot path.
Revenue received: no evidence yet.
