# Context Budget Governance

## Goal

把 Harness 从“有工作流”升级为“有工作流且有硬约束上下文预算”的框架。

## Required Artifacts

生成的新 Harness 至少要包含：

- `harness_Engineering/knowledge/context_manifest.yaml`
- `harness_Engineering/knowledge/summaries/`
- `harness_Engineering/scripts/context-budget-gate.sh`
- `harness_Engineering/scripts/context-expand.sh`
- `runtime/task_packets/<task>/task_packet.md`
- `runtime/task_packets/<task>/context_summary.md`
- `runtime/task_packets/<task>/context_audit.md`

## Required Runtime Rules

- preflight 必须输出预算等级，而不是只输出推荐阅读顺序。
- 默认读取摘要，不默认读取长文档全文。
- `optional_full` 和 `forbidden_by_default` 文档在读取前必须经过 `context-budget-gate`。
- 每次扩容都必须写入 `context_audit`，至少记录：
  - `stage`
  - `type`
  - `doc`
  - `reason`
  - `over_budget`
- Agent 契约全文不默认读取；只有在对应角色真的被启用时才允许读取全文。

## Default Budget Levels

| level | max_full_docs | max_summary_docs | default_full_routing | default_agent_contracts |
| --- | --- | --- | --- | --- |
| `minimal` | 0 | 2 | no | no |
| `light` | 0 | 3 | no | no |
| `normal` | 1 | 5 | no | no |
| `high_risk` | 2 | 8 | no | no |

说明：

- `task_packet.md`、`context_summary.md`、阶段 gate 摘要不计入全文额度。
- 超预算读取必须显式留下 `context_expand_reason`。

## Context Manifest Requirements

`context_manifest.yaml` 至少要能表达：

- `id`
- `title`
- `full_path`
- `summary_path`
- `category`
- `default_load`
- `stages`
- `modules` 或 `risk_tags`
- `full_load_triggers`

## Generation Guidance

- 大型 playbook、module ref、Agent 契约、项目 skill 规则默认都要有运行态摘要。
- Harness 入口和 project skill 只保留状态机、STOP 条件和下一步动作，不要重复铺开长解释。
- 当部署模式是 `full` 时，`context_manifest`、运行态摘要目录和预算脚本属于必备产物，不可省略。
