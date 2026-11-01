# IMA Browser Bridge

Manifest V3 Chrome extension for a user-controlled bridge between an authenticated browser session and IMA.

## Security boundaries

- Does not read, export, or transmit browser cookies.
- Does not read passwords.
- Uses `activeTab` + `scripting` so page access is user-initiated and scoped to the current tab.
- Only accepts HTTP(S) URLs for link opening.
- Financial, destructive, permission-changing, publishing, or irreversible actions are intentionally not automated by this first release.
- Optional outbound calls use a user-configured HTTPS endpoint and optional scoped bearer token.
- Page content is truncated to 20,000 characters before transmission.

## Install for local verification

1. Open `chrome://extensions`.
2. Enable Developer mode.
3. Choose **Load unpacked**.
4. Select this directory.
5. Open a normal HTTP(S) page and use the IMA Browser Bridge action.

## Status

This is the initial secure bridge foundation. Chrome Web Store publication requires the user's Google developer account and any required store verification/payment steps; those cannot be completed by IMA without the account owner performing Google's consent/verification steps.
