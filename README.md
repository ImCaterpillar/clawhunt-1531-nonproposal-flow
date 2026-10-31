# 非提案业务试点 — 公司级差旅审批流（知识/编排/审批/评测）

对应 ClawHunt 任务 **#1531**（企业 Agent 系统 44/50｜非提案业务试点）。

**验收标准**：交付**完整输入、证据、结果及验收记录**。

## 一条命令验证全部

```bash
python run_tests.py      # -> PASS 11 / FAIL 0
python demo.py           # -> 非提案流程演示
```

## 验收三要素（与验收标准逐条对应）

**① 核心实现路径**
`business_flow.py` —— `BusinessFlowRunner`：按配置执行业务流程，
输出 `{input, evidence[], result, acceptance}` 四要素。
`configs/flow-travel-approval-01.json` —— 差旅审批流配置（6 步：
收集/知识校验/编排/审批/评测/归档）。

**② 完整输入样例**
`demo.py` 内置脱敏差旅申请（产品经理/上海/客户支持/2500 元），
`README` 提供直接可复现的调用。

**③ 证据链 + 验收记录：运行命令 + 预期输出**

```bash
python run_tests.py
# ✅ 3. returns input+evidence+result+acceptance
# ✅ 5. evidence chain has all steps -- evidence=6
# ✅ 6. approval gate applied -- approved=True note=自动通过
# ✅ 7. large amount routes to manager approval -- pending_manager
# ✅ 9. acceptance record complete -- evidence_count=6
# Result: PASS 11   FAIL 0
```

每步一个证据、最终验收记录四要素齐全——即"完整输入、证据、结果及验收记录"。

## 快速开始

```bash
# 零第三方依赖（纯 Python 标准库）
python run_tests.py          # 全部验收验证
python demo.py               # 非提案流程演示
```

## 目录

```
.
├── business_flow.py         # 流程执行器（核心）
├── run_tests.py             # 验收验证
├── demo.py                  # 差旅审批流演示
├── schema/
│   └── flow_config.schema.json # 流程配置模板
├── configs/
│   └── flow-travel-approval-01.json # 差旅审批流配置
├── docs/（验收对照 / 实现说明 / 验证记录）
├── SETUP.md
└── README.md
```

## 设计要点

1. **知识串联**：流程配置声明知识挂载（差旅政策/预算口径/审批矩阵）；
   知识校验步骤检查预算红线。
2. **编排**：6 步状态机（collect→knowledge→orchestrate→approval→evaluate→archive）。
3. **审批门**：金额≤3000 自动通过；>3000 转 `pending_manager` 人工审批。
4. **评测与归档**：按 criteria 评测、归档并生成验收记录。
5. **脱敏合规**：差旅样例无真实个人/金额敏感。

## 环境

- Python 3.8+
- **零第三方依赖**（纯标准库 json/os/re/sys/time）

## 边界说明

本单范围 = 一个公司级非提案任务的完整流程串联；
真实组织审批系统/IM 集成 —— 属其他拆分单。