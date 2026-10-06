# IMA Tool Evidence Contract

Every tool action that can affect the outside world or produce a capability claim should return a structured evidence record.

Required fields: `timestamp`, `capability_id`, `provider`, `authorization`, `execution`, `verification`, `claimable`, `evidence`, and `provenance`. `failure_mode` is required for failed/unknown execution or contradicted verification.

IMA may claim an action was completed only when `execution=succeeded`, `verification=verified`, and `claimable=true`. Registration, connection, authentication, or reachability alone is not proof that an action happened.

Discovery and manifest preparation do not authorize an external connection. Candidate providers remain candidates until connection, health, and permissions are actually verified.

Evidence must preserve provenance and must never contain credentials, access tokens, passwords, or private payloads.