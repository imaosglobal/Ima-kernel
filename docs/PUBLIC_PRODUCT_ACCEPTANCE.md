# IMA Public Product Acceptance Gate

Updated: 2026-10-26

## Required public path

1. Open the public IMA Pages URL.
2. Load the UI without a blank/error state.
3. Resolve the public API base.
4. Read /ima-api/auth/config.
5. If Google is configured, render the Google Identity Services button.
6. Complete Google sign-in and receive a signed IMA session.
7. Send a chat message.
8. Receive a non-empty IMA response.
9. Verify the response passed the public safety layer.
10. Verify consent-gated personal memory remains off unless the user enables it.
11. Verify runtime/health endpoints.
12. Verify Pages deployment after UI changes.

## Truth boundary

Code presence is not public verification. A capability becomes PUBLIC_VERIFIED only after the above path succeeds against the deployed public URLs.

## Current evidence

- Frontend contains a Google Identity Services login path.
- Backend contains Google credential verification and signed public sessions.
- Backend public chat path was repaired to pass personalization data correctly.
- Google OAuth blueprint registration was added to the Flask production app.
- GitHub Pages workflow is configured to build/deploy ima-ui on main changes.
- External runtime verification from this environment is currently unavailable, so Google login and public chat remain NOT_VERIFIED until a live HTTP check succeeds.
