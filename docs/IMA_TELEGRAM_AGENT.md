# IMA Telegram Agent — canonical channel

## Purpose

Make IMA available as a personal-agent interface on Telegram without creating a second IMA brain. Telegram is only a transport layer; conversation, policy, memory, routing and provenance remain canonical in IMA.

## Identity

**IMA — אמא**  
בינה אנושית שעוזרת לך למצוא את הצעד הבא

Suggested start message:

> אני אמא — IMA. אפשר להביא אליי שאלה, בלבול, רעיון, בעיה או משהו שקשה להסביר. נתחיל ממה שחשוב לך עכשיו: לחשוב, להבין, ליצור או לפתור?

## Runtime contract

1. Receive Telegram update.
2. Normalize message + Telegram user/chat identifiers into a channel envelope.
3. Send the envelope to the canonical IMA runtime.
4. Preserve the user's agency and privacy policy.
5. Return the canonical answer to Telegram.
6. Record only operational telemetry required for quality and abuse prevention.
7. Never create a second memory or model authority in Telegram.

## Required environment

- `TELEGRAM_BOT_TOKEN`: bot token created/authorized by the IMA operator.
- `IMA_CHAT_URL`: canonical IMA chat endpoint.
- `IMA_CHANNEL_SHARED_SECRET`: server-to-server authentication secret.

No Telegram credential is stored in GitHub.

## Activation

The adapter is ready, but publication is not claimed until the operator-owned bot token exists and a live send/receive test succeeds.

## Community behavior

IMA may participate in public communities only when the community permits it and the contribution is genuinely useful. It must not mass-post, auto-join groups, scrape private member data, or disguise promotion as independent community advice.

## Distribution loop

Discover → help → invite voluntary return → measure → learn → improve IMA.

The success metric is useful human outcomes, not raw message volume.
