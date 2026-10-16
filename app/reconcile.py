"""Core reconciliation logic — pure Python, no dependencies.

Matches expected orders/invoices against actual payments and explains
every discrepancy in plain language. This is the shared kernel reused
across Open Agent / Nebius / PayPal / Databricks submissions.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Order:
    order_id: str
    client: str
    amount: float
    currency: str = "USD"


@dataclass
class Payment:
    payment_id: str
    order_ref: str  # order_id this payment claims to settle
    amount: float
    currency: str = "USD"
    source: str = "paypal_sandbox"  # paypal_sandbox | bank | manual


@dataclass
class Finding:
    order_id: str
    kind: str  # matched | amount_mismatch | missing_payment | duplicate_payment | fee_suspected | currency_mismatch | orphan_payment
    explanation: str
    expected: float | None = None
    received: float | None = None


def reconcile(orders: list[Order], payments: list[Payment],
              fee_rate_hint: float = 0.029) -> list[Finding]:
    """Explain-why reconciliation: every order and stray payment gets a finding."""
    findings: list[Finding] = []
    by_ref: dict[str, list[Payment]] = {}
    for p in payments:
        by_ref.setdefault(p.order_ref, []).append(p)

    known_ids = {o.order_id for o in orders}

    for order in orders:
        pays = by_ref.get(order.order_id, [])
        if not pays:
            findings.append(Finding(
                order.order_id, "missing_payment",
                f"No payment found for order {order.order_id} "
                f"({order.client}, {order.amount:.2f} {order.currency}). "
                f"Action: send a payment reminder / payment link.",
                expected=order.amount, received=0.0))
            continue
        if len(pays) > 1:
            total = sum(p.amount for p in pays)
            findings.append(Finding(
                order.order_id, "duplicate_payment",
                f"{len(pays)} payments reference order {order.order_id}, "
                f"totalling {total:.2f} vs expected {order.amount:.2f}. "
                f"Action: check for a double charge and refund the extra payment.",
                expected=order.amount, received=total))
            continue
        pay = pays[0]
        if pay.currency != order.currency:
            findings.append(Finding(
                order.order_id, "currency_mismatch",
                f"Payment {pay.payment_id} is in {pay.currency} but the order "
                f"is in {order.currency}. Action: confirm the FX rate applied.",
                expected=order.amount, received=pay.amount))
        elif abs(pay.amount - order.amount) < 0.005:
            findings.append(Finding(
                order.order_id, "matched",
                f"Payment {pay.payment_id} matches order {order.order_id} exactly "
                f"({pay.amount:.2f} {order.currency}). No action needed.",
                expected=order.amount, received=pay.amount))
        else:
            diff = order.amount - pay.amount
            fee_guess = round(order.amount * fee_rate_hint, 2)
            if pay.amount < order.amount and abs(diff - fee_guess) <= max(0.35, order.amount * 0.01):
                findings.append(Finding(
                    order.order_id, "fee_suspected",
                    f"Payment {pay.payment_id} is {diff:.2f} short of the order total. "
                    f"The shortfall is consistent with a ~{fee_rate_hint:.1%} processing "
                    f"fee ({fee_guess:.2f}). Action: record the fee, do not chase the client.",
                    expected=order.amount, received=pay.amount))
            else:
                findings.append(Finding(
                    order.order_id, "amount_mismatch",
                    f"Payment {pay.payment_id} is {pay.amount:.2f} but the order is "
                    f"{order.amount:.2f} (difference {diff:+.2f}). The gap does not match "
                    f"a standard processing fee. Action: ask the client to confirm "
                    f"whether this was a partial payment.",
                    expected=order.amount, received=pay.amount))

    for ref, pays in by_ref.items():
        if ref not in known_ids:
            for p in pays:
                findings.append(Finding(
                    ref, "orphan_payment",
                    f"Payment {p.payment_id} ({p.amount:.2f} {p.currency}) references "
                    f"unknown order '{ref}'. Action: match it manually or refund.",
                    expected=None, received=p.amount))
    return findings


def summary(findings: list[Finding]) -> dict:
    out: dict[str, int] = {}
    for f in findings:
        out[f.kind] = out.get(f.kind, 0) + 1
    return out
