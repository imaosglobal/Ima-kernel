# Chrome Web Store listing — IMA Browser Bridge

**Short description**

Secure, user-controlled browser bridge for IMA.

**Detailed description**

IMA Browser Bridge connects a user's active Chrome tab to IMA without exporting passwords or browser cookies. The extension can read the visible content of the current tab after a user-initiated action and, when configured, send that result to an IMA HTTPS endpoint.

The first release intentionally does not automate financial transactions, destructive actions, permission changes, publishing, or other irreversible operations.

**Privacy**

- No password collection.
- No cookie export.
- No browsing-history database.
- Page content is only read after a user action.
- Optional outbound transmission is disabled until the user configures an HTTPS endpoint.
- Data sent to an IMA endpoint is limited to the page URL, title, visible text (up to 20,000 characters), and timestamp.

**Permissions justification**

- activeTab: access the current tab after a user action.
- scripting: read visible page content in the current tab.
- storage: store user-selected bridge settings locally.
- tabs: identify the current tab and open explicit HTTP(S) links.

**Support**

https://github.com/imaosglobal/Ima-kernel/blob/main/ima-chrome-extension/PRIVACY_POLICY.md
