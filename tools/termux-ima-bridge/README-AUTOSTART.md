# IMA Live Browser — persistent Android autostart

Goal: eliminate the repeated manual sequence of launching Chrome, forwarding
ADB port 9222, and starting the bridge.

The canonical path remains LIVE-001 / BrowserGlass / IMA Action Core.

## One-time setup

Install and enable Termux:Boot, then place an executable copy/symlink of
start-ima-bridge.sh in:

~/.termux/boot/10-ima-live-browser

Termux:Boot runs scripts from ~/.termux/boot at Android boot. Open the
Termux:Boot app once after installation.

The script:
1. starts the canonical IMA page in Chrome;
2. refuses to start a second bridge;
3. starts the existing canonical bridge only once;
4. leaves Android device control to the outbound authenticated native
   accessibility transport.

No Wireless Debugging pairing, fixed IP, ADB port-forward, or inbound device
port is required by the production LIVE-001 transport.

## Important

Do not create another bridge or another BrowserGlass surface.
