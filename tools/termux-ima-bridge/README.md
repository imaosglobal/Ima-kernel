# IMA Universal Device Bridge — Termux/Chrome

This bridge is the Android reference agent for IMA Universal Action Core.

## Network-independent architecture

The production direction is outbound-only:

`Chrome/Termux -> HTTPS polling -> IMA API -> device command queue`

The device does **not** need a fixed Wi-Fi address, inbound port, or the same router. After enrollment, the bridge can reconnect over Wi-Fi or cellular because the device initiates the HTTPS connection.

The local CDP path is still used only on the device:

`IMA UI -> 127.0.0.1:8787 -> Chrome CDP -> Chrome Android`

## Current capabilities

- Stable IMA-tab targeting instead of blindly selecting the first Chrome tab.
- Screenshot capture.
- URL navigation.
- DOM click/type/key actions.
- Coordinate tap and scroll actions.
- Cloud command polling with exponential backoff.
- Device key persisted locally with restrictive file permissions.
- One-click enrollment from the IMA UI at `/enroll`.
- Fail-closed behavior when the cloud channel is unavailable.

## One-time device enrollment

1. Start the local bridge.
2. Sign in to IMA with Google.
3. Open Chat -> LIVE BROWSER.
4. When the local bridge is detected, press **Make connection persistent / חיבור קבוע** once.
5. The bridge registers the device through the authenticated IMA API, stores the returned device key locally, and starts the outbound cloud agent.

No device key should be copied into public pages, GitHub, or chat.

## Run

```bash
python ~/Ima-kernel/tools/termux-ima-bridge/bridge.py
```

Optional environment variables:

- `IMA_CLOUD_API_BASE` — defaults to `https://ima-915m.onrender.com`
- `IMA_DEVICE_KEY` — explicit key; normally not needed after enrollment
- `IMA_DEVICE_STATE_FILE` — persistent key file; defaults to `~/.config/ima/device.json`
- `IMA_CHROME_TARGET_HINT` — defaults to `imaosglobal.github.io/Ima-kernel`
- `IMA_CLOUD_POLL_SECONDS` — defaults to 2 seconds

## Security boundary

The bridge is not a public HTTP server. It binds to `127.0.0.1`. The cloud channel is outbound and authenticated with a per-device key. Commands are scoped by the IMA API and should be verified after execution.

The Termux bridge is a reference implementation, not yet the final Android background service. If Android/Termux kills the process, the cloud channel stops until the process is restarted. The production Android agent must provide lifecycle supervision, reconnect, revoke, visible connection state, and an emergency stop.

## Interactive IMA UI

The IMA Chat page contains a LIVE BROWSER panel. It now supports direct click/tap and scrolling on the mirrored Chrome screen, plus navigation and keyboard controls. This is an interactive control surface; it is not a native remote-desktop window embedded in ChatGPT itself.

