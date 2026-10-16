"""HTTP entry point (FastAPI). Run: uvicorn app.main:app --reload
Demo data is built in so the deployed demo works with zero setup.
"""
from fastapi import FastAPI
from pydantic import BaseModel

from .agent import run_agent, narrate_with_nebius
from .reconcile import Order, Payment

app = FastAPI(title="Recon Agent — freelancer payment reconciliation")


class OrderIn(BaseModel):
    order_id: str
    client: str
    amount: float
    currency: str = "USD"


class PaymentIn(BaseModel):
    payment_id: str
    order_ref: str
    amount: float
    currency: str = "USD"
    source: str = "paypal_sandbox"


class ReconIn(BaseModel):
    orders: list[OrderIn]
    payments: list[PaymentIn]


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/reconcile")
def do_reconcile(body: ReconIn):
    report = run_agent(
        [Order(**o.model_dump()) for o in body.orders],
        [Payment(**p.model_dump()) for p in body.payments])
    narration = narrate_with_nebius(report)
    if narration:
        report["narration"] = narration
    return report


@app.get("/demo")
def demo():
    orders = [Order("A1", "Client X", 100.00), Order("A2", "Client Y", 200.00),
              Order("A3", "Client Z", 103.00), Order("A4", "Client W", 50.00)]
    payments = [Payment("P1", "A1", 100.00), Payment("P2", "A2", 194.20),
                Payment("P3", "A3", 60.00), Payment("P4", "A9", 10.00)]
    return run_agent(orders, payments)
