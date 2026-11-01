# IMA — Real User Feedback & Reputation Protocol

## Feedback contract

Every public IMA interface should provide four simple choices:
- useful;
- not useful;
- report a problem;
- suggest an improvement.

Feedback is attributed to a session/user pseudonym only when necessary for product integrity. Message content is not required for a rating.

Every accepted feedback item must receive a durable archive record and a receipt/acknowledgement. The original text, sentiment, language, source, page, client timestamp, timezone, provenance and privacy-preserving identity binding must be retained according to the applicable retention policy. A UI acknowledgement is not evidence of persistence unless the API has returned an accepted result.

## Non-regression invariant

The public feedback path must not regress to a generic acknowledgement that hides persistence status. The canonical public product must expose the verified acknowledgement contract:
"המשוב נשמר וקיבל קבלה."

A release is blocked if:
- the feedback form is missing;
- the durable feedback API call is missing;
- the verified acknowledgement contract is missing;
- the legacy generic acknowledgement "המשוב התקבל תודה" returns to the public bundle;
- the deployed GitHub Pages bundle does not match the canonical source SHA.

The deployment pipeline must test the source, built bundle, gh-pages branch and public browser surface before treating the release as verified.

## Feedback lifecycle

COLLECT → ACKNOWLEDGE → ARCHIVE → CLASSIFY → PROTECT → TRIAGE → LEARNING CANDIDATE → DECIDE → FIX → TEST → VERIFY → PUBLISH CHANGE → RECORD EVIDENCE → ASK AGAIN

Accepted feedback must enter the learning/execution ledger with explicit state. A suggestion is evidence, not automatic truth. IMA must distinguish:
- received;
- archived;
- duplicate/conflict;
- learning candidate;
- justified;
- rejected/not justified;
- implementation planned;
- implemented;
- tested;
- deployed;
- verified live;
- blocked, with exact blocker.

Where feedback is justified, the corresponding product change should be implemented through the canonical release path and linked to the originating feedback/provenance record without exposing private user information. Where it is not justified, preserve the reasoning/evidence instead of silently discarding the signal.

Feedback must never silently become shared model learning. Project learning requires the explicit governance path.

## Reputation

App-store ratings and reviews are external user signals. IMA must:
- link to the official store listing only after the listing is verified;
- ask for a rating only after a meaningful successful experience;
- never manufacture or purchase ratings;
- never condition essential functionality on a positive review;
- preserve negative feedback as a product signal;
- respond to reviews truthfully and without impersonation.

## Globalization

Feedback must accept the user's language. Classification may normalize internally, but the original feedback and language/provenance must be preserved.

Minimum launch languages for the growth program:
Hebrew, English, Arabic, Spanish, French, Portuguese, German, Hindi, Japanese, Korean, Chinese.

These are a rollout target, not a claim that all translations are already live.

## User truth dashboard

The dashboard must separately expose:
- verified users;
- anonymous traffic;
- returning users;
- feedback volume;
- satisfaction distribution;
- error rate;
- retention when statistically meaningful;
- country/region only when privacy thresholds permit;
- channel attribution only when lawfully collected.

No dashboard may label an unverified estimate as a verified user count.
