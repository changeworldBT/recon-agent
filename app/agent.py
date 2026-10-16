"""Multi-step reconciliation agent.

Steps: ingest -> reconcile -> explain -> propose actions.
The reasoning layer is pluggable:
- default: deterministic rule-based explanations (reconcile.py) — always works offline
- optional: Nebius Token Factory (OpenAI-compatible) with an NVIDIA open
  model (e.g. Nemotron) to narrate explanations. NOTE for Nebius reasoning
  models: the answer may arrive in `reasoning_content` while `content` is
  empty, and tool/function calling is unreliable — ask for JSON in the
  prompt and parse it.
"""
from __future__ import annotations

import json
import os
import urllib.request

from .reconcile import Order, Payment, reconcile, summary


def run_agent(orders: list[Order], payments: list[Payment]) -> dict:
    findings = reconcile(orders, payments)
    actions = []
    for f in findings:
        if f.kind == "missing_payment":
            actions.append({"order_id": f.order_id, "action": "create_payment_link",
                            "note": "Generate a PayPal payment link and send a reminder."})
        elif f.kind == "duplicate_payment":
            actions.append({"order_id": f.order_id, "action": "review_refund",
                            "note": "Human review before refunding the duplicate."})
        elif f.kind == "orphan_payment":
            actions.append({"order_id": f.order_id, "action": "manual_match",
                            "note": "Ask the owner to match or refund this payment."})
    return {
        "findings": [f.__dict__ for f in findings],
        "summary": summary(findings),
        "proposed_actions": actions,
    }


def narrate_with_nebius(report: dict) -> str | None:
    """Optional narration via Nebius Token Factory. Returns None if unconfigured."""
    key = os.environ.get("NEBIUS_API_KEY")
    if not key:
        return None
    model = os.environ.get("NEBIUS_MODEL", "nvidia/nemotron-3-nano-30b-a3b")
    prompt = (
        "You are a bookkeeping assistant. In under 150 words, summarise this "
        "reconciliation report for a freelancer and list the single most urgent "
        "action. Reply with plain text only.\n" + json.dumps(report)[:4000]
    )
    body = json.dumps({"model": model,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(
        "https://api.tokenfactory.nebius.com/v1/chat/completions",
        data=body, method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
    msg = data["choices"][0]["message"]
    return (msg.get("content") or msg.get("reasoning_content") or "").strip() or None
