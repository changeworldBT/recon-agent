import sys, unittest
sys.path.insert(0, __file__.rsplit("/tests/", 1)[0])
from app.reconcile import Order, Payment, reconcile, summary


class TestReconcile(unittest.TestCase):
    def setUp(self):
        self.orders = [
            Order("A1", "Client X", 100.00),
            Order("A2", "Client Y", 200.00),
            Order("A3", "Client Z", 103.00),
            Order("A4", "Client W", 50.00),
        ]
        self.payments = [
            Payment("P1", "A1", 100.00),          # exact match
            Payment("P2", "A2", 194.20),          # 200 - 2.9% fee = 194.20
            Payment("P3", "A3", 60.00),           # partial / mismatch
            Payment("P4", "A9", 10.00),           # orphan
            # A4: no payment -> missing
        ]
        self.findings = {f.order_id: f for f in reconcile(self.orders, self.payments)}

    def test_matched(self):
        self.assertEqual(self.findings["A1"].kind, "matched")

    def test_fee_suspected(self):
        self.assertEqual(self.findings["A2"].kind, "fee_suspected")

    def test_amount_mismatch(self):
        self.assertEqual(self.findings["A3"].kind, "amount_mismatch")

    def test_missing(self):
        self.assertEqual(self.findings["A4"].kind, "missing_payment")

    def test_orphan(self):
        self.assertEqual(self.findings["A9"].kind, "orphan_payment")

    def test_every_finding_explains_why(self):
        for f in self.findings.values():
            self.assertTrue(len(f.explanation) > 30)


if __name__ == "__main__":
    unittest.main()
