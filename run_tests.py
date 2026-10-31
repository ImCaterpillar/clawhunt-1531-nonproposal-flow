# -*- coding: utf-8 -*-
"""非提案业务试点主流程验证 —— 对应验收标准
「交付完整输入、证据、结果及验收记录」

零第三方依赖。打印每条验收标准的实测结果。
"""
import json
import os
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from business_flow import BusinessFlowRunner, FlowError, validate  # noqa

PASS, FAIL = [], []
OK = "\u2705"
NO = "\u274c"


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    mark = OK if cond else NO
    line = "  " + mark + " " + name
    if detail:
        line += " -- " + detail
    print(line)


print("=" * 78)
print("Non-Proposal Business Flow -- acceptance verification")
print("=" * 78)
print("Acceptance: 完整输入、证据、结果及验收记录\n")

HERE = os.path.dirname(os.path.abspath(__file__))
runner = BusinessFlowRunner(os.path.join(HERE, "configs"))

# 1. 流程配置可加载
check("1. flow config loadable", runner.flows.get("flow-travel-approval-01") is not None,
      f"flows={list(runner.flows)}")

# 2. 完整输入（脱敏差旅申请）
user_input = {
    "applicant_role": "产品经理",
    "destination": "上海",
    "purpose": "客户现场支持",
    "days": 3,
    "amount_estimate": 2500,   # 脱敏金额
    "reference_budget_rule": "travel-policy-v2",
}
out = runner.execute("flow-travel-approval-01", user_input)

# 3. 返回四要素：完整输入/证据/结果/验收记录
check("3. returns input+evidence+result+acceptance",
      "input" in out and "evidence" in out
      and "result" in out and "acceptance" in out,
      f"keys={list(out.keys())}")

# 4. 完整输入保留（快照一致）
check("4. complete input preserved",
      out["input"].get("destination") == "上海"
      and out["input"].get("amount_estimate") == 2500,
      str(out["input"])[:60])

# 5. 证据链完整（6 步全留证）
check("5. evidence chain has all steps",
      len(out["evidence"]) == 6,
      f"evidence={len(out['evidence'])}")

# 6. 审批门生效（金额 2500 <= 3000 应在红线内自动通过）
appr = [e for e in out["evidence"] if e["kind"] == "approval"][0]
check("6. approval gate applied",
      appr["approved"] is True and "红线内" in appr["note"],
      f"approved={appr['approved']} note={appr['note'][:20]}")

# 7. 大额申请被拦截（> 3000 需人工）
big_in = dict(user_input)
big_in["amount_estimate"] = 8500
out_big = runner.execute("flow-travel-approval-01", big_in)
appr_big = [e for e in out_big["evidence"] if e["kind"] == "approval"][0]
check("7. large amount routes to manager approval",
      appr_big["approved"] is False
      or "需 line_manager" in appr_big["note"],
      f"approved={appr_big['approved']} note={appr_big['note'][:24]}")

# 8. 结果含状态流转 + 归档
check("8. result contains status+archive",
      out["result"].get("status") == "orchestrated"
      and out["result"].get("archived") is True,
      f"status={out['result'].get('status')} archived={out['result'].get('archived')}")

# 9. 验收记录四要素齐
acc = out["acceptance"]
check("9. acceptance record complete",
      acc.get("complete_input") is True
      and acc.get("evidence_count") == 6
      and acc.get("policy_compliant") is True
      and acc.get("archived") is True,
      str(acc))

# 10. 非法配置被拒（缺步骤/知识挂载/审批）
bad = {
    "flow_id": "flow-bad-99", "flow_name": "x",
    "task_type": "y", "steps": [], "knowledge_mounts": [],
    "approval_gates": {}, "evaluation": {}
}
errs = validate(bad, runner.schema)
check("10. invalid flow config rejected", len(errs) >= 4,
      f"{len(errs)} errors")

# 11. demo 可运行
r11 = subprocess.run([sys.executable, "demo.py"], cwd=HERE,
                     capture_output=True, text=True, encoding="utf-8",
                     errors="replace")
check("11. demo.py exit=0", r11.returncode == 0, f"exit={r11.returncode}")

# 12. 交付齐套
refs = ["business_flow.py", "run_tests.py", "demo.py",
        "schema/flow_config.schema.json",
        "configs/flow-travel-approval-01.json",
        "README.md", "SETUP.md",
        "docs/验收对照.md", "docs/实现说明.md", "docs/验证记录.md"]
broken = [r for r in refs if not os.path.isfile(os.path.join(HERE, r))]
check("12. delivery set complete (10 files)", not broken,
      "broken=" + str(broken) if broken else str(len(refs)) + " files")

print()
print("=" * 78)
print("Result: PASS " + str(len(PASS)) + "   FAIL " + str(len(FAIL)))
print("=" * 78)
if FAIL:
    print("Failed: " + ", ".join(FAIL))
sys.exit(1 if FAIL else 0)