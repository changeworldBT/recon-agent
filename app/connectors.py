"""Data connectors — MCP-style tool interface for the agent.

Each connector exposes `tools()` (name, description, JSON-schema-ish
params) and `call(name, args)`, mirroring the Model Context Protocol
shape so the agent can treat orders/payments sources as tools:
local CSV files today; PayPal Sandbox and Lakebase plug in behind the
same interface for the other hackathon variants.
"""
from __future__ import annotations

import csv
import io

from .reconcile import Order, Payment


class CsvConnector:
    name = "local_csv"

    def __init__(self, orders_csv: str = "", payments_csv: str = ""):
        self._orders_csv = orders_csv
        self._payments_csv = payments_csv

    def tools(self) -> list[dict]:
        return [
            {"name": "list_orders", "description": "List expected orders/invoices",
             "params": {}},
            {"name": "list_payments", "description": "List received payments",
             "params": {}},
        ]

    def call(self, name: str, args: dict | None = None):
        if name == "list_orders":
            return [Order(r["order_id"], r["client"], float(r["amount"]),
                          r.get("currency", "USD"))
                    for r in csv.DictReader(io.StringIO(self._orders_csv))]
        if name == "list_payments":
            return [Payment(r["payment_id"], r["order_ref"], float(r["amount"]),
                            r.get("currency", "USD"), r.get("source", "manual"))
                    for r in csv.DictReader(io.StringIO(self._payments_csv))]
        raise ValueError(f"unknown tool {name}")


def load_all(connector: CsvConnector):
    orders = connector.call("list_orders")
    payments = connector.call("list_payments")
    return orders, payments
