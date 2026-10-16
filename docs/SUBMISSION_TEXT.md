# Submission copy (English, pre-filled draft)

**Project name:** Recon Agent
**Tagline:** The bookkeeping agent that explains itself — every
reconciliation conclusion comes with its reason and its next action.
**Track:** The Agent That Can Explain Why (also fits Connected Agent Context)

## What it does
Freelancers and small sellers get paid through scattered channels.
Payments arrive late, short, duplicated, or not at all — and existing
tools only say "unmatched". Recon Agent ingests fragmented orders and
payments through tool-style (MCP-shaped) connectors, reconciles them
in multiple steps, and for every order explains *why*: an exact match,
a shortfall that matches a standard processing fee (so you record the
fee instead of awkwardly chasing your client), a genuine partial
payment, a missing payment, a duplicate, a currency mismatch, or a
payment that references a nonexistent order. It then proposes the
concrete next action — payment reminder/link, refund review, manual
match — and never moves money without human approval.

## How it works
1. Connect: tool connectors expose `list_orders` / `list_payments`
   over CSV/API sources in an MCP-shaped interface.
2. Reason: a deterministic matching engine classifies each item;
   fee-pattern detection uses the observed fee rate to distinguish
   "fee" from "underpayment" instead of guessing.
3. Explain: every finding carries evidence, a plain-language reason,
   and an action. An optional LLM narration layer (NVIDIA open model
   via a token factory API) summarises the report for non-accountants.
4. Act: proposed actions are queued for one-click human approval.

## How we built it
Python (standard-library core, zero-dependency reconciliation engine),
FastAPI service layer, MCP-shaped connectors, a labelled evaluation
harness (tests/evaluate.py) scoring classification accuracy across
scenario families, and a full unit-test suite.

## Challenges we ran into
The hard part was not matching amounts — it was *explaining* them.
A 2.9% shortfall and a lazy partial payment look identical until you
model the fee hypothesis and test it against tolerance bands. We also
learned that reasoning models return answers in `reasoning_content`
with empty `content`, and unreliable tool calling — so the agent asks
for JSON in-prompt and parses defensively.

## What we learned / what's next
Explainability is a feature users can feel: "why" turns a report into
a decision. Next: live PayPal/Stripe connectors, multi-currency FX
explanation, and a memory layer that learns each client's payment
habits across months.
