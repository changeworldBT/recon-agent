"""PayPal Sandbox connector — behind the same shape as connectors.py.

Implements the PayPal AI Hackathon loop for the agent's
`create_payment_link` proposed action:

  1. OAuth2 client-credentials token (Sandbox)
  2. Create a Checkout order for a missing payment -> approve link
     (this is the "payment link" the freelancer sends the client)
  3. Read the order back after approval/capture and convert a
     COMPLETED order into a reconcile.Payment(source="paypal_sandbox"),
     so the payment feeds straight back into reconciliation.

Credentials come only from the environment (PAYPAL_CLIENT_ID /
PAYPAL_CLIENT_SECRET); nothing is stored in the repo. The HTTP layer
is injectable (`opener`, same call shape as urllib.request.urlopen)
so the whole flow is unit-testable offline with a fake opener.

NOT yet verified against the real Sandbox — that needs the user's own
PayPal Developer account (client id/secret), created on their device.
"""
from __future__ import annotations

import base64
import json
import os
import urllib.parse
import urllib.request

from .reconcile import Order, Payment

SANDBOX_BASE = "https://api-m.sandbox.paypal.com"
LIVE_BASE = "https://api-m.paypal.com"


class PayPalNotConfigured(RuntimeError):
    """Raised when PAYPAL_CLIENT_ID / PAYPAL_CLIENT_SECRET are missing."""


class PayPalSandboxClient:
    name = "paypal_sandbox"

    def __init__(self, client_id: str | None = None,
                 client_secret: str | None = None,
                 base_url: str = SANDBOX_BASE, opener=None):
        self.client_id = client_id or os.environ.get("PAYPAL_CLIENT_ID", "")
        self.client_secret = client_secret or os.environ.get("PAYPAL_CLIENT_SECRET", "")
        self.base_url = base_url.rstrip("/")
        self._opener = opener or urllib.request.urlopen
        self._token: str | None = None

    # -- low level ------------------------------------------------------
    def _require_credentials(self):
        if not self.client_id or not self.client_secret:
            raise PayPalNotConfigured(
                "Set PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET (PayPal "
                "Developer Dashboard -> Sandbox app) before calling PayPal.")

    def _request(self, method: str, path: str, body=None, headers=None):
        data = None
        hdrs = {"Content-Type": "application/json"}
        if isinstance(body, dict):
            data = json.dumps(body).encode()
        elif isinstance(body, (bytes, str)):
            data = body.encode() if isinstance(body, str) else body
        if headers:
            hdrs.update(headers)
        req = urllib.request.Request(self.base_url + path, data=data,
                                     method=method, headers=hdrs)
        with self._opener(req, timeout=30) as resp:
            return json.loads(resp.read() or b"{}")

    # -- OAuth ----------------------------------------------------------
    def access_token(self) -> str:
        self._require_credentials()
        if self._token:
            return self._token
        basic = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()).decode()
        data = self._request(
            "POST", "/v1/oauth2/token",
            body=urllib.parse.urlencode({"grant_type": "client_credentials"}),
            headers={"Authorization": f"Basic {basic}",
                     "Content-Type": "application/x-www-form-urlencoded"})
        self._token = data["access_token"]
        return self._token

    def _auth(self) -> dict:
        return {"Authorization": f"Bearer {self.access_token()}"}

    # -- Checkout orders --------------------------------------------------
    def create_payment_link(self, order: Order, return_url: str,
                            cancel_url: str) -> dict:
        """Create a Checkout order; return {order_id, status, approve_url}."""
        body = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "reference_id": order.order_id,
                "description": f"Payment for order {order.order_id} ({order.client})",
                "amount": {"currency_code": order.currency,
                           "value": f"{order.amount:.2f}"},
            }],
            "application_context": {"return_url": return_url,
                                    "cancel_url": cancel_url},
        }
        data = self._request("POST", "/v2/checkout/orders", body=body,
                             headers=self._auth())
        approve = next((link["href"] for link in data.get("links", [])
                        if link.get("rel") == "approve"), None)
        return {"order_id": data["id"], "status": data.get("status"),
                "approve_url": approve}

    def get_order(self, paypal_order_id: str) -> dict:
        return self._request("GET", f"/v2/checkout/orders/{paypal_order_id}",
                             headers=self._auth())

    def payment_from_order(self, paypal_order_id: str) -> Payment | None:
        """Convert a COMPLETED Checkout order into a reconciliation Payment.

        Returns None while the order is not completed (created/approved
        but not captured), so callers can poll without special-casing.
        """
        data = self.get_order(paypal_order_id)
        if data.get("status") != "COMPLETED":
            return None
        unit = (data.get("purchase_units") or [{}])[0]
        amount = (unit.get("amount") or {})
        capture_id = paypal_order_id
        payments = unit.get("payments") or {}
        captures = payments.get("captures") or []
        if captures:
            capture_id = captures[0].get("id", paypal_order_id)
            amount = captures[0].get("amount") or amount
        return Payment(payment_id=capture_id,
                       order_ref=unit.get("reference_id", ""),
                       amount=float(amount.get("value", 0)),
                       currency=amount.get("currency_code", "USD"),
                       source="paypal_sandbox")
