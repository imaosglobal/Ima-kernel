# IMA Release and Runtime Verification

This checklist separates repository automation from user-visible product behavior. A green workflow is not proof that the deployed application, memory, avatar, or external integrations work.

## Release gates

- [ ] Identify the exact commit SHA being released.
- [ ] Confirm required CI checks completed successfully for that SHA; distinguish `success`, `failure`, `cancelled`, and `skipped`.
- [ ] Confirm the Pages deployment completed and record its deployment/run URL.
- [ ] Verify the public site returns the expected application, not merely HTTP 200.
- [ ] Verify runtime health and the runtime API independently; record timestamp, endpoint, HTTP status, and a redacted response summary.
- [ ] Exercise one real user path: open app, send a message, receive a response, and confirm graceful behavior when runtime is unavailable.
- [ ] Verify memory only with a disposable test profile and confirm user data is not exposed across profiles.
- [ ] Verify avatar/voice fallback on a mobile browser, including Hebrew RTL rendering.
- [ ] Check external actions are permission-gated and never silently purchase, publish, message, or transfer personal data.

## Safe maintenance rules

1. Prefer additive changes and isolated branches/PRs for code or workflow changes.
2. Never bulk-close PRs/issues, delete artifacts, rotate secrets, or overwrite canonical/core assets as an automated cleanup step.
3. Treat generated demo PRs as untrusted until their diff, tests, dependencies, and provenance are reviewed.
4. Require human review before merging generated code or changing deployment/security workflows.
5. Do not report a capability as working based only on a README, registry declaration, successful build, or HTTP response.
6. If a check cannot be reached, report it as **unverified**, not healthy or failed.
7. Keep logs useful but redact tokens, credentials, private user content, and personal contact data.

## Incident record template

- Commit SHA:
- Workflow/run URL and conclusion:
- Deployment URL and timestamp:
- Runtime endpoint and HTTP status:
- User-path tested:
- Evidence captured (redacted):
- Known limitation:
- Follow-up issue/PR:

## Current status

This document defines the verification standard; it does not itself assert that any live runtime or user journey has passed. Update status only with fresh, reproducible evidence.
