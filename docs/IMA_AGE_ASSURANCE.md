# IMA Privacy-Preserving Age Assurance

Status: signed-attestation protocol implemented in source; production issuer configuration is **not verified** until the deployment has the required secrets and a real issuer test passes.

## Behavior

- The public chat route accepts an optional `age_attestation` token. It does not accept a raw `age`, `age_band`, date of birth, or a client-side boolean as proof.
- A valid attestation is a short-lived HS256 JWT signed by the trusted issuer configured for this IMA deployment.
- Required claims: `iss`, `aud`, `purpose="age_assurance"`, `iat`, `exp`, `age_band`, and `session_binding`.
- `age_band` must be one of `under_5`, `6_9`, `10_12`, `13_15`, `16_17`, `adult`. Exact date of birth, identity documents, face images and biometrics are not part of this contract.
- `session_binding` is the hexadecimal SHA-256 digest of the authenticated IMA session subject returned by the backend session validation, i.e. SHA-256 of the string `public:<opaque-session-id>`. The issuer must bind the proof to the same session; otherwise the proof is rejected.
- The token must be unexpired, not issued too far in the future, no more than 15 minutes long, signed with HS256, issued by the configured issuer, and intended for the configured audience.
- If the verifier is unconfigured or any check fails, the effective age remains `unknown` and the protective child-safety profile is used. No raw token is logged or persisted by this code.
- The API reports the effective band and whether the attestation was verified in `safety.age_assurance`. This status is not a claim that the production deployment has an issuer configured.

## Required deployment configuration

Set these secrets/variables in the backend deployment environment:

- `IMA_AGE_ATTESTATION_SECRET`: a high-entropy secret shared only by IMA and the trusted age-assurance issuer over a secure secret-management channel.
- `IMA_AGE_ISSUER`: exact issuer identifier expected in the signed claim.
- `IMA_AGE_AUDIENCE`: optional; defaults to `ima-public-chat`.

Never commit the secret to Git, expose it to browser JavaScript, or put it in a mobile app. The trusted issuer must be selected and reviewed, and the signing secret rotated through the deployment secret manager. A real issuer integration and live end-to-end test are required before describing age verification as live.

## Integration and release gates

1. Choose a reputable age-assurance issuer with a privacy and security assessment, appeal path, accessibility alternatives and relevant jurisdictional review.
2. The issuer verifies age using its approved method, then signs only the minimum age-band result and session binding. It must not reuse the information for advertising, profiling or unrelated learning.
3. The UI obtains the attestation from the issuer and sends it as `age_attestation` with the authenticated `/ima-api/chat` request. It must not mint or edit the claims itself.
4. Verify a valid token for every supported band, and test bad signatures, expired tokens, wrong issuer/audience, wrong session binding, invalid age bands, missing secrets and issuer outage.
5. Confirm deployed configuration using `GET /ima-api/age/status`, then run a real end-to-end issuer test. Until then the endpoint must show `not_configured` or the actual failure state.
6. Re-review retention, deletion, consent and child-facing UX before broad release.

## Limits

This code verifies an issuer-signed assertion; it does not itself establish a person's age. The quality of age verification depends on the external issuer's method and governance. HMAC is a shared-secret trust model: if the secret is exposed, the issuer and IMA must rotate it immediately. Independent security/privacy review is required before broad child-facing deployment.
