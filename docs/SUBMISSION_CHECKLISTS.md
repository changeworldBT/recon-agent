# Per-event submission checklists (verified 2026-10-07)

## 1. Open Agent Hackathon — schedule converged (re-checked 2026-10-10)
- Both official pages now agree on the updated schedule: build Oct 22–27, registration closes Oct 22 23:59 UTC (hard deadline), submissions close Oct 27 23:45 UTC, results Nov 6 16:00 UTC. The earlier Academy schedule (register by Oct 13, build Oct 15–20) no longer appears on the Academy page as of 2026-10-10.
- Only remaining outlier: an official LinkedIn post once said registration closes Oct 20 — so the execution target stays "register by Oct 20", which covers every known version.
- [ ] USER: complete registration by Oct 20 (safe under all versions); after registering, verify the final schedule/submission入口 in the event platform or Discord.
- [ ] Academy workshops: the current Academy page describes three live workshops plus an onboarding call before kickoff, recorded and available on demand, and no longer lists a specific Oct 12 live date in its schedule text (checked 2026-10-10) — watch the recordings and do the Start Here setup guide instead of planning around an Oct 12 live session; confirm any live times inside the platform/Discord after registering.
- [ ] Track: pick ONE — The Agent That Can Explain Why.
- [ ] Build: recon-agent + MCP-style data connectors + explanation trace page; have a submittable version ready by Oct 20, then use Oct 22–26 for verified sponsor-tech integration if the updated schedule controls.
- [ ] Bonus/evidence: open-source repo, evaluations (currently 12 scenarios, 14/14 checks), documented insights.
- [ ] Submit the final version before Oct 27 23:45 UTC (Beijing Oct 28 07:45); aim to finish Oct 26, keeping Oct 27 as buffer only.

## 2. Nebius × NVIDIA — submit by Oct 30, 10:00 PDT (Oct 31 01:00 CST)
- [ ] USER: Devpost account + register on nebiusglobalaihackathon.devpost.com
- [ ] USER/ASSIST: claim Token Factory credits from Resources page — up to $50 total: the first $25 plus another $25 for free joining of the Builders Program (verified 2026-10-11); claim both, create Nebius account + API key
- [ ] Runtime must actually call Token Factory inference API with ≥1 NVIDIA open model (Nemotron via app/agent.py narrate_with_nebius)
- [ ] Track: Best Apps & Agents (fallback: Coding & Agentic Engineering)
- [ ] Public GitHub repo + MIT license + README setup/run instructions (repo prepared locally at ~/workspace/recon-agent — needs USER's GitHub to publish)
- [ ] Working demo URL deployed and kept free/accessible through judging Dec 1–15
- [ ] YouTube demo video < 3 min, public, narrates sponsor-tech usage (English script in docs/DEMO_SCRIPT_EN.md)
- [ ] Devpost text description + track choice + Token Factory/NVIDIA feedback form

## 3. PayPal AI Hackathon — submit by Nov 12, 14:00 PST (Nov 13 ~06:00 CST)
- [ ] USER: Devpost account (same as Nebius) + PayPal Developer account, create Sandbox app, note client id/secret (keep in vault, not in repo)
- [ ] Integrate PayPal Sandbox checkout for the "create_payment_link" action; webhook or return-URL updates payment status -> feeds reconciliation — CODE READY 2026-10-10: app/paypal_connector.py (OAuth + Checkout order/approve link + COMPLETED order -> Payment), offline tests 4/4 in tests/test_paypal_connector.py; remaining is a live Sandbox round-trip with the USER's developer-account credentials
- [ ] AI must be in the core experience: reconciliation explanations + narration
- [ ] Working prototype URL + Devpost submission (video recommended)
- [ ] Existing projects allowed only with meaningful updates during the period — our PayPal layer is built in-period, document that in the submission

## 4. Databricks AppQuest — SKIPPED (user decision 2026-10-07; archive only, do not execute)
Skipped because the $20 completion reward requires a valid company email + declared company name in Quest 1, which the user (between jobs) does not have; eligibility unconfirmed. Not in the sprint schedule. The checklist below is kept only as a historical record.
- [ ] USER: register via AngelHack entry (dbricks.info/db-appquest-blog), create Databricks account (Quest 1)
- [ ] Quest 2: architecture map doc (Apps / Lakebase / Agent Bricks / Lakehouse) — draft from README diagram
- [ ] Quest 3: install Databricks CLI, authenticate workspace, load agent skills
- [ ] Quest 4: scaffold app from DevHub template, deploy with Lakebase backend (port recon data model)
- [ ] Quest 5: add RAG assistant over reconciliation reports/documents; record demo
- [ ] $20 completion reward is per finishing participant; $750 training voucher is competitive on Quest 5 customisation

## 5. 鲸锐 AI 创作大赛 — submit by Nov 22 (separate, non-coding)
- [ ] USER: register on the contest site or via Youku search “鲸锐AI创作大赛”
- [ ] Story elaboration ≥1000 chars: draft ready at goals files/鲸锐故事阐述草稿.md
- [ ] AI short film ≥10 min, original, premiere in this contest, no existing IP
- [ ] Decide go/no-go on full production by ~Nov 8 based on coding-hackathon progress
