# IMA Browser Bridge

Manifest V3 Chrome extension for a user-controlled bridge between an authenticated browser session and IMA.

## Monetization model

The extension is intentionally free. It is an acquisition channel for IMA, not the payment boundary:

- Extension → IMA website with attributable referral traffic.
- IMA can offer paid services on the website when those services and checkout are actually available.
- No fabricated customers, revenue, conversions, partnerships or performance claims.
- No automatic financial transactions, payout changes, or purchases.
- Chrome Web Store publication remains a separate distribution decision.

Landing page: https://imaosglobal.github.io/Ima-kernel/browser-bridge.html

## Security boundaries

- Does not read, export, or transmit browser cookies.
- Does not read passwords.
- Uses activeTab + scripting so page access is user-initiated and scoped to the current tab.
- Only accepts HTTP(S) URLs for link opening.
- Financial, destructive, permission-changing, publishing, or irreversible actions are intentionally not automated by this first release.
- Optional outbound calls use a user-configured HTTPS endpoint and optional scoped bearer token.
- Page content is truncated to 20,000 characters before transmission.

## Install for local verification

1. Open chrome://extensions.
2. Enable Developer mode.
3. Choose Load unpacked.
4. Select this directory.
5. Open a normal HTTP(S) page and use the IMA Browser Bridge action.

## Distribution status

The code and landing page are public. Chrome requires a one-time developer registration fee before publishing items in the Chrome Web Store. IMA does not bypass Chrome's distribution rules. The monetization architecture therefore does not depend on paying that fee: the extension can be validated as a free acquisition product first, while a store listing can be added later if distribution economics justify it.

## Verification

The repository workflow validates the MV3 manifest, security boundaries and generated icons. A workflow pass is evidence of package validation, not evidence that a Chrome Web Store listing is published.