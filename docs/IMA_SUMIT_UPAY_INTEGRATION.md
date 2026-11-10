# IMA SUMIT/Upay integration contract

## Current state
- SUMIT/Upay is the canonical payment path under evaluation.
- No payment credentials are stored in Git.
- No live payment link is hard-coded until the user supplies the verified SUMIT payment endpoint.
- No revenue is counted from a pending, failed, or merely-created payment.

## Intended flow
1. IMA creates a payment request through SUMIT's supported payment-link/redirect flow.
2. Customer completes payment on the SUMIT/Upay-hosted payment page.
3. SUMIT sends a success notification to the configured IMA endpoint.
4. IMA records the transaction as verified revenue only after provider confirmation.
5. The revenue-first budget gate may then use the verified amount as an attributable reserve.
6. Paid AI remains blocked when verified revenue is zero and no explicit budget exists.

## API safety
SUMIT documents API keys as a public identifier plus a private authentication key. The private key is shown only when first generated and must not be committed to the repository. Webhooks are HTTP requests configured in SUMIT and can be used to notify an external service about relevant card records.

## Next manual step
In the real SUMIT account:
- enable the required payment/Upay module;
- generate an API key only if the selected integration requires it;
- create/configure the payment link or redirect;
- configure the webhook/IPN endpoint when the production endpoint is available;
- send the resulting non-secret endpoint/configuration to the IMA integration layer.

## Cost guard
Do not upgrade a paid SUMIT plan or activate a paid module solely to test this integration without explicit user authorization. The initial target remains zero fixed cost before the first real revenue.
