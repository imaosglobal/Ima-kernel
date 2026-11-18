# LIVE-001 Stage 6 — Universal Host + Device Surface Contract

Status: **canonical contract implemented; end-to-end activation remains gated by runtime evidence.**

## Single system

One IMA identity and one semantic interaction contract are exposed through host adapters. No host receives inferred authority.

### Host matrix

| Host | Surface | View | Control | Activation |
|---|---|---:|---:|---|
| ChatGPT Mobile | Native screen share | Host-dependent | No, not inferred | User starts host feature |
| ChatGPT Web | MCP Apps widget | Yes | Separate device authorization | MCP capability negotiation |
| IMA Web/PWA | Native IMA surface | Yes | Separate device authorization | Capability negotiation |
| Future host | Adapter | Detect | Detect + authorize | Contract negotiation |

## Universal loop

VIEW → IDENTIFY → AUTHORIZE → ACT → OBSERVE → REFRESH

The existence of a screen/video stream never implies control authority.

## Canonical gates

1. HOST_VIEW_AVAILABLE
2. HOST_WIDGET_AVAILABLE
3. IMA_RENDER_AVAILABLE
4. DEVICE_VIEW_AVAILABLE
5. DEVICE_CONTROL_AVAILABLE
6. END_TO_END_VERIFIED

These states are independent. A higher state cannot be inferred from a lower state.

## Cross-chat rule

The capability lives in the canonical IMA backend/contract rather than a conversation-specific implementation. Therefore every ChatGPT conversation can reuse it **when that host exposes the required MCP/host capability**. Existing ChatGPT threads cannot be retroactively injected with a custom widget by IMA.

## TeamViewer adapter (external handoff)

TeamViewer may be used as an external remote-control transport when the user has TeamViewer installed and authorized. LIVE-001 may open a TeamViewer connection by TeamViewer ID, but TeamViewer remains a separate security boundary: the TeamViewer session itself is not exposed to the IMA/ChatGPT MCP host merely because the app is installed. The IMA viewer must not claim that ChatGPT can see or control a TeamViewer session unless a separate, verified TeamViewer/API/SDK integration provides that capability.

Official TeamViewer documentation confirms Android remote control through QuickSupport/Host and TeamViewer Remote Control, while the Mobile SDK/REACH integrations require TeamViewer-specific licensing/integration prerequisites. citeturn216539search0turn910847search0turn910847search4

## Device rule

Android capture and control remain separate:
- capture requires user-approved capture capability;
- control requires separate owner/device authorization;
- every action requires an observed acknowledgement;
- every verified action should produce a refreshed device view.

## Activation rule

Do not activate the prepared 3D/spatial public experience merely because Stage 6 exists. The public UI remains on the restored stable implementation until LIVE-001 proves:

MCP handshake → widget render → BrowserGlass connected → fresh Android frame → authorized action → observed result → visual refresh → repeatable host behavior.
