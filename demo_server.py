"""Zero-dependency demo server: python3 demo_server.py [port]
Serves a one-page explanation-trace UI over the built-in demo data,
so the project can be demoed/deployed anywhere without installing
FastAPI. The production entry point remains app/main.py.

Deployment: set PORT (and optionally HOST=0.0.0.0) in the environment
— most PaaS hosts inject PORT and expect the app to listen on all
interfaces. Locally both default to 127.0.0.1:8000, and an explicit
command-line port still wins over $PORT.
"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from app.agent import run_agent
from app.reconcile import Order, Payment

DEMO_ORDERS = [Order("A1", "Client X", 100.00), Order("A2", "Client Y", 200.00),
               Order("A3", "Client Z", 103.00), Order("A4", "Client W", 50.00)]
DEMO_PAYMENTS = [Payment("P1", "A1", 100.00), Payment("P2", "A2", 194.20),
                 Payment("P3", "A3", 60.00), Payment("P4", "A9", 10.00)]

PAGE = """<!doctype html><meta charset="utf-8"><title>Recon Agent — demo</title>
<style>body{font-family:system-ui;max-width:820px;margin:2rem auto;padding:0 1rem}
.f{border:1px solid #ddd;border-radius:8px;padding:1rem;margin:.6rem 0}
.k{font-weight:700}.matched{border-color:#2e7d32}.fee_suspected{border-color:#ed6c02}
.missing_payment,.orphan_payment{border-color:#c62828}</style>
<h1>Recon Agent — explanation trace</h1>
<p>Every conclusion shows its reason and its next action.</p>
<div id="app">loading…</div>
<script>fetch('/api/demo').then(r=>r.json()).then(d=>{
document.getElementById('app').innerHTML =
 '<p><b>Summary:</b> '+JSON.stringify(d.summary)+'</p>' +
 d.findings.map(f=>`<div class="f ${f.kind}"><span class="k">${f.order_id} — ${f.kind}</span><br>${f.explanation}</div>`).join('') +
 '<h3>Proposed actions (human approval required)</h3>' +
 d.proposed_actions.map(a=>`<div class="f">${a.order_id}: <b>${a.action}</b> — ${a.note}</div>`).join('');
})</script>"""


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/demo":
            body = json.dumps(run_agent(DEMO_ORDERS, DEMO_PAYMENTS)).encode()
            ctype = "application/json"
        else:
            body = PAGE.encode()
            ctype = "text/html; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", "8000"))
    # A $PORT in the environment is the PaaS signal: listen on all
    # interfaces there; stay on localhost for plain local runs.
    host = os.environ.get("HOST", "0.0.0.0" if "PORT" in os.environ else "127.0.0.1")
    print(f"demo at http://{host}:{port}/", flush=True)
    HTTPServer((host, port), H).serve_forever()
