# Shield customer portal

**Application:** Billing & Customer (`billing-customer`)

**Component:** `CM-PORTAL`

**Owner:** Customer experience

`src/portal/dashboard.py` builds a claim dashboard through callbacks to
`shield-policy-service`, `shield-claims-service`, and `shield-billing-service`.
Supply a local SQLite connection to `CustomerPortal`; initialization creates
the portal's schema. `contracts/portal-api.yaml` describes the intended API.
There is no browser UI or HTTP server in this readable fixture.

Shared context: `amithp-ust/shield-context` (`AGENTS.md`, glossary, scope,
standards, component map). `specs/` is empty pending spec pull requests.
For a future `001-claim-payment-reason` intent, this repository receives only
portal requirements linked to the full primary spec in `shield-claims-service`.
The current dashboard does not display payment-reason explanations.

Python 3.12+, standard library only. Run `python -m unittest discover -s tests`.
Use synthetic data only; this fixture is not a production customer portal.
