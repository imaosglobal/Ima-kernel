# IMA Universal Action Bridge

## Purpose

IMA Universal Action Bridge connects an authorized AI agent to the real device owned by the person using IMA.

This is not a claim that IMA invented computer-use agents. Browser agents, Android accessibility bridges, WebMCP and remote device-control products already exist. The IMA-specific goal is to unify them under one provider-neutral, evidence-gated and human-centered action layer with continuity, consent, provenance, adaptive installation and post-action verification.

## Architecture

AI / IMA / compatible agent
|
| authenticated command
v
IMA device command plane
|
| owner + device scope
v
outbound-only phone agent
|                    |
v                    v
Chrome CDP bridge    Android Accessibility
|                    |
v                    v
browser              real device

The device initiates the network connection. No inbound public port is required.

## Network continuity

A device can move between Wi-Fi networks and cellular data because the transport is outbound HTTPS to the IMA service. This avoids dependence on a stable local IP, shared Wi-Fi, public port forwarding or VPN.

It does not defeat Android background limits. A production installer must configure the appropriate background/foreground mechanism, boot startup and power policy for the specific device and then verify that the agent remains alive.

## Adaptive execution

IMA should prefer the strongest reliable interface in this order:

1. official API or structured tool
2. WebMCP or equivalent structured browser tool
3. CLI
4. accessibility tree
5. deterministic UI action
6. visual fallback

This reduces brittleness and risk.

## Safety

The public action surface is allow-listed. It does not expose arbitrary shell execution.

The bridge must require authorization, use least privilege, support revocation, separate read and write actions, require confirmation for consequential actions, preserve command/result evidence, and stop when authorization is withdrawn.

It must never bypass authentication, security controls, privacy boundaries, rate limits, paywalls or provider terms.

## Productization

The same protocol can become an IMA website capability, Android installer, browser extension, MCP server, SDK or white-label integration.

The product is the capability layer, not a dependency on one AI model.

## Founder provenance

This records the IMA-specific formulation and implementation path inside the project's existing provenance system. It is not a legal determination of patentability or exclusive ownership. Existing rights, succession and revenue-governance records remain authoritative.

## Breakthrough log — 2026-11-05

IMA moved from a local Termux-to-Chrome debugging bridge toward a reusable universal action architecture.

Implemented today:
- owner-scoped device command tables;
- one-time device key issuance with server-side hashing;
- transactional command claiming;
- expiring allow-listed commands;
- device revocation;
- outbound network model independent of the current Wi-Fi;
- reusable Termux device agent;
- compatibility path for the existing Chrome CDP bridge and Android AccessibilityService.

Remaining production gates:
- live end-to-end device registration and command execution;
- Android background reliability;
- device management UI;
- independent security testing;
- provider review/publication;
- pricing and commercial validation.
