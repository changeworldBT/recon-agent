"""Offline tests for the PayPal Sandbox connector (fake HTTP opener)."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.paypal_connector import PayPalNotConfigured, PayPalSandboxClient
from app.reconcile import Order


class FakeResponse:
    def __init__(self, payload):
        self._body = json.dumps(payload).encode()

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class FakePayPal:
    """Records requests; answers like the Sandbox token + orders APIs."""

    def __init__(self):
        self.requests = []
        self.order_status = "COMPLETED"

    def __call__(self, req, timeout=None):
        self.requests.append(req)
        url = req.full_url
        if url.endswith("/v1/oauth2/token"):
            assert req.get_header("Authorization", "").startswith("Basic ")
            return FakeResponse({"access_token": "tok-123", "expires_in": 3600})
        if url.endswith("/v2/checkout/orders") and req.method == "POST":
            assert req.get_header("Authorization") == "Bearer tok-123"
            body = json.loads(req.data)
            assert body["intent"] == "CAPTURE"
            assert body["purchase_units"][0]["reference_id"] == "A9"
            return FakeResponse({
                "id": "PP-ORDER-1", "status": "CREATED",
                "links": [
                    {"rel": "self", "href": "https://api-m.sandbox.paypal.com/x"},
                    {"rel": "approve",
                     "href": "https://www.sandbox.paypal.com/checkoutnow?token=PP-ORDER-1"},
                ]})
        if "/v2/checkout/orders/PP-ORDER-1" in url:
            return FakeResponse({
                "id": "PP-ORDER-1", "status": self.order_status,
                "purchase_units": [{
                    "reference_id": "A9",
                    "amount": {"currency_code": "USD", "value": "75.00"},
                    "payments": {"captures": [{
                        "id": "CAP-1",
                        "amount": {"currency_code": "USD", "value": "75.00"}}]},
                }]})
        raise AssertionError(f"unexpected request {req.method} {url}")


class PayPalConnectorTests(unittest.TestCase):
    def setUp(self):
        self.fake = FakePayPal()
        self.client = PayPalSandboxClient("cid", "secret", opener=self.fake)

    def test_missing_credentials_raise_clear_error(self):
        client = PayPalSandboxClient("", "", opener=self.fake)
        with self.assertRaises(PayPalNotConfigured):
            client.access_token()

    def test_create_payment_link_returns_approve_url(self):
        out = self.client.create_payment_link(
            Order("A9", "Client Q", 75.0),
            "https://example.com/ok", "https://example.com/cancel")
        self.assertEqual(out["order_id"], "PP-ORDER-1")
        self.assertEqual(out["status"], "CREATED")
        self.assertIn("checkoutnow?token=PP-ORDER-1", out["approve_url"])
        # token fetched once, then reused from cache
        token_calls = [r for r in self.fake.requests
                       if r.full_url.endswith("/v1/oauth2/token")]
        self.assertEqual(len(token_calls), 1)

    def test_completed_order_becomes_payment(self):
        pay = self.client.payment_from_order("PP-ORDER-1")
        self.assertIsNotNone(pay)
        self.assertEqual(pay.payment_id, "CAP-1")
        self.assertEqual(pay.order_ref, "A9")
        self.assertEqual(pay.amount, 75.0)
        self.assertEqual(pay.source, "paypal_sandbox")

    def test_uncompleted_order_is_none_not_error(self):
        self.fake.order_status = "APPROVED"
        self.assertIsNone(self.client.payment_from_order("PP-ORDER-1"))


if __name__ == "__main__":
    unittest.main()
