---
name: <repo>-harness
description: <repo> 项目 Harness 显式入口。只有用户调用 /harness 或明确要求使用 Harness 时启用。
---

# <repo> Harness

## Pattern

- ADK 5-pattern tags: `Pipeline` + `Tool Wrapper` + `Reviewer`

## Input Contract

- 用户任务
- 文件路径或模块名
- 可选错误日志

## Output Contract

- task_packet_path
- context_summary_path
- context_audit_path
- route_result
- verification_result
- risks

## Workflow

1. Thinking Mode
2. Preflight
3. Context Budget
4. Route
5. Gate
6. Verify
7. Postflight

## Gates

- 未运行 preflight 不得修改文件。
- 未运行 context budget gate 不得默认展开全文规则文档。
- 修改类任务未授权不得执行。
