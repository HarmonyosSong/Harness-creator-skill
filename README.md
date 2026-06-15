# Harness Creator Skill

这是一个可复用的 Harness 工作流部署 Skill，已经同时适配 Codex、Claude Code 和 Cursor 的插件分发结构。

它的目标是帮助 AI Agent 在任意客户端仓库中初始化、升级或审查一套 Harness 工作流框架，包括前置上下文收集、任务包、Agent 契约、评审门禁、验证门禁和 trace 归档。

## 目录结构

```text
.
├── .cursor-plugin/
│   └── plugin.json
├── .codex-plugin/
│   └── plugin.json
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
└── skills/
    └── harness-framework-deployer/
        ├── SKILL.md
        ├── agents/
        ├── assets/
        ├── references/
        └── scripts/
```

说明：

- `skills/harness-framework-deployer/` 是 Skill 的唯一源码位置。
- `.cursor-plugin/` 用于 Cursor 插件分发。
- `.codex-plugin/` 用于 Codex 插件分发。
- `.claude-plugin/` 用于 Claude Code 插件和 marketplace 分发。
- 不再在仓库根目录保留裸 `harness-framework-deployer/`，避免维护两份 Skill。

## Claude Code 安装

在 Claude Code 中添加 marketplace，然后安装插件：

```text
/plugin marketplace add HarmonyosSong/Harness-creator-skill
/plugin install harness-framework-deployer@harness-creator-skill
```

本地校验：

```bash
claude plugin validate --strict .
```

也可以分别校验 manifest：

```bash
claude plugin validate --strict .claude-plugin/plugin.json
claude plugin validate --strict .claude-plugin/marketplace.json
```

## Codex 安装

当前仓库已包含 Codex 插件 manifest：

```text
.codex-plugin/plugin.json
```

如果只想直接安装 Skill，可以安装 Skill 目录：

```text
$skill-installer install https://github.com/HarmonyosSong/Harness-creator-skill/tree/main/skills/harness-framework-deployer
```

如果要按插件分发，请通过 Codex 的插件 marketplace 流程注册本仓库。

本地校验：

```bash
python3 /Users/tal/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

## Cursor 安装

当前仓库已包含 Cursor 插件 manifest：

```text
.cursor-plugin/plugin.json
```

本地联调可以把仓库链接到 Cursor 的本地插件目录：

```bash
ln -s /Users/tal/Desktop/harness-creator-skill/Harness-creator-skill ~/.cursor/plugins/local/harness-framework-deployer
```

然后重启 Cursor，或执行 `Developer: Reload Window`。

如果要公开分发，可以直接按 Cursor 插件仓库提交；单插件仓库只需要 `.cursor-plugin/plugin.json`，不要求额外的 marketplace manifest。

本地 shape 校验：

```bash
python3 skills/harness-framework-deployer/scripts/check_deployed_harness.py . --mode plugin --plugin-runtime cursor
```

## 使用场景

适合用在这些任务中：

- 给一个客户端仓库初始化 Harness 工作流框架。
- 给已有仓库补齐 preflight、review、verify、postflight 和 trace 闭环。
- 审查目标仓库已有 Harness 是否结构完整。
- 把 Harness creator skill 打包成 Codex、Claude Code 或 Cursor 可安装插件。

不适合用在这些任务中：

- 直接完成目标仓库的业务开发需求。
- 替目标仓库编造构建命令、业务模块或代码规范。
- 把某个私有项目规则硬编码成通用 Harness 规则。

## 双端分发校验

运行仓库内置 shape check：

```bash
python3 skills/harness-framework-deployer/scripts/check_deployed_harness.py . --mode plugin --plugin-runtime all
```

期望输出包含：

```text
plugin_distribution: valid
cursor_plugin_distribution: valid
codex_plugin_distribution: valid
claude_plugin_distribution: valid
```

## 维护约束

- Skill 主体只维护在 `skills/harness-framework-deployer/`。
- Cursor 专属元数据只放在 `.cursor-plugin/`。
- Codex 专属元数据只放在 `.codex-plugin/`。
- Claude Code 专属元数据只放在 `.claude-plugin/`。
- 不要把 marketplace 元数据写进 `SKILL.md`。
- 更新插件结构后，需要同时跑 Cursor、Codex 和 Claude Code 校验。
