# IMA Nylas email integration

The IMA public runtime can read the connected IMA mailbox through Nylas.

## Runtime variables

Set these in Render as secrets/environment variables:

- `NYLAS_API_KEY` — Nylas Sandbox API key; never commit it.
- `NYLAS_GRANT_ID` — the Grant ID for `imaosglobal@gmail.com`.
- `NYLAS_MAILBOX` — `imaosglobal@gmail.com`.
- `NYLAS_ENVIRONMENT` — `sandbox`.
- `NYLAS_API_BASE_URL` — optional; defaults to `https://api.us.nylas.com/v3`.

The integration exposes:

- `GET /ima-api/email/status` — configuration status without mailbox contents.
- `GET /ima-api/email/messages` — recent messages, protected by the existing signed IMA session.

Nylas recommends webhooks for real-time message notifications rather than polling. The webhook endpoint is intentionally a separate follow-up because its generated webhook secret must be stored as a Render secret and its Nylas destination must be created from the Nylas account.
