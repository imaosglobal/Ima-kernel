# IMA Contributor Architecture

## Start here

1. Canonical vision: `IMA_CANONICAL_VISION.md`
2. Canonical runtime: `kernel/runtime/CANONICAL/`
3. Public runtime: `app.py`, `public_memory.py`, `identity_context.py`
4. Preservation/provenance: canonical preservation, portable identity and derivation-registry components
5. UI: `ima-ui/`
6. Verification: `tests/`, `.github/workflows/`, and `npm run ima:verify`

## Contribution path

Changes enter through normal Git commits or Pull Requests and must pass the repository verification gates before being treated as verified.

## Privacy boundary

Community-facing code must not expose private founder memory, credentials, security secrets, or another user's private memory.

## Capability claims

A capability is described as active only when its implementation and verification path exist. Documentation must not turn planned integrations into claims of live connectivity.
