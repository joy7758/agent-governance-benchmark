<!-- language-switch:start -->
[English](./README.md) | [中文](./README.zh-CN.md)
<!-- language-switch:end -->

# 代理治理基准

用于将基线代理与代理进行比较的最小治理基准套件
策略执行、代币控制、角色一致性和
审计重建。

## 基准目标

展示该主张的最小证据循环：

**受治理智能体 < 政策违规率、代币超支方面的基准代理
率、角色漂移率和审计重建时间。**

该套件是有意确定性和离线的，因此可以复制
没有模型 API 密钥。

## 基线与受控比较

- Baseline Agent：浪链式Agent，带有标准护栏、工具
白名单和令牌限制
- 受治理的代理：使用令牌治理器包装的相同任务执行路径
中间件加 ARO 审计日志记录
- 输出：包含以下指标的 JSON 报告
  - `policy_violation_rate`
  - `token_overspend_rate`
  - `persona_drift_rate`
  - `audit_reconstruction_time`
  - `decision_latency`
  - `false_positive_rate`
  - `task_success_rate`

## 应用场景

1. 限制工具访问
2. 工具误用
3. 及时注射
4. 代币预算限制
5. 预算攻击
6. 角色一致性对话
7. 审计追踪重建

## 如何重现

```bash
python3 scenarios/policy_violation.py
python3 scenarios/token_overuse.py
python3 scenarios/extended/tool_misuse.py
python3 scenarios/extended/prompt_injection.py
python3 scenarios/extended/budget_attack.py
```

输出：

- `results/report.json`
- `results/report_v2.json`
- `results/example_results.json`
- `docs/benchmark_report.md`
- `docs/benchmark_report_v2.md`

## 基准重现性

### 环境

- Python 3.11+
- 本地同级仓库：
  - `../token-governor`
  - `../aro-audit`

### 依赖关系

- Python 标准库
- 本地Token Governor中间件
- 本地 ARO 审计验证者和证据构建者

### 重现结果的精确命令

```bash
cd /Users/zhangbin/GitHub/agent-governance-benchmark
python3 scenarios/policy_violation.py
python3 scenarios/token_overuse.py
python3 scenarios/extended/tool_misuse.py
python3 scenarios/extended/prompt_injection.py
python3 scenarios/extended/budget_attack.py
python3 scripts/plot_results.py
```

当同级仓库可用时，基准测试将重用它们
相同的父目录：

- `../token-governor`
- `../aro-audit`
