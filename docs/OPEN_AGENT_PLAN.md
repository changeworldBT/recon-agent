# Open Agent Hackathon 2026 — 执行计划（核实 2026-10-07）

## ✅ 2026-10-10 复核：两个官方页面已收敛到新口径
- 2026-10-10 本次实查 Academy 课程页，其 Schedule 段已改为「建造窗口 10月22–27日」，不再是 10月15–20日的旧口径。
- 同日实查赛事平台 hackathon.genai.works 赛事页「6 dates that matter」：报名 10月22日 23:59 UTC 截止（Hard deadline，北京时间 10月23日 07:59）、建造 10月22日开启、提交 10月27日 23:45 UTC 截止、结果 11月6日 16:00 UTC。
- 结论：10月13日不再是硬约束；但官方 LinkedIn 帖曾写报名 10月20日截止，故执行口径改为「10月20日前完成注册」即覆盖全部已知口径。逐日计划中 10月14–20日「备好可提交版」的节点保留（提前备好无损失），10月22–27日按新口径做赞助技术集成与终稿提交。

## ⚠ 日期冲突：采取双保险排期（2026-10-07 15:48 CST 再复核）【历史记录 — 已被上方 2026-10-10 复核结论取代，本节的「10月13日前注册」双保险口径不再执行，现行口径只有上方一条：10月20日前注册、硬截止 10月22日】
- Academy 课程页（2026-10-07 实查）仍显示：活动期 10月15–20日、workshop 10月7/8/12日、onboarding 10月14日一类的旧口径。
- 赛事平台 hackathon.genai.works 的实时赛事页（2026-10-07 实查）显示更新口径：建造窗口 10月22–27日；报名于 10月22日 23:59 UTC 截止；提交于 10月27日 23:45 UTC 截止；结果 11月6日 16:00 UTC 公布。Zetaris 2026-10-06 新闻稿的 10月22–27日口径与赛事平台一致。
- 两个官方入口尚未同步，不能断言旧口径已作废。执行上双保险：**10月13日前完成能完成的注册/报名动作**，同时在 10月20日前备好可提交版本；若新口径最终确认，再用 10月22–27日做赞助技术集成和终稿提交。
- 赛事平台当前赛道为 Solving Fragmented Intelligence / The Agent That Can Explain Why / Reasoning Architecture + Wildcard，并明确“Pick one track”。本项目仍选 **The Agent That Can Explain Why** 单赛道，不再把 Connected Agent Context / Autonomous Agent 写成现行赛道。

## 时间线（双口径并列）
- Academy 旧口径：报名截止 10月13日；建造 10月15–20日；提交 10月20日 23:45 UTC；结果 10月30日。
- 赛事平台新口径：建造 10月22–27日；报名截止 10月22日 23:59 UTC（北京时间 10月23日 07:59）；提交 10月27日 23:45 UTC（北京时间 10月28日 07:45）；结果 11月6日 16:00 UTC（北京时间 11月7日 00:00）。
- 直播 workshop：Academy 口径为 10月7、8、12日，均有录播可回看；新口径下的 workshop/onboarding 时间注册后以赛事平台/Discord 为准。

## 赛道与打法
- 主赛道：The Agent That Can Explain Why（我们的每条对账结论都带原因+依据+动作）
- 副赛道靠拢：Connected Agent Context（通过 MCP 形态工具连接碎片订单/付款数据）
- 赞助技术：尽量实际用上三层中的至少两层——Zetaris/MCP 式数据连接、NVIDIA token 层做叙事推理；Meterless 若接入成本高，至少在架构文档中说明编排步骤

## 评分（满分100+加分，官方口径）
Impact 30｜Technical 20｜Innovation 15｜Demo / Product & UX / Sponsor tech 各 10
加分（最高 +30）：开源代码、提交 evaluations、记录 insights —— 三项我们都做：
- 开源：GitHub 公开仓库 + MIT（等用户 GitHub 发布）
- Evaluations：tests/evaluate.py 已跑通 14/14 检查（2026-10-09 复测）
- Insights：docs/INSIGHTS.md 已备草稿

## 逐日计划（双保险版）
- 10月7–13日：用户完成能完成的官网/赛事注册；看完三场 workshop 录播；项目骨架已就绪（对账引擎+Agent+MCP式连接器+评测，评测现为 12 个场景、14/14 检查通过）
- 10月14–20日：按旧口径推进到“可提交版”：数据接入层定版（CSV + 示例数据包）、解释链路页面、动作层的人工确认环节、部署 demo、录演示、README 与 insights 定版；若旧口径有效，10月20日上午提交。
- 10月21日：核对赛事平台/Discord 的最终口径与提交入口，冻结 Nebius 迁移所需的核心接口。
- 10月22–26日（若新口径有效）：只做赛事平台要求的赞助技术集成（优先 Zetaris/Meterless 的可验证接入）和按新赛道文案终修，不重写对账内核；10月26日完成终稿。
- 10月27日：上午提交新口径终稿，下午留作缓冲复查，绝不卡 23:45 UTC。

## 用户注册步骤（只需这一步，其余我做）
1. 打开 https://academy.genai.works/courses/open-agent-hackathon-2026/details
2. 注册 GenAI Works Academy 账号（邮箱注册即可）并 Enroll / Register 本赛事
3. 按页面指引进 Discord 社区（公告和组队都在那里）
4. 注册成功后回主聊天说一声“Open Agent 注册好了”，并把账号用的邮箱告诉我（只记邮箱，不记密码）
