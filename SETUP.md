# 设置与运行

零第三方依赖，无需安装任何包。

## 环境要求

- Python 3.8+（标准库：json / os / re / sys / time）

## 快速验证

```bash
# 在项目根目录
python run_tests.py        # 验收断言，期望 PASS 11 / FAIL 0
python demo.py             # 差旅审批流演示，期望退出码 0
```

## 在自己的代码中使用

```python
from business_flow import BusinessFlowRunner

runner = BusinessFlowRunner("configs")

user_input = {
    "applicant_role": "产品经理",
    "destination": "上海",
    "purpose": "客户现场支持",
    "days": 3,
    "amount_estimate": 2500,   # 脱敏金额
    "reference_budget_rule": "travel-policy-v2",
}
out = runner.execute("flow-travel-approval-01", user_input)
print(out["input"])        # 完整输入
print(len(out["evidence"]) # 证据链（6）
print(out["result"])       # 结果
print(out["acceptance"])   # 验收记录
```

## 新增业务流

1. 复制 `configs/flow-travel-approval-01.json`
2. 改 `flow_id` / 名称 / 步骤 / 知识挂载 / 审批门 / 评测口径
3. 放入 `configs/`，`BusinessFlowRunner` 自动校验加载

## 常见问题

- **审批门怎么生效？** 配置 `approval_gates.required=true` + 门槛
  逻辑；核心实现内金额 > 3000 转人工（可改阈值）。
- **步骤类型有哪些？** collect_input / knowledge_check / orchestrate /
  approval / evaluate / archive。
- **Windows 中文乱码？** 脚本已内置 UTF-8 重配置。