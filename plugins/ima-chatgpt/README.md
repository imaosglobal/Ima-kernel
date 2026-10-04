# IMA public distribution package

## Purpose
This package is the portable distribution layer for IMA. The canonical intelligence remains in IMA's core repositories; this package exposes a standards-based MCP gateway to compatible hosts.

## Current endpoint
- MCP: https://ima-server-1ptk.onrender.com/mcp
- Website: https://ima-server-1ptk.onrender.com/
- Support: https://ima-server-1ptk.onrender.com/support
- Privacy: https://ima-server-1ptk.onrender.com/privacy
- Terms: https://ima-server-1ptk.onrender.com/terms

## Truth state
- Package: PREPARED
- MCP endpoint: DEPLOYMENT_PENDING_VERIFICATION
- OpenAI public publication: NOT_SUBMITTED
- Provider approval: REQUIRED
- User installation/connection: OPT_IN
- Demo recording: NOT_YET_PROVIDED
- Domain challenge: requires provider-issued token in `OPENAI_APPS_CHALLENGE`

## Distribution principle
One canonical IMA core, many adapters. Add an adapter only when the host supports MCP or an authorized integration mechanism. Never bypass provider review, authentication, rate limits, licensing or user consent.

## Review materials
The manifest contains exactly five positive and three negative review cases as required for initial MCP review. The demo URL is intentionally absent until a real accessible recording exists; no placeholder URL is used.
