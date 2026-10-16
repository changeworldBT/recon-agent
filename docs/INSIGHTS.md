# Insights — building an agent that explains why

Documented for the Open Agent Hackathon bonus criteria, and kept as
the project's public lab notebook.

## Insight 1: Deterministic core, LLM at the edges
We kept classification deterministic and testable, and used the LLM
only for narration. Result: evaluations are reproducible (14/14
labelled checks across 12 scenarios), and the demo never depends on a model being "in a good
mood". Agents that do real work need a spine you can unit-test.

## Insight 2: "Why" is a data model, not a paragraph
Every finding stores kind + evidence + expected/received amounts +
explanation + proposed action. Because the explanation is structured,
the UI, the narration prompt, and the evaluation harness all consume
the same object — no re-interpretation drift between layers.

## Insight 3: Fee-vs-underpayment is a hypothesis test
A shortfall is classified as a fee only if it sits within a tolerance
band around the platform's fee rate; otherwise it stays an honest
"amount mismatch". Naming the hypothesis explicitly made the agent's
explanations shorter and more trustworthy.

## Insight 4: Tool-shaped connectors beat bespoke imports
Framing each data source as tools (`list_orders`, `list_payments`)
in an MCP shape meant the PayPal and database variants slotted in
without touching the reasoning core. The connector contract, not the
source, is the integration surface.

## Insight 5: Evaluations first, features second
Writing labelled scenarios before polishing the UI caught two
classification edge cases (duplicate payments, orphan payments) that
a demo script alone would never have surfaced.
