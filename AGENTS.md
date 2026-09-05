# IMA — Base44 Dev Environment

## Architecture
- **Frontend**: `ima-ui/` — React 19 + Vite dev server (port 5173, mapped to host 3000).
  - Proxies `/ima-api/*` to the backend via `API_TARGET` env var (defaults to `http://127.0.0.1:8080`; set to `http://api:8080` in compose).
  - Endpoints used: `POST /ask`, `GET /health`, `GET /ready`.
- **Backend**: `api/server.py` — Python stdlib `http.server` on port 8080.
  - Needs `requests` (pip) for optional Supabase memory store; Supabase calls are wrapped in try/except so the server boots without credentials.
  - Import chain: `api/server.py` → `ima_master_runtime.py` → `ima_system.py` (many learning/engine/language modules). All exist in the repo.

## Running
```
docker compose -f docker-compose.base44.yml up -d --build
```
Verify: `curl -sf http://localhost:3000/` (frontend) and `curl -sf http://localhost:3000/ima-api/health` (proxied backend).

## No external secrets required
Supabase/Google/Apple credentials in `.env.production.template` are optional — the app runs without them. Memory falls back to local JSON files.

## Notes
- The repo root has many legacy/backup files (`.bak`, `_backup_*`, `*.before_*`). The active code is `ima-ui/` (frontend) and `api/server.py` + its import chain (backend).
- `server.js` (root) references missing `kernel/memory_engine` and `kernel/stability` — not used; the Vite frontend is the real entry point.
- `Dockerfile` and `docker-compose.yml` at root target a Python/gunicorn build on port 10000/8080 — not used by Base44 compose.
