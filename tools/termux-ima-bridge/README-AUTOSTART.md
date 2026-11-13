# IMA Live Browser — persistent Android autostart

Goal: eliminate the repeated manual sequence of launching Chrome, forwarding
ADB port 9222, and starting bridge.py.

The canonical path remains LIVE-001 / BrowserGlass / IMA Action Core.

## One-time setup

Install and enable Termux:Boot, then place an executable copy/symlink of
start-ima-bridge.sh in:

~/.termux/boot/10-ima-live-browser

Termux:Boot runs scripts from ~/.termux/boot at Android boot. Open the
Termux:Boot app once after installation.

The script:
1. starts the canonical IMA page in Chrome;
2. reuses the existing paired ADB transport when Android has one;
3. recreates tcp:9222 -> localabstract:chrome_devtools_remote;
4. refuses to start a second bridge;
5. starts the existing canonical bridge only once.

This removes the repeated manual startup steps. Android Wireless Debugging
itself still has to remain enabled, and Android may rotate its TCP endpoint
after reboot/toggling. If the ADB transport is absent, the script deliberately
does not guess or create an insecure legacy TCP/5555 listener.

## Important

Do not create another bridge or another BrowserGlass surface.
