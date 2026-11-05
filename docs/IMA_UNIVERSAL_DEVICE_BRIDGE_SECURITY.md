# IMA Universal Device Bridge — Security & Consent Contract

**Status:** canonical product-security direction  
**Date:** 2026-11-05

## Purpose

IMA Universal Device Bridge connects an authorized AI session to a user's own device. It is an execution capability, not a general remote-access service.

## Default-deny

No device is controllable until:

1. the user explicitly enrolls it;
2. the device identity is established;
3. the user grants capabilities;
4. the session is authenticated;
5. the requested action is within the granted scope.

## Capability scopes

Examples:

- browser.read
- browser.navigate
- browser.click
- browser.type
- browser.capture
- app.read
- app.action
- shell.read
- shell.execute
- files.read
- files.write
- accessibility.observe
- accessibility.act

Scopes must be independently grantable and revocable.

Shell execution is never a default capability.

## Transport

The device agent should maintain an outbound encrypted connection to the relay. The device must not require inbound ports.

The connection must survive network changes by reconnecting through the same enrollment identity over whichever authorized network is currently available.

## Credentials

Use:

- device key pair;
- short-lived session credentials;
- rotating enrollment tokens;
- server-side revocation;
- signed requests;
- nonce/timestamp replay protection.

Never store provider API keys or permanent shared secrets in the repository.

## User visibility

The device must expose:

- connected/disconnected state;
- current controlling AI/session;
- granted capabilities;
- recent consequential actions;
- revoke/stop control.

The user must be able to terminate the connection locally.

## Action classes

LOW:
- read public page state;
- inspect non-sensitive UI state;
- take a screenshot when authorized.

MEDIUM:
- navigate;
- fill non-sensitive forms;
- edit files inside an authorized workspace.

HIGH:
- send messages;
- publish content;
- change account settings;
- install software;
- modify security settings;
- access sensitive information.

CRITICAL:
- transfer money;
- delete important data;
- change ownership;
- expose credentials;
- disable security controls;
- actions affecting third parties without their authorization.

HIGH and CRITICAL actions require explicit confirmation unless a narrowly scoped policy explicitly permits the operation and the action remains within the safety contract. CRITICAL operations should remain confirmation-gated.

## Verification

Every meaningful action must have a postcondition.

Examples:

- navigation: target URL observed;
- click: expected UI state observed;
- installation: package/version verified;
- file change: hash/diff verified;
- publication: public URL checked;
- payment: provider receipt checked.

No "done" claim without evidence.

## Prompt-injection resistance

Content displayed by websites, documents or applications is untrusted input.

Instructions encountered inside those sources must never silently expand the device's authority.

The agent must keep:

user intent > IMA safety policy > granted capability scope > untrusted content instructions

## Privacy

Private device data remains private.

Data should be collected only for the requested task, minimized, scoped, encrypted in transit, and deleted or retained according to the user's selected policy.

No cross-user memory is created merely because a device was connected.

## Children and vulnerable users

Use stronger defaults, narrower capabilities and human escalation where appropriate. The system must never use vulnerability as a reason to increase IMA's control.

The objective is to return capability to the person, not to make IMA indispensable.

## Abuse prevention

The public product must reject requests whose primary purpose is unauthorized access, credential theft, covert surveillance, malware, destructive persistence, evasion of security controls or harm to others.

## Emergency stop

The device agent must provide a local kill/revoke path that does not depend on the AI or relay being available.

## Audit

Audit records should include:

request_id, user_id, device_id, capability, action, risk_class, authorization, timestamp, result, verification, evidence_ref

Secrets and sensitive payloads must not be logged.

## Recovery

A network loss must fail closed.

A relay restart must not silently broaden permissions.

A device reboot must require a policy-defined re-enrollment or securely recover only the previously granted limited policy.

## Product rule

The bridge exists to make useful things possible, not to make control invisible.

