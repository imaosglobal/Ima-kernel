# IMA Deal Hunter — live implementation status

Implemented in `founder/executive_ai/global_intelligence/`:

- `deal_hunter.py` — public commercial-demand discovery and scoring.
- `deal_hunter_daemon.py` — 15-minute continuous scan loop.
- `opportunity_engine.py` — feeds commercial deals into IMA opportunity ranking.
- `opportunity_ranker.py` — ranks explicit payout opportunities above generic world signals.
- `../data/deal_hunter_opportunities.json` — current public Referr opportunities seeded from live marketplace pages.
- `start_deal_hunter.sh` / `stop_deal_hunter.sh` — daemon controls.

Safety boundary:

- Only public commercial signals are collected.
- No scraped personal data is treated as a lead.
- Consent remains required before transferring a person's details.
- No paid lead purchase is performed automatically.
- No unsolicited outreach is performed automatically.

Current live evidence source: Referr public lead-request pages.

Current limitation: the remote shell can read/write the user's Termux files but Android blocks that shell from executing Termux binaries. The daemon must therefore be started from the actual Termux app.
