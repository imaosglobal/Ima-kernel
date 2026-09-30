# IMA Continuous Evolution

IMA is intended to improve through an observable engineering loop:

DISCOVER -> SPECIFY -> IMPLEMENT -> TEST -> VERIFY -> DEPLOY -> OBSERVE -> LEARN

Automation may:
- run tests and integrity checks
- build the public UI
- deploy verified changes
- inspect service health
- refresh capability metadata
- propose bounded maintenance changes

Automation must not:
- expose private memory
- publish secrets
- bypass authorization
- impersonate users
- perform unsolicited outreach
- silently make irreversible consequential changes

IMA's capabilities are not defined by one conversational model.
They are defined by the verified union of the models, tools, agents,
devices and knowledge sources actually connected to its runtime.
