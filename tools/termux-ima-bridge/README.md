# IMA Termux Chrome Bridge

Purpose: keep Chrome Android as the user's browser and connect it to IMA through Termux + ADB/CDP.

Flow:
IMA public page (same phone) -> 127.0.0.1:8787 -> IMA bridge -> 127.0.0.1:9222 -> mobilebridge -> ADB -> Chrome Android.

One-time setup in Termux:
1. Android Settings -> Developer options -> Wireless debugging -> Pair device with pairing code.
2. Install packages: pkg update && pkg install -y git python nodejs android-tools golang
3. Clone mobilebridge: git clone https://github.com/VulpineOS/mobilebridge.git ~/mobilebridge
4. Build it: cd ~/mobilebridge && go install ./cmd/mobilebridge
5. Pair/connect using the IP and ports shown by Android Wireless debugging:
   adb pair <PAIR-IP:PAIR-PORT>
   adb connect <CONNECT-IP:CONNECT-PORT>
   adb devices
6. Start Chrome CDP proxy: mobilebridge --port 9222
7. In another Termux session run: python ~/Ima-kernel/tools/termux-ima-bridge/bridge.py

Expected bridge status: http://127.0.0.1:8787/status
Tabs: http://127.0.0.1:8787/tabs
Screenshot: http://127.0.0.1:8787/screenshot

Security: the bridge binds only to 127.0.0.1. Do not expose it publicly without authentication.

Why this path: mobilebridge is an open-source Android Chrome CDP bridge designed for real Chrome over ADB, so no replacement browser is required.