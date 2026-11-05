# Shield customer portal

**Application:** Billing & Customer (`billing-customer`)

**Component:** `CM-PORTAL`

**Owner:** Customer experience

`src/portal/dashboard.py` builds a claim dashboard through callbacks to
`shield-policy-service`, `shield-claims-service`, and `shield-billing-service`.
Supply a local SQLite connection to `CustomerPortal`; initialization creates
the portal's schema. `contracts/portal-api.yaml` describes the intended API.
There is no browser UI or HTTP server in this readable fixture.

The current dashboard does not display payment-reason explanations.

## Specification consumer

Canonical specs, authoring, gates, and requirement metrics live only in
[`amithp-ust/Intent-to-spec`](https://github.com/amithp-ust/Intent-to-spec).
Shared glossary, map, standards, and policy remain in
[`amithp-ust/shield-context`](https://github.com/amithp-ust/shield-context).
This repo owns `CM-PORTAL` implementation, not spec authoring. See
[AGENTS.md](AGENTS.md) for immutable approved spec references, issue/PR traceability,
human review, and fixture-contract checks. Do not install authoring here or copy
specs; empty `specs/.gitkeep` is a legacy placeholder.

Python 3.11+, standard library only. Run `python -m unittest discover -s tests`
from this repository root; the unit-test CI runs the same command on Python 3.11.
Use synthetic data only; this fixture is not a production customer portal.
