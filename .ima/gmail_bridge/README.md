# IMA Gmail → Build Recovery Bridge

Gmail notification → OAuth read-only access → GitHub Actions run URL → failed logs via GitHub CLI → incident record → optional local repair command.

One-time:
1. Create a Google Cloud OAuth 2.0 Desktop App credential for Gmail.
2. Save the downloaded JSON as `.ima/gmail_bridge/credentials.json`.
3. `pip install -r .ima/gmail_bridge/requirements.txt`
4. `gh auth status`
5. `python .ima/gmail_bridge/ima_gmail_build_watch.py`

The first run opens Google's OAuth consent flow and requests Gmail **read-only** access. Offline OAuth uses a refresh token so the watcher can continue after access-token expiry.

For repair, set `IMA_AUTOFIX_COMMAND`. It receives `IMA_FAILURE_LOG`, `IMA_FAILURE_RUN`, and `IMA_FAILURE_SUBJECT`. Without that variable the bridge captures failures only and does not claim to repair them.

Gmail is an alert/evidence channel; GitHub Actions logs and repository state remain the engineering source of truth.
