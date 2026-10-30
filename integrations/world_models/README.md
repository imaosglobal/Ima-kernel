# IMA World-Model Integration

This directory is the single integration boundary for interactive world-model providers.

## Live connection gate

A provider adapter may be marked live only after all of these are true:

1. The provider's official API/SDK is identified.
2. Credentials are supplied through the deployment secret store, never committed.
3. The adapter implements `WorldModelProvider`.
4. A bounded generation request succeeds against the real provider.
5. Returned provenance identifies the provider and simulation status.
6. A regression test passes without requiring private credentials.
7. Public capability metadata is updated from `NOT_VERIFIED` to `VERIFIED_LIVE` only after the live test evidence exists.

IMA must not claim a live Genie/other provider connection from this contract alone.

## Intended first use

The first safe live demonstration should be a low-risk interactive educational environment, not robotics, medicine, driving or another high-impact domain.

Example request: generate a small fictional room where a user can move around and inspect objects for 30 seconds.

## Security

- Never commit API keys.
- Never upload private user data to a provider without explicit authorization and an appropriate data policy.
- Bound duration, compute and output size.
- Preserve provider provenance.
- Keep simulation outputs separate from real-world facts.
