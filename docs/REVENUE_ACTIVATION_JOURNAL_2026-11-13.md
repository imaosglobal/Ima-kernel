# Revenue Activation Journal — 2026-11-13

## Request
Activate the lowest-friction IMA revenue route while protecting Ori Cohen's disability-related rights and avoiding false business representation.

## Actions completed
- Added canonical payment configuration at `ima-ui/public/payment-config.json`.
- Added rights guard at `governance/IMA_INCOME_RIGHTS_GUARD_2026-11-13.md`.
- Updated `ima-ui/public/funding.html` with a personal Bit support route that is disabled until a verified destination exists.
- Updated the canonical public IMA app so its "Support IMA" CTA goes to the rights-safe funding page.
- Kept Google Pay out of the personal receiving path because it is a payment method, not a standalone receiving account.
- Kept business processors deferred.

## Rights evidence
- National Insurance states that income not from work can affect a general disability benefit depending on the benefit amount and that income changes should be reported.
- Therefore the product does not promise that Bit receipts are harmless to benefits.

## Current blocker
The Bit destination is intentionally blank and `enabled=false`. A personal payment URL cannot be safely invented or inferred.

## Activation condition
After Ori provides his verified personal Bit receiving URL, update only `ima-ui/public/payment-config.json`, verify the exact destination, then run the canonical QA/deployment/runtime verification loop.

## Claim status
Implemented: yes.
Payment destination activated: no.
Money received: no evidence.
Disability-rights outcome: not claimed or guaranteed.
