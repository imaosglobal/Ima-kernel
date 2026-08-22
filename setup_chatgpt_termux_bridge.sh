#!/data/data/com.termux/files/usr/bin/bash

set -Eeuo pipefail

BASE="$HOME/ima_kernel"
BRIDGE="$BASE/.ima/chatgpt_termux_bridge"
SERVER="$BRIDGE/mcp_server.py"
CONFIG="$BRIDGE/bridge_config.json"
LOG="$BRIDGE/bridge.log"

mkdir -p "$BRIDGE"

echo "=== IMA / CHATGPT TERMUX BRIDGE SETUP ==="
echo "BASE: $BASE"
echo "BRIDGE: $BRIDGE"

# ------------------------------------------------------------
# 1. BACKUP / INVENTORY
# ------------------------------------------------------------

STAMP="$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BRIDGE/backups/$STAMP"

for f in \
    "$BASE/ima_master_runtime.py" \
    "$BASE/api/server.py" \
    "$BASE/product/gateway/product_gateway.py"
do
    if [ -f "$f" ]; then
        cp "$f" "$BRIDGE/backups/$STAMP/"
    fi
done

# ------------------------------------------------------------
# 2. CONFIG
# ------------------------------------------------------------

cat > "$CONFIG" <<JSON
{
  "name": "IMA Termux Bridge",
  "version": "1.0.0",
  "transport": "mcp",
  "local_only": true,
  "ollama": false,
  "runtime": "$BASE/ima_master_runtime.py",
  "api": "$BASE/api/server.py"
}
JSON

# ------------------------------------------------------------
# 3. CREATE MCP SERVER
# ------------------------------------------------------------

cat > "$SERVER" <<'PY'
import json
import os
import sys
import time
from pathlib import Path

BASE = Path.home() / "ima_kernel"

if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

BRIDGE = BASE / ".ima" / "chatgpt_termux_bridge"

def runtime_status():
    result = {
        "bridge": "IMA Termux Bridge",
        "status": "online",
        "time": time.time(),
        "termux": True,
        "ollama": False,
        "runtime": False
    }

    try:
        import ima_master_runtime
        result["runtime"] = True
        result["runtime_module"] = str(
            Path(ima_master_runtime.__file__).resolve()
        )
    except Exception as e:
        result["runtime_error"] = str(e)

    return result


def ima_ask(message):
    if not isinstance(message, str):
        message = str(message)

    try:
        import ima_master_runtime

        result = ima_master_runtime.ask(message)

        return {
            "status": "ok",
            "source": "ima_master_runtime",
            "result": result
        }

    except Exception as e:
        return {
            "status": "error",
            "source": "ima_master_runtime",
            "error": str(e)
        }


def read_file(path):
    path = Path(path).expanduser().resolve()

    allowed_roots = [
        BASE.resolve()
    ]

    if not any(
        str(path).startswith(str(root))
        for root in allowed_roots
    ):
        return {
            "status": "denied",
            "error": "path outside IMA kernel"
        }

    try:
        return {
            "status": "ok",
            "path": str(path),
            "content": path.read_text(
                encoding="utf-8",
                errors="replace"
            )
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def main():
        json.dumps(
            {
                "name": "IMA Termux Bridge",
                "status": "ready",
                "transport": "stdio",
                "time": time.time()
            },
            ensure_ascii=False
        ),
        flush=True
    )

    for line in sys.stdin:
        line = line.strip()

        if not line:
            continue

        try:
            request = json.loads(line)
        except Exception as e:
                json.dumps(
                    {
                        "status": "error",
                        "error": f"invalid json: {e}"
                    },
                    ensure_ascii=False
                ),
                flush=True
            )
            continue

        method = request.get("method")
        params = request.get("params", {})

        if method == "health":
            response = runtime_status()

        elif method == "ima_ask":
            response = ima_ask(
                params.get("message", "")
            )

        elif method == "read_file":
            response = read_file(
                params.get("path", "")
            )

        else:
            response = {
                "status": "error",
                "error": f"unknown method: {method}"
            }

            json.dumps(
                response,
                ensure_ascii=False
            ),
            flush=True
        )


if __name__ == "__main__":
    main()
PY

# ------------------------------------------------------------
# 4. COMPILE
# ------------------------------------------------------------

python3 -m py_compile "$SERVER"

# ------------------------------------------------------------
# 5. LOCAL TEST
# ------------------------------------------------------------

echo '{"method":"health"}' \
| python3 "$SERVER" \
> "$BRIDGE/health_test.json"

echo '{"method":"ima_ask","params":{"message":"IMA_DIRECT_BRIDGE_TEST"}}' \
| python3 "$SERVER" \
> "$BRIDGE/ask_test.json"

# ------------------------------------------------------------
# 6. WRITE STATUS
# ------------------------------------------------------------

python3 - <<PY
import json
from pathlib import Path

p = Path("$BRIDGE/bridge_status.json")

data = {
    "status": "local_bridge_ready",
    "chatgpt_side": "not_registered",
    "termux_side": "ready",
    "ollama": False,
    "mcp_server": "$SERVER",
    "config": "$CONFIG",
    "health_test": "$BRIDGE/health_test.json",
    "ask_test": "$BRIDGE/ask_test.json"
}

p.write_text(
    json.dumps(data, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

PY

echo
echo "=== BRIDGE CREATED ==="
echo "MCP SERVER:"
echo "$SERVER"
echo
echo "STATUS:"
cat "$BRIDGE/bridge_status.json"
echo
echo "=== HEALTH TEST ==="
cat "$BRIDGE/health_test.json"
echo
echo "=== ASK TEST ==="
cat "$BRIDGE/ask_test.json"
echo
echo "=== DONE ==="
