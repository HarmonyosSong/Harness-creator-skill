# Harness Framework

## 核心定位

Harness 是一层 AI 工程操作系统，放在业务代码旁边，但不替代业务代码。它负责：

- 任务入口：判断什么时候进入 Harness。
- 上下文收敛：把任务、路径、模块、风险、规则和验证建议写进 Task Packet。
- 工作流门禁：在修改前要求 Spec / Plan / Go，在完成前要求 Review / Verify / Postflight。
- 角色协作：用 Agent 契约限定 Orchestrator、Explorer、Coder、Reviewer、Triage、Verifier 的输入输出。
- 验证闭环：把构建、测试、lint、截图、人工阻塞等统一写成可审计产物。
- 经验沉淀：把高价值任务归档为 trace，把稳定错误规则沉淀到知识层。

## 默认目录结构

```text
target-repo/
├── <repo>_Harness.md
├── harness_Engineering/
│   ├── README.md
│   ├── DECISIONS.md
│   ├── knowledge/
│   │   ├── README.md
│   │   ├── architecture.md
│   │   ├── module-routing.md
│   │   ├── deep-thinking-mode.md
│   │   ├── quick-mode.md
│   │   ├── spec-plan-go.md
│   │   ├── multi-agent-patterns.md
│   │   ├── error-log.md
│   │   ├── playbooks/
│   │   └── module_refs/
│   ├── agents/
│   ├── scripts/
│   ├── runtime/
│   └── archive/
├── AGENTS.md
├── .codex/commands/harness.md
├── .codex/skills/<repo>-harness/SKILL.md
└── skills/<repo>-.../SKILL.md
```

只创建目标 runtime 真正可用的入口；目标仓库不用 Claude，就不要默认创建 `.claude/`。

## 80% 还原边界

通常可通用还原：

- Harness 目录结构。
- 入口、gate、Agent、runtime、verification、trace 流程。
- Task Packet、Context Summary、Spec、Plan、Review、Postflight schema。
- 脚本职责和命令分类。
- 风险输出和收口格式。

必须目标本地化：

- 技术栈规则。
- 模块路由。
- 产品名、target、flavor、包名。
- 构建、测试、lint 命令。
- 代码规范和架构约束。
- 业务域和高风险链路。
- 项目级 skills。
