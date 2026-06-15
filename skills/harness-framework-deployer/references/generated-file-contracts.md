# Generated File Contracts

## Plugin 分发文件

### `.cursor-plugin/plugin.json`

用于 Cursor Plugin 分发。最少必须包含：

- `name`: 插件名，lowercase kebab-case。

推荐默认包含：

- `version`: 默认 `1.0.0`，除非用户指定。
- `description`: 人类可读的一句话用途说明。
- `author.name`: 作者或组织名。
- `skills`: `./skills/`，或者其他真实存在的相对路径。

不得包含：

- `[TODO: ...]` 占位符。
- 指向不存在目录的 `skills`、`rules`、`commands`、`agents`、`hooks`。
- 绝对路径或 `..` 路径跳转。

### `.codex-plugin/plugin.json`

必须包含：

- `name`: 与插件目录名一致，使用 lowercase hyphen-case。
- `version`: 默认 `1.0.0`，除非用户指定。
- `description`: 人类可读的一句话用途说明。
- `skills`: `./skills/`，并且该目录真实存在。

不得包含：

- `[TODO: ...]` 占位符。
- 不存在的 `apps`、`mcpServers` 或其他 companion 配置。
- marketplace policy；marketplace policy 属于 marketplace entry，不属于 plugin manifest。

### `skills/harness-framework-deployer/`

必须包含原 skill 的 `SKILL.md`。如果原 skill 有 `agents/`、`references/`、`assets/`、`scripts/`，迁移后必须保持相同相对路径，避免破坏 `SKILL.md` 中引用。

### `.claude-plugin/plugin.json`

用于 Claude Code Plugin 分发。必须包含：

- `name`: 与插件名一致，使用 lowercase hyphen-case。
- `version`: 默认 `1.0.0`，除非用户指定。
- `description`: 人类可读的一句话用途说明。
- `author.name`: 作者或组织名。

不得包含：

- `[TODO: ...]` 占位符。
- 不存在的 hooks、agents、commands、MCP、LSP 或其他 companion 配置。

### `.claude-plugin/marketplace.json`

用于 Claude Code marketplace 安装。必须包含：

- `name`: marketplace 名称。
- `description`: marketplace 用途说明；strict 校验会要求补齐。
- `owner.name`: 维护者或组织名。
- `plugins[]`: 至少包含 `name`、`source`、`description`。

当插件就在 marketplace 仓库根目录时，`source` 使用 `"./"`。

### `.cursor-plugin/marketplace.json`

只在多插件 Cursor marketplace 仓库中使用。单插件仓库不要求它。

若需要生成，必须包含：

- `name`: marketplace 名称。
- `owner.name`: 维护者或组织名。
- `plugins[]`: 至少包含 `name`、`source`。

推荐补齐：

- `metadata.description`
- 每个 `plugins[]` 条目的 `description`

## `<repo>_Harness.md`

必须包含：

- 一句话定位：这是目标仓库的 AI 工作流入口。
- 显式触发规则：只有用户调用 `/harness` 或明确说使用 Harness 时才进入。
- 当前仓库架构总览：由 `target_profile` 生成，不写没有证据的业务事实。
- 默认阅读顺序：入口 -> context summary -> task packet -> 命中摘要 -> 按需全文；`context_audit` 只在扩容或复盘时读取。
- 完整工作流：Thinking Mode -> Preflight -> Context Budget Gate -> Agent Gate -> Route -> Spec -> Plan -> Go -> Execute -> Review -> Prebuild -> Verify -> Postflight -> Trace。
- 输出要求：模式选择、命中模块、启用角色、产物路径、验证结果、假设、未覆盖项、风险。

## `AGENTS.md`

只登记真实存在的 project skills 和 command。必须说明：

- Harness 的触发条件。
- 多 Agent 不可用时是否阻塞，或如何显式降级。
- 不要把普通需求自动升级为 Harness，除非用户明确要求。
- 项目 skills 的加载位置，例如 `.codex/skills/`、`.cursor/skills/` 或仓库级 `skills/`。

## `.codex/commands/harness.md`

必须保持薄入口，只说明 `/harness` 如何调用索引和路由。命令清单以 `harness-index.sh` 为准，避免维护两份索引。

## Cursor 项目级 skill

当目标 runtime 包含 Cursor 且用户需要仓库内原生入口时，优先生成：

- `.cursor/skills/<repo>-harness/SKILL.md`

除非用户明确要求，否则不要为 Cursor 伪造单独的 `/harness` 命令文件；Cursor 原生支持通过 skill 调用或插件命令分发。

## Agent 契约

每个 Agent 文件使用同一结构：

```text
# <Role> 契约
## 角色定位
## 输入
## 输出
## 上下文装载
  - MUST
  - OPTIONAL
  - FORBIDDEN
## 允许动作
## 禁止动作
## 汇报格式
```

基础角色：

- Orchestrator：控制 gate、汇总产物、对用户沟通；不直接替代 Reviewer。
- Context/Explorer：只读探索仓库，输出模块、风险、上下文建议；不得改文件。
- Coder/Worker：只在 Spec / Plan / Go 通过后修改文件；必须记录偏离。
- Reviewer：审查 diff 是否符合已授权基线；优先报告问题。
- Triage：处理构建、测试、类型、静态检查错误；判断是否可自愈。
- Verifier：复核验证范围、命令、未覆盖项和残余风险。

## Runtime Schema

### Task Packet

```text
status:
created_at:
task:
target_repo:
mode:
branch_or_commit:
changed_files:
task_type:
modules:
platforms:
risk_level:
high_risk_reasons:
target_profile_evidence:
context_budget:
  level:
  max_full_docs:
  max_summary_docs:
  read_full_routing_by_default:
  read_agent_contracts_by_default:
context_plan:
  read_first:
  expand_if_needed:
  forbidden_by_default:
context_artifacts:
  context_summary_path:
  context_audit_path:
recommended_agents:
recommended_validation:
spec_required:
plan_required:
trace_recommended:
assumptions:
todo_confirm:
```

### Context Summary

```text
task_summary:
budget_level:
budget_limits:
  max_full_docs:
  max_summary_docs:
module_guess:
risk_summary:
read_first:
expand_only_if:
forbidden_by_default:
likely_files:
validation_hint:
open_questions:
```

### Context Audit

```text
budget_level:
budget_limits:
  max_full_docs:
  max_summary_docs:
audit_entries:
  - stage:
    type:
    doc:
    reason:
    over_budget:
notes:
```

### Spec

```text
status: draft | signed_off
user_goal:
in_scope:
out_of_scope:
acceptance_criteria:
affected_modules:
risks:
assumptions:
sign_off:
```

### Implementation Plan

```text
status: draft | approved | in_progress | completed | deviated
signed_spec_path:
go_record:
target_files:
non_goals:
steps:
  - id:
    action:
    files:
    validation:
execution_tracking:
deviation_log:
rollback_plan:
```
