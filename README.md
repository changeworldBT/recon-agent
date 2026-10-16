# Recon Agent — Freelancer Payment Reconciliation Agent

An AI agent that does real bookkeeping work for freelancers and small
sellers: it ingests scattered orders and payments, reconciles them step
by step, **explains why every discrepancy happened**, and proposes the
next action (send a PayPal payment link, review a duplicate, record a
processing fee instead of chasing the client).

## Why this exists
Freelancers lose hours and money to three silent problems: payments
that never arrive, amounts that are quietly short (often just a
processing fee), and duplicate/unknown payments nobody dares to touch.
Recon Agent turns a pile of CSV/API fragments into an explained,
actionable report in seconds.

## How it works
1. **Ingest** — orders/invoices + payments (PayPal Sandbox API, CSV, manual).
2. **Reconcile** — deterministic matching engine classifies each order:
   matched / amount_mismatch / fee_suspected / missing_payment /
   duplicate_payment / currency_mismatch / orphan_payment.
3. **Explain** — every finding ships with a plain-language reason and a
   concrete action. Optional LLM narration via Nebius Token Factory
   (NVIDIA open model) summarises the report.
4. **Act** — proposes payment links / refund reviews; a human approves
   anything money-moving.

## Run it
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# open http://127.0.0.1:8000/demo for a built-in sample report
python -m unittest discover -s tests   # core logic tests, no deps needed
```

## Deploy the demo (for judges)
The demo server is stdlib-only, so it deploys anywhere:
```bash
python3 demo_server.py                 # local: http://127.0.0.1:8000/
PORT=8000 python3 demo_server.py       # PaaS mode: binds 0.0.0.0:$PORT
docker build -t recon-agent . && docker run -e PORT=8000 -p 8000:8000 recon-agent
```
Set `PORT` (hosts usually inject it) and the server listens on all
interfaces; `HOST` overrides the bind address explicitly.

## Optional: Nebius narration
Set `NEBIUS_API_KEY` (Token Factory) and optionally `NEBIUS_MODEL`.
Without a key the agent still works fully on rule-based explanations.

## Optional: PayPal Sandbox payment links
`app/paypal_connector.py` implements the PayPal loop behind the
agent's `create_payment_link` action: OAuth token, Checkout order
(returns the approve/payment link), and converting a COMPLETED order
back into a reconciliation payment. Set `PAYPAL_CLIENT_ID` and
`PAYPAL_CLIENT_SECRET` (Sandbox app from the PayPal Developer
Dashboard). Covered by offline unit tests with a fake HTTP layer;
a live Sandbox round-trip still needs a real developer account.

## Hackathon notes
This single codebase is the submission kernel for: Open Agent
Hackathon (Explain-Why track), Nebius × NVIDIA Global AI Hackathon,
and PayPal AI Hackathon (PayPal Sandbox checkout for the payment-link
action). See `docs/` for per-event checklists. (A Databricks AppQuest
variant was considered and dropped on 2026-10-07; it is not a target.)

## License
MIT
