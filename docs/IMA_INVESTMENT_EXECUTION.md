# IMA Investment Execution Mode

## Purpose
Extend the canonical IMA Opportunity Engine from investment research into a controlled path for actually purchasing and holding public-market securities, while preserving user agency and regulatory boundaries.

## Architecture
IMA is the decision and orchestration layer. A regulated brokerage/custodian remains the account holder and execution venue.

Flow:
1. IMA discovers and researches an opportunity.
2. IMA presents evidence, thesis, risks, fees, conflicts, and uncertainty.
3. User defines an investment mandate: account, permitted instruments, budget, risk limits, time horizon, and whether orders require per-trade confirmation.
4. A broker adapter exposes only the minimum required account/market/order capabilities.
5. IMA creates an order proposal, never an invisible order.
6. User explicitly authorizes the order unless a separately authorized discretionary mandate legally permits otherwise.
7. The broker executes the order and returns an authoritative execution result.
8. IMA records the proposal, authorization, broker response, holdings change, fees, and source evidence in an auditable journal.

## Operating modes

### 1. Research-only
No brokerage connection and no order capability.

### 2. Connected portfolio
Read-only account/positions/balance/transaction data where the provider supports it. IMA can monitor and analyze but cannot trade.

### 3. Confirm-before-trade
IMA may prepare an exact order:
- symbol/security identifier
- buy/sell
- quantity or notional amount
- order type
- limit/price constraints
- estimated fees
- estimated total
- reason/evidence
- risk checks

The order remains pending until the user explicitly authorizes that specific order.

### 4. Pre-authorized mandate
Only after a legally appropriate brokerage/advisory arrangement, explicit mandate, suitability/compliance controls, and provider support are in place may a broker adapter execute within predefined limits without per-order confirmation. This mode is disabled by default and must never be implied to exist merely because a brokerage API is connected.

## Hard controls
- Never fabricate execution, holdings, cash, prices, fills, or returns.
- Never store brokerage passwords or private keys in IMA.
- Prefer OAuth/tokenized broker connections and least-privilege scopes.
- No money transfers.
- No leverage, margin, options, short selling, or derivatives unless explicitly enabled by the user, supported by the provider, and separately risk-gated.
- Enforce per-order, daily, and portfolio exposure limits.
- Reject stale market data when an order requires current pricing.
- Show conflicts, fees, and uncertainty before authorization.
- Keep an immutable audit trail of proposed and executed actions.
- Provide a kill switch that disables order submission while leaving research/monitoring available.
- If the broker or market-data source is unavailable, fail closed: no order.

## Default IMA policy
The default mode is **Confirm-before-trade**. IMA may continuously discover opportunities and prepare proposals, but actual stock purchases require explicit user authorization unless a separately established and legally valid discretionary mandate says otherwise.

## Broker adapter contract
A future adapter should implement, as available:
- connect/auth status
- account summary
- positions
- balances
- market data
- order preview
- order submission
- order status
- cancel order
- transaction history

The adapter must identify the provider, account, permissions, data timestamp, and execution venue in every response.

## Audit record
Each investment action should record:
- opportunity ID
- security identifier
- evidence sources and timestamps
- thesis and counter-thesis
- user mandate/limits in force
- exact proposed order
- explicit authorization event
- broker/provider response
- fill(s), fees and timestamps
- resulting position
- errors/blockers/unknowns

## Separation of roles
IMA does not become the custodian of user assets. The brokerage account remains with the regulated provider. IMA's role is research, decision support, orchestration, and—only when properly authorized and supported—order routing.

## Safety and compliance gate
Before enabling live execution for any jurisdiction or user, the implementation must verify the applicable broker permissions, identity/KYC requirements, advisory/trading obligations, disclosures, tax/reporting requirements, and provider terms. A technical API connection alone is not sufficient.
