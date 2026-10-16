# Demo video script (English, < 3 minutes) — for Nebius / PayPal / Open Agent

Total target: 2:30. Record screen; narration can be read aloud slowly or
generated with TTS — no live Q&A is required for these submissions.

0:00–0:20 — Problem
"Freelancers get paid through scattered channels. Some payments never
arrive, some arrive short, and nobody knows why. Chasing clients for a
difference that turns out to be a processing fee wastes hours."

0:20–0:50 — What it does
"This is Recon Agent. I paste in my orders and my payments. The agent
reconciles them step by step and explains every single result —
not just matched or not matched, but why."

0:50–1:40 — Live demo (open /demo, then a custom /reconcile run)
"Order A1 matched exactly. A2 is 5 dollars 80 short — the agent
recognises the standard processing-fee pattern and tells me to record
the fee instead of chasing the client. A3 is a real partial payment.
A4 never arrived, so the agent proposes a payment link. And this
payment references an order that does not exist — flagged for review."

1:40–2:10 — Sponsor tech (say this explicitly; it is scored)
Nebius version: "The narration layer runs on Nebius Token Factory,
calling NVIDIA's open Nemotron model through its OpenAI-compatible
API at runtime."
PayPal version: "The payment-link action creates a real PayPal
Sandbox checkout; when the client pays, the payment flows back into
the reconciliation automatically."

2:10–2:30 — Close
"One agent, three outcomes: no silent losses, no awkward fee-chasing,
and a bookkeeping report a human can trust because every conclusion
explains itself. Thank you."
