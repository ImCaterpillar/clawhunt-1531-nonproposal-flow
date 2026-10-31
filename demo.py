# -*- coding: utf-8 -*-
"""演示：非提案业务流程（输入→证据链→审批→评测→归档→验收记录）

运行：python demo.py
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from business_flow import BusinessFlowRunner  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
runner = BusinessFlowRunner(os.path.join(HERE, "configs"))

print("非提案业务流程演示 — 差旅申请试点\n")
print(f"可用流程：{list(runner.flows)}\n")

user_input = {
    "applicant_role": "产品经理",
    "destination": "上海",
    "purpose": "客户现场支持",
    "days": 3,
    "amount_estimate": 2500,
    "reference_budget_rule": "travel-policy-v2",
}
out = runner.execute("flow-travel-approval-01", user_input)

print("完整输入：")
print(" ", json.dumps(out["input"], ensure_ascii=False))
print("\n证据链（6 步）：")
for e in out["evidence"]:
    print(f"  {e['step']} [{e['kind']}]")
print("\n结果：")
print(" ", json.dumps({k: v for k, v in out["result"].items()
                       if k in ("status", "workflow_id",
                                "approval_status", "approval_note",
                                "archived")}, ensure_ascii=False))
print("\n验收记录：")
print(" ", json.dumps(out["acceptance"], ensure_ascii=False))

print("\n" + "=" * 50)
print("验收结果: 完整输入 + 证据 + 结果 + 验收记录 -> ✅")
print("=" * 50)
sys.exit(0)