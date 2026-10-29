# IMA Capability Delta — 2026-10-29

## Verified facts

- ChatGPT connected apps can support event-triggered tasks for eligible users.
- Official OpenAI documentation dated 2026-08-25 states webhook-triggered tasks support new Gmail messages, Slack channel messages, and GitHub pull-request activity.
- The same documentation states Free users cannot create webhook-triggered tasks; Free users can create up to three active scheduled tasks, recurring no more than daily.
- Therefore the current IMA account's daily scan cannot be truthfully upgraded to real-time event monitoring while the account remains Free.
- Plugin extensions for ChatGPT are documented, but web extensions are still described as coming soon to Free/Go; no claim of availability is made here.
- Public plugin submission is supported through OpenAI's plugin directory submission flow; publication requires review and approval.
- Current Supabase project `tenpzpvqvtezezaossjd` is verified ACTIVE_HEALTHY.
- GitHub received a new whole-system multi-perspective review sequence on 2026-10-28, followed by a single-scheduled fix.

## MISSED-CAPABILITY-DETECTION assessment

No confirmed missed capability was established in this run.

Reason: the event-trigger feature is materially relevant but is not eligible on the current Free plan. The earliest official evidence found is 2026-08-25. This is recorded so future runs distinguish "feature exists" from "feature is available to this account".

## Monitoring rule

Every capability scan must keep three states separate:
1. exists in OpenAI product;
2. eligible for this account/plan/region;
3. actually connected and successfully tested.

Never promote state 1 to state 3 without evidence.
