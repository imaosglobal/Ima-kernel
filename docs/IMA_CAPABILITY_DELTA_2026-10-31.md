# IMA Capability Delta — 2026-10-31

## Verified facts
- Supabase project `tenpzpvqvtezezaossjd` is `ACTIVE_HEALTHY` (checked 2026-10-31).
- Render service `ima-opportunity-mcp` is live at `https://ima-opportunity-mcp.onrender.com`; latest deployment completed successfully.
- Render logs confirm the intended command `cd apps/ima-opportunity-mcp && npm start` and the MCP server listening on the assigned port.
- GitHub combined status for commit `7914d3a1e8b6ddd101e9783119d6467fbb22bd4c` returned no status records; CI is therefore NOT VERIFIED.
- Gmail connector calls currently fail with HTTP 400; profile retrieval returned no data. This is a current connector/runtime signal, not evidence that Gmail data was deleted.
- Gmail search surfaced 21 IMA-related threads in the last two days before the connector error; this establishes that recent IMA email activity exists in the connected account context, but the current connector cannot presently be treated as reliably readable.
- OpenAI official documentation currently states that event-triggered tasks support Gmail, Slack and GitHub, but Free and Go accounts cannot create them. Scheduled recurring tasks remain available to Free users up to once daily.
- OpenAI's current public plugin documentation confirms that a plugin may contain MCP connections, skills, or both; public submission requires package upload, automated checks and review, and publication only after approval.

## Capability delta
No newly verified account-level event-trigger capability was found today. The account remains constrained to scheduled monitoring rather than webhook/event-triggered monitoring.

## MISSED-CAPABILITY-DETECTION
None newly established today. Continue distinguishing product availability, account eligibility, connected permission, runtime test and production verification.

## Risks
- Gmail connector: current HTTP 400 makes Gmail scanning partially unavailable in this run.
- Render npm output reports one high-severity dependency vulnerability. No automatic `npm audit fix --force` was applied because that could introduce breaking/unreviewed changes.
- Public MCP production status is verified at the hosting layer; public OpenAI directory publication remains a separate approval gate.

## Preventive loop changes
- Treat Gmail connector errors as an explicit health signal and do not interpret an empty/failed read as absence of email.
- Treat `statuses: []` as NOT VERIFIED rather than passing.
- Treat dependency audit warnings as review items requiring compatibility-aware remediation, not forced automatic upgrades.
- Preserve the four-state capability model: PRODUCT_AVAILABLE → ACCOUNT_ELIGIBLE → CONNECTED_AND_AUTHORIZED → RUNTIME_VERIFIED.
