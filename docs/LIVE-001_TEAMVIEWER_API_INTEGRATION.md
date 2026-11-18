# LIVE-001 TeamViewer API Integration

Status: **integration boundary implemented; credentials and TeamViewer transport licensing remain external prerequisites.**

IMA now exposes a canonical `ima_teamviewer` MCP tool and a server-side TeamViewer API adapter.

## What is implemented

- Server-side TeamViewer API client using a bearer token.
- `ima_teamviewer(status)` reports whether the server has TeamViewer credentials without exposing secrets.
- `ima_teamviewer(devices)` can query the TeamViewer device list once an authorized token is configured.
- `ima_teamviewer(session)` creates an official TeamViewer attended support session and returns the TeamViewer session payload.
- The result is explicitly marked **unverified** until the actual transport/control path is observed.
- No TeamViewer secret is accepted from chat or stored in browser code.

## What is not claimed

The normal TeamViewer web API is not itself a live screen-stream/control protocol. For Android remote control, TeamViewer documents separate Mobile SDK and REACH integration paths, with licensing and registration prerequisites. Therefore IMA must not claim that an API-created session gives ChatGPT direct Android screen/control access until the actual TeamViewer transport is integrated and runtime-verified.

## Required TeamViewer setup

TeamViewer's official integration documentation requires a TeamViewer account and an OAuth application with a client ID, client secret, redirect URI, and appropriate permissions. A script token can be used for initial API testing.

Configure the deployment environment, never the source repository:

- `TEAMVIEWER_ACCESS_TOKEN` — server-side secret
- optional `TEAMVIEWER_GROUP_NAME` — defaults to `IMA`

Do not paste the token into ChatGPT.

## Canonical activation target

VIEW → IDENTIFY → AUTHORIZE → ACT → OBSERVE → REFRESH

The TeamViewer adapter is one transport inside LIVE-001. BrowserGlass/Android bridge remains the existing free canonical path; TeamViewer is an optional external/enterprise transport until its licensing and Android SDK/REACH requirements are satisfied.

Official references:
- TeamViewer API: https://www.teamviewer.com/en/global/support/for-developers/
- Build an integration: https://www.teamviewer.com/en-us/global/support/knowledge-base/teamviewer-remote/for-developers/build-a-teamviewer-integration/
- Mobile SDK: https://www.teamviewer.com/en/global/support/knowledge-base/teamviewer-classic/integrations/core-integrations/teamviewer-mobile-software-development-kit-sdk/
- REACH API: https://www.teamviewer.com/en/global/support/knowledge-base/teamviewer-classic/integrations/core-integrations/remote-access-api-integration-guide/
