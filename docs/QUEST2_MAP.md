# Quest 2 答卷草稿 — Apps / Lakebase / Agent Bricks / Lakehouse 如何衔接

一句话版：Lakehouse 是数据与治理的底座，Lakebase 是给应用用的
在线事务数据库（Postgres），Databricks Apps 是把应用跑起来并托管
的运行时，Agent Bricks 是在同一平台上给应用加 AI 能力的组件；
AppKit 把鉴权、缓存、可观测和对 SQL Warehouse / 模型服务 /
Lakebase 的连接都预先接好，开发者只写业务。

## 关系图（文字版）
用户 → Databricks App（AppKit 运行时：鉴权/缓存/日志）
        ├─ 读在线业务数据 → Lakebase Postgres（OLTP，低延迟 CRUD）
        ├─ 分析查询/历史数据 → SQL Warehouse → Lakehouse
        │     （Delta Lake + Unity Catalog 治理：表、权限、血缘）
        └─ AI 能力 → Agent Bricks / Model Serving
              （RAG 检索知识来自 Lakehouse/Lakebase 中的文档与数据，
               推理结果回写 Lakebase 供应用展示）

## 落到我们的对账项目
- 订单/付款的在线增删改查 → Lakebase
- 对账报告与历史账单的分析、RAG 知识库文档 → Lakehouse 表 + Unity Catalog 管理
- 前端+后端应用托管 → Databricks Apps（Quest 4 部署的正是这一层）
- “解释每笔差异”的智能问答助手 → Agent Bricks（Quest 5 加在这一层）
