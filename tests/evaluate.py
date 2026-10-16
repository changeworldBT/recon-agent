"""Evaluation harness — runs the agent against labelled scenarios and
reports classification accuracy. Ships as the 'evaluations' artefact
for Open Agent bonus points and as a regression gate for all variants.
Run: python -m tests.evaluate
"""
import sys
sys.path.insert(0, __file__.rsplit("/tests/", 1)[0])

from app.agent import run_agent
from app.reconcile import Order, Payment

SCENARIOS = [
    # (orders, payments, expected kinds by order_id)
    ([Order("S1", "A", 100)], [Payment("x", "S1", 100)], {"S1": "matched"}),
    ([Order("S2", "B", 200)], [Payment("x", "S2", 194.20)], {"S2": "fee_suspected"}),
    ([Order("S3", "C", 80)], [], {"S3": "missing_payment"}),
    ([Order("S4", "D", 50)], [Payment("x", "S4", 20)], {"S4": "amount_mismatch"}),
    ([Order("S5", "E", 60)], [Payment("x", "S5", 60), Payment("y", "S5", 60)],
     {"S5": "duplicate_payment"}),
    ([Order("S6", "F", 70)], [Payment("x", "ZZ", 70)], {"S6": "missing_payment", "ZZ": "orphan_payment"}),
    ([Order("S7", "G", 90, "USD")], [Payment("x", "S7", 90, "EUR")], {"S7": "currency_mismatch"}),
    ([Order("S8", "H", 500)], [Payment("x", "S8", 485.50)], {"S8": "fee_suspected"}),
    ([Order("S9", "I", 30)], [Payment("x", "S9", 45)], {"S9": "amount_mismatch"}),
    ([Order("S10", "J", 120, "EUR")], [Payment("x", "S10", 120, "EUR")], {"S10": "matched"}),
    ([Order("S11", "K", 1000)], [Payment("x", "S11", 900)], {"S11": "amount_mismatch"}),
    ([Order("S12", "L", 75)], [Payment("x", "S12", 75), Payment("y", "XX", 5)],
     {"S12": "matched", "XX": "orphan_payment"}),
]


def main() -> int:
    total = correct = 0
    for orders, payments, expected in SCENARIOS:
        report = run_agent(orders, payments)
        got = {f["order_id"]: f["kind"] for f in report["findings"]}
        for oid, kind in expected.items():
            total += 1
            ok = got.get(oid) == kind
            correct += ok
            print(f"{'PASS' if ok else 'FAIL'} {oid}: expected {kind}, got {got.get(oid)}")
    print(f"\naccuracy: {correct}/{total} = {correct/total:.0%}")
    return 0 if correct == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
