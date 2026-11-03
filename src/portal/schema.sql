CREATE TABLE IF NOT EXISTS claim_status (
    claim_id TEXT PRIMARY KEY,
    policy_id TEXT NOT NULL,
    status TEXT NOT NULL,
    paid_cents INTEGER NOT NULL CHECK (paid_cents >= 0)
);
