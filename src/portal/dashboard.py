"""Synthetic customer claim dashboard (CM-PORTAL)."""

from collections.abc import Callable
from pathlib import Path
import sqlite3


class CustomerPortal:
    def __init__(self, connection: sqlite3.Connection, get_policy: Callable,
                 get_claim: Callable, premium_schedule: Callable):
        self.connection = connection
        self.get_policy = get_policy
        self.get_claim = get_claim
        self.premium_schedule = premium_schedule
        self.connection.executescript(
            Path(__file__).with_name("schema.sql").read_text()
        )

    def refresh_claim(self, claim_id: str) -> dict:
        claim = self.get_claim(claim_id)
        if claim["claim_id"] != claim_id:
            raise ValueError("Claim response does not match requested claim")
        with self.connection:
            self.connection.execute(
                "INSERT INTO claim_status (claim_id, policy_id, status, paid_cents) "
                "VALUES (?, ?, ?, ?) ON CONFLICT(claim_id) DO UPDATE SET "
                "policy_id = excluded.policy_id, status = excluded.status, "
                "paid_cents = excluded.paid_cents",
                (claim_id, claim["policy_id"], claim["status"], claim["paid_cents"]),
            )
        return self.cached_claim(claim_id)

    def cached_claim(self, claim_id: str) -> dict:
        row = self.connection.execute(
            "SELECT claim_id, policy_id, status, paid_cents "
            "FROM claim_status WHERE claim_id = ?",
            (claim_id,),
        ).fetchone()
        if row is None:
            raise LookupError(f"Claim is not available locally: {claim_id}")
        return dict(zip(("claim_id", "policy_id", "status", "paid_cents"), row))

    def dashboard(self, claim_id: str) -> dict:
        claim = self.refresh_claim(claim_id)
        policy = self.get_policy(claim["policy_id"])
        premium = self.premium_schedule(claim["policy_id"])
        return {
            "claim": claim,
            "policy": policy,
            "premium_schedule": premium,
        }
