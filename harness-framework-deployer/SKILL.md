---
name: harness-framework-deployer
description: 通用开源 Harness 框架部署技能。用于在任意客户端仓库中初始化、部署、升级或审查一套 AI Harness 工作流框架；目标仓库不限品牌和技术栈，可用于 Android、iOS、HarmonyOS、Flutter、React Native、Web、小程序或混合客户端仓库。
---

# Harness Framework Deployer

## Pattern

- ADK 5-pattern tags: `Generator` + `Pipeline` + `Reviewer` + `Inversion` + `Tool Wrapper`
- Primary pattern: `Generator`，生成 Harness 目录、入口文档、脚本、runtime 模板和项目 skills。
- Secondary pattern: `Pipeline`，按 discovery -> plan -> generate -> validate -> report 顺序执行。
- Secondary pattern: `Reviewer`，用 gate 和 checklist 检查是否误套业务、误造命令或遗漏验证。
- Supporting patterns: `Inversion` 先识别目标仓库语言再生成规则；`Tool Wrapper` 把扫描、验证和 smoke check 固定为脚本入口。

## Goal

在任意客户端仓库中部署一套自包含的 Harness 工作流框架，让 AI 处理需求、修复、评审和验证时有统一入口、统一上下文、统一门禁、统一产物和统一收口。

## Input Contract

- 目标仓库路径；用户要求实际写入但没给路径时，先问目标仓库在哪里。
- 部署模式：`plan_only`、`skeleton`、`full`、`audit`。
- 目标 AI runtime：Codex、Claude、自定义 Agent、shell-only、未知或混合。
- 可选偏好：Harness 名称、是否启用多 Agent、是否生成 project skills、是否生成 shell 脚本、是否接入 CI。

## Output Contract

- `target_profile`：技术栈、模块、入口、公共层、业务词、构建/测试/lint 命令、已有 AI 文件。
- `deployment_manifest`：新建、更新、跳过、冲突四类文件。
- 生成或更新的 Harness 文件路径。
- smoke 验证结果。
- `TODO(confirm)`、未覆盖项和残余风险。

## Use This Skill For

- 在新客户端仓库中一键部署 Harness 框架。
- 把已有仓库升级为带 preflight、gate、review、verify、postflight 的 AI 工作流。
- 审查目标仓库已有 Harness 是否结构完整。
- 生成目标仓库 project skills、Agent 契约、runtime 产物模板和脚本入口。

## Do Not Use This Skill For

- 直接完成目标仓库的业务开发需求。
- 替目标仓库发明业务事实、构建命令或代码规范。
- 把某个私有项目的业务规则原样迁移为通用规则。

## Minimal Workflow

1. Discovery：读取目标仓库，按 `references/target-discovery.md` 生成 `target_profile`。
2. Conflict Check：检查已有 `AGENTS.md`、`.codex/`、`.claude/`、`skills/`、`harness_Engineering/`。
3. Plan：生成 `deployment_manifest`，列出 create / update / skip / conflict。
4. Generate：按 `references/one-click-deploy-implementation.md` 生成目录、入口、知识层、Agent 契约、脚本、runtime 模板和 project skills。
5. Localize：按目标仓库证据写入模块路由、验证命令和技术栈约束；无法确认的内容写 `TODO(confirm)`。
6. Validate：运行 `scripts/check_deployed_harness.py <target-repo>`，并运行目标仓库可用的脚本语法检查和 preflight smoke。
7. Report：输出部署结果、验证结果、未确认项和风险。

## Decision Gates

- Gate 1：没有目标仓库路径时，不做实际部署。
- Gate 2：没有完成 `target_profile` 时，不生成本地化路由和技术规则。
- Gate 3：不得覆盖用户已有文件；冲突时先报告合并方案。
- Gate 4：不得登记不存在的 skill、command 或脚本。
- Gate 5：不得编造 build / test / lint 命令。
- Gate 6：`full` 模式不得只生成目录和说明文档，必须生成可运行的最小脚本和 runtime 模板。
- Gate 7：任何返回成功的验证脚本都必须真的执行命令或明确说明只是 smoke，不得伪装验证。
- Gate 8：目标 runtime 不支持多 Agent 时，必须写明 blocked 或显式降级规则。

## Shared References

- `references/harness-framework.md`：Harness 核心概念、目录结构、80% 还原边界。
- `references/target-discovery.md`：多端客户端仓库识别规则。
- `references/generated-file-contracts.md`：入口、AGENTS、Agent 契约、knowledge 文件、runtime schema。
- `references/one-click-deploy-implementation.md`：一键部署算法和最小脚本实现要求。
- `references/flow-diagrams.md`：Harness 分层、主流程、部署、路由、多 Agent、授权、验证和文件化通信流程图。
- `references/review-checklist.md`：部署和审查 checklist。

## Shared Assets

- `assets/templates/harness-entry.md`
- `assets/templates/project-harness-skill.md`
- `assets/templates/agent-contract.md`
- `assets/templates/task-packet.md`

## Shared Scripts

- `scripts/check_deployed_harness.py`
