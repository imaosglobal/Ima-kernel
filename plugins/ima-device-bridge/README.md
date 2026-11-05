# IMA Universal Device Bridge

A provider-neutral action bridge for authorized personal devices.

It gives compatible AI agents a controlled capability surface for a user's real device without requiring the device and agent to share a Wi-Fi network.

Design:
- outbound-only device connectivity
- owner-scoped device identity
- short-lived commands
- explicit action allowlist
- result verification
- revocation
- provider-neutral protocol
- no arbitrary shell execution
- compatible with Chrome CDP and Android AccessibilityService

The source lives in the IMA repository. Public marketplace publication remains subject to provider review and approval.

The bridge must not be used to bypass authentication, security controls, privacy boundaries, rate limits, paywalls or platform rules.
