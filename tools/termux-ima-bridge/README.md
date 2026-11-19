# IMA Universal Device Bridge — Termux/Chrome

This bridge is the Android reference agent for IMA Universal Action Core.

## Canonical network-independent architecture

The production transport is outbound-only:

`Termux/Android agent -> HTTPS -> IMA API -> authenticated device command queue`

The device does **not** require a fixed Wi-Fi address, inbound port, the same router, or a Wireless Debugging IP/port.

The canonical LIVE-001 surface remains:

`IMA UI -> LIVE-001 -> authenticated IMA device channel -> Android/Chrome`

ADB/Wireless Debugging is **not the production transport**. Any ADB support in `bridge.py` is legacy/local fallback and must never be presented as a required pairing step.

## Current verified architecture

- LIVE-001 remains the single canonical live-browser surface.
- The Termux launcher is `bridge_launcher.py`; do not run `bridge.py` separately when the launcher is active.
- The cloud agent uses an authenticated per-device key and outbound HTTPS polling.
- The device key is persisted locally with restrictive permissions.
- Enrollment is performed through the authenticated IMA UI/API.
- The bridge is intended to reconnect over Wi-Fi or cellular without a fixed device IP.

## Important implementation boundary

The current repository still contains ADB/CDP code for local Chrome/device operations. That code is retained as a compatibility fallback; it is **not** proof that a native Android screen/input transport is available without an Android-side transport provider.

Therefore the system must report the native transport as unavailable rather than silently falling back to Wireless Debugging.

No device key should be copied into public pages, GitHub, or chat.

## Run

```bash
python ~/Ima-kernel/tools/termux-ima-bridge/bridge_launcher.py
```

Do **not** start `bridge.py` separately if `bridge_launcher.py` is already running.

## Optional environment variables

- `IMA_CLOUD_API_BASE` — defaults to `https://ima-915m.onrender.com`
- `IMA_DEVICE_KEY` — explicit key; normally not needed after enrollment
- `IMA_DEVICE_STATE_FILE` — persistent key file; defaults to `~/.config/ima/device.json`
- `IMA_CHROME_TARGET_HINT` — defaults to `imaosglobal.github.io/Ima-kernel`
- `IMA_CLOUD_POLL_SECONDS` — defaults to 2 seconds
- `IMA_ALLOWED_ORIGINS` — comma-separated browser origins allowed to invoke local actions

## Security boundary

The bridge binds locally to `127.0.0.1`. The cloud channel is outbound and authenticated with a per-device key. Commands are scoped by the IMA API and should be verified after execution.

The native Android transport is implemented by `android/ima-native-provider`: an Android AccessibilityService polls the local Termux bridge over loopback (`127.0.0.1:8787`) and provides screen capture/input without ADB, Wireless Debugging, a fixed Wi-Fi address, or an inbound network port. LIVE-001 must still report the provider as unavailable until the Android service is installed, enabled, and runtime-verified.

## Interactive IMA UI

The IMA Chat page contains the canonical LIVE-001 panel. It is not a second browser system and all future improvements must attach to LIVE-001.
\n## Native provider\n\nBuild artifact: `ima-native-provider-debug-apk`. After installation, Android requires the user to enable IMA under Accessibility. This is the only required Android authorization; the device transport itself remains local loopback + outbound HTTPS.\n