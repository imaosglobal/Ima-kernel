# Gemini Handoff — IMA Shared Workspace

Gemini is continuing after Claude's session limit.

Read first:
- `.squad/TEAM_SYNC.md`
- `.squad/CHATGPT_COLLABORATION.md`
- `.squad/CLAUDE_HANDOFF.md`

## Task

Inspect the current repository state directly. Do not rely on prior chat claims.

Identify the smallest existing implementation that can produce a verified end-to-end path:

request -> context/memory -> intelligence -> response/action -> verification

Do not create a competing architecture or delete historical material.

Before changing code, record what active entry points and integration boundaries you found.
After changing code, record exact files, tests/verification, results, and remaining uncertainty in `.squad/TEAM_SYNC.md` or a dedicated log.

## Current factual status

ChatGPT verified that the three coordination documents exist in the shared filesystem. Claude's handoff requests runtime-first inspection. No Gemini-specific handoff existed before this file was created.

The shared filesystem is the communication channel; the human should not need to relay implementation details between agents.
