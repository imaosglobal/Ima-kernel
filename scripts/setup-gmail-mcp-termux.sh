#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

REPO="$HOME/Ima-kernel"
CFG="$HOME/.config/ima/gmail-mcp.env"

echo "== IMA Gmail MCP / Termux =="
echo "Repo: $REPO"

if [ ! -d "$REPO" ]; then
  echo "ERROR: $REPO not found"
  exit 1
fi

cd "$REPO"

if ! command -v node >/dev/null 2>&1; then
  echo "Installing Node.js..."
  pkg update -y
  pkg install -y nodejs-lts
fi

echo "Node: $(node --version)"
echo "npm:  $(npm --version)"

mkdir -p "$(dirname "$CFG")"
chmod 700 "$(dirname "$CFG")"

if [ ! -f "$CFG" ]; then
  cat > "$CFG" <<'EOF'
# IMA Gmail MCP — local only
# Fill these from Google Cloud OAuth Desktop credentials.
export GOOGLE_CLIENT_ID=""
export GOOGLE_CLIENT_SECRET=""
export IMA_GMAIL_ADDRESS="imaosglobal@gmail.com"
EOF
  chmod 600 "$CFG"
  echo
  echo "Created: $CFG"
  echo "Next: put the Google OAuth Client ID/Secret into that file."
else
  echo "Config exists: $CFG"
fi

echo
echo "MCP package check:"
npx -y @mcp-z/mcp-gmail --help >/dev/null 2>&1 || true
echo "OK: @mcp-z/mcp-gmail is available through npx."
echo
echo "After credentials are filled, run:"
echo "  source $CFG"
echo "  npx -y @mcp-z/mcp-gmail"
