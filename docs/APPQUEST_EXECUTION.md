# Databricks AppQuest 执行单（核实于 2026-10-07）

## ✅ 已确认的好消息
- 资格地区包含 **Hong Kong (SAR)**，你符合地区要求。
- 要建 4 个账号（可同一邮箱）：Databricks Free Edition、AngelHack (earn.angelhack.com)、Databricks Customer Academy、Databricks Community（亚太社区加入需审批，可能要等）。
- 评审两批：11月2日前完成 → 11月评审；12月31日前完成 → 2027年1月评审。目标赶第一批。
- $20 是完成全部 5 个 Quest 的总奖励（各 Quest 有各自小额，如 Quest 4 页面显示 $3），另有 Graduate 徽章；Quest 5 自定义优秀者争 $750 培训券（数量有限）。

## ⚠️ 领钱的硬条件（官方原文大意）
可以用个人邮箱注册，**但只有在 Quest 1 提供有效公司邮箱（company email）并申报公司名称的提交，才有资格进入评审和拿奖励。**
- 你目前是离职/待业状态，没有在职公司邮箱；前公司（杭州宇为）的邮箱不应再使用。
- 因此先向官方 support（见活动页公布的支持邮箱）书面确认以下口径，再决定是否投入：
  1. 独立/自由职业开发者（self-employed / freelancer）能否以自有域名邮箱 + 自报个体名称申报？
  2. 若不行，个人邮箱完成全部 Quest 是否只发徽章、不发 $20？
- 询问邮件草稿在本文件末尾，须经你批准后才发送（按你的邮件规则）。

## 五个 Quest 的具体交付物（已核实部分）
- Quest 1：建 Databricks 账号 + 加入社区；在此填写公司邮箱 + 公司名（领钱条件在此关）
- Quest 2：理清 Apps / Lakebase / Agent Bricks / Lakehouse 的关系（概念图答卷见 docs/QUEST2_MAP.md，已备）
- Quest 3：装 CLI + 认证 workspace + 给编码 Agent 加载 skills
  - 本机已装好 Databricks CLI v1.19.0 并验证版本（Quest 3 的安装步已预演）；认证需你的 workspace 地址，登录后在本机/你电脑执行 `databricks auth login`
- Quest 4：用 `databricks apps init` 的 App-with-Lakebase 模板脚手架 → 开 Lakebase Postgres → 部署 App
  - 交付物（官方）：1) 你在 Databricks Community 发帖的截图 2) 已部署应用的截图
  - Lakebase 实例要保留给 Quest 5，别关
- Quest 5：在 Quest 4 的 App 上加 RAG 助手（用我们的对账报告/文档做知识库）+ 录 demo

## 建议节奏（赶 11月2日第一批）
- 本周：你建 4 个账号 + 我发 support 问清公司邮箱口径（并行，不等回复先做 Quest 2/3）
- 账号齐后 2–3 天：Quest 1–3 提交物做完
- 随后 3–4 天：Quest 4 部署 + 社区发帖截图
- 再 3–4 天：Quest 5 RAG + demo，10月底前全部交完

---

## 附：给 AngelHack Support 的询问邮件草稿（未发送，等你批准）
收件人：活动页公布的 AppQuest 支持邮箱
主题：AppQuest eligibility question — company email requirement for an independent developer

Body:
Hello AppQuest team,

I am an independent / freelance software developer based in Hong Kong
(an eligible region). I am currently between jobs and do not have an
employer-issued company email address.

Your campaign page says only submissions from participants who provide
a valid company email address and declare their company name in
Quest 1 are eligible for review and rewards.

Could you please confirm:
1. May a self-employed developer declare their own freelance practice
   name and use an email address on a domain they personally own?
2. If not, can a participant using only a personal email still earn
   the US$20 completion reward and the Graduate badge?

Thank you very much.
Heng Yu (Hong Kong)
