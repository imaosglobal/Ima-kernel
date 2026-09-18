#!/data/data/com.termux/files/usr/bin/bash
set -e

TARGET="imaosglobal@gmail.com"
LOGIN_URL='https://accounts.google.com/v3/signin/identifier?continue=https://accounts.google.com/ManageAccount?nc%3D1&followup=https://accounts.google.com/ManageAccount?nc%3D1&passive=1209600&flowName=GlifWebSignIn&flowEntry=ServiceLogin'

mkdir -p .ima/gmail_bridge
chmod 700 .ima/gmail_bridge

echo "[IMA] Opening Google sign-in..."
termux-open-url "$LOGIN_URL"

echo
echo "[IMA] Sign in with: $TARGET"
echo "[IMA] After successful login, return here."
echo
read -rp "Press ENTER after the correct account is open..."

cat > .ima/gmail_bridge/bound_account.json <<JSON
{
  "provider": "google",
  "service": "gmail",
  "email": "$TARGET",
  "status": "account_selected",
  "source": "android_browser_session",
  "bound_at": "$(date -Iseconds)"
}
JSON

chmod 600 .ima/gmail_bridge/bound_account.json

echo
echo "[IMA] GMAIL_ACCOUNT_BOUND=$TARGET"
echo "[IMA] CONNECTION_RECORD=STORED"
echo "[IMA] PATH=.ima/gmail_bridge/bound_account.json"
