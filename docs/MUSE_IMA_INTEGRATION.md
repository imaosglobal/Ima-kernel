# Muse / Meta AI integration boundary

Muse is an external AI surface, not a fake GitHub Action.

## Canonical IMA endpoint
https://ima-universal-action-core.onrender.com/mcp

## Intended connection
Muse → Meta Connector → MCP → IMA Universal Action Core

## Current state
- IMA MCP implementation: present in the repository.
- Public root/health endpoint: deployed.
- Muse Custom Connector: requires Meta-side authorization/availability.
- Do not claim Muse is connected until a real Meta connector test succeeds.

## Security
Credentials belong in the provider's secure credential store or GitHub/Render secrets.
Never commit API keys, bearer tokens, session identifiers or private user data.

## Team role
Muse may propose ideas, inspect approved IMA capabilities and participate in review when a real connector or Meta Model API authorization exists.
