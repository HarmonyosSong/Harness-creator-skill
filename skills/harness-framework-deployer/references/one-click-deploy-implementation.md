# One-click Deploy Implementation

执行 `full` 或 `skeleton` 部署时，必须实际写入目标仓库。不得只输出目录清单。

当任务目标是“公开给别人安装”“GitHub 分发”“marketplace”或“按官方 Plugin 结构改造”时，必须生成目标 runtime 的 Plugin 分发层，而不是只保留裸 skill 根目录。

## 0. Plugin 分发结构

推荐仓库结构：

```text
<repo>/
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
        ├── references/
        ├── assets/
        └── scripts/
```

最小 `.cursor-plugin/plugin.json`：

```json
{
  "name": "harness-framework-deployer",
  "version": "1.0.0",
  "description": "Deploy a reusable Harness workflow framework into client repositories.",
  "author": {
    "name": "HarmonyosSong"
  },
  "skills": "./skills/"
}
```

最小 `.codex-plugin/plugin.json`：

```json
{
  "name": "harness-framework-deployer",
  "version": "1.0.0",
  "description": "Deploy a reusable Harness workflow framework into client repositories.",
  "skills": "./skills/"
}
```

最小 `.claude-plugin/plugin.json`：

```json
{
  "name": "harness-framework-deployer",
  "version": "1.0.0",
  "description": "Deploy a reusable Harness workflow framework into client repositories.",
  "author": {
    "name": "HarmonyosSong"
  }
}
```

最小 `.claude-plugin/marketplace.json`：

```json
{
  "name": "harness-creator-skill",
  "description": "Claude Code marketplace for reusable Harness workflow deployment plugins.",
  "owner": {
    "name": "HarmonyosSong"
  },
  "plugins": [
    {
      "name": "harness-framework-deployer",
      "source": "./",
      "description": "Deploy a reusable Harness workflow framework into client repositories."
    }
  ]
}
```

迁移规则：

- 如果仓库根目录存在 `harness-framework-deployer/SKILL.md`，迁移到 `skills/harness-framework-deployer/`。
- 保留 `agents/`、`references/`、`assets/`、`scripts/` 及其相对路径。
- Cursor 分发新增 `.cursor-plugin/plugin.json`；多插件 Cursor marketplace 仓库才额外考虑 `.cursor-plugin/marketplace.json`。
- Codex 分发新增 `.codex-plugin/plugin.json`。
- Claude Code 分发新增 `.claude-plugin/plugin.json`；如果用户要求 GitHub marketplace 安装，同步新增 `.claude-plugin/marketplace.json`。
- 不要把 marketplace 元数据写进 `SKILL.md`。
- 迁移后裸 skill 根目录应删除或标记为冲突，避免维护两份 skill。


## 1. 生成部署清单

先生成 `deployment_manifest`：

```text
repo:
mode:
runtime:
will_create:
will_update:
will_skip:
conflicts:
target_profile:
commands:
  build:
  test:
  lint:
  verify_fast:
  verify_module:
plugin_distribution:
  enabled:
  runtime:
  cursor_plugin_json:
  cursor_marketplace_json_optional:
  codex_plugin_json:
  claude_plugin_json:
  claude_marketplace_json:
  skills_root:
  marketplace:
todo_confirm:
```

判定规则：

- 文件不存在 -> `will_create`。
- 文件存在且属于 Harness 旧版本 -> `will_update`。
- 文件存在且不是 Harness 文件 -> `conflicts`，未经用户同意不得覆盖。
- 目标 runtime 不支持的入口 -> `will_skip`。

## 2. 最小脚本实现要求

脚本可以用 shell、Python、Node 或目标仓库已有脚本体系实现。职责必须稳定。

### `harness-index`

必须支持：

```text
list
search <query>
command <key>
```

未知 key 返回非 0；无参数时等价于 `list`。

### `changed-modules`

实现步骤：

1. 读取 `git diff --name-only HEAD` 或用户传入文件列表。
2. 用 `target_profile.module_patterns` 做最长前缀匹配。
3. 输出 changed_file、module、platform、risk_hint。
4. 无法匹配时 `module=unknown`，不得猜业务归属。

### `preflight-context`

必须支持：

```text
--task <text>
--from-git
--skip-git
--format text|json
--output <path>
<paths...>
```

实现步骤：

1. 解析任务文本和路径。
2. 如果 `--from-git`，调用 `changed-modules`。
3. 根据路径、关键词、模块表识别 task_type、modules、platforms。
4. 根据高风险词和跨模块数量计算 risk_level。
5. 生成 `runtime/task_packets/<timestamp>-<slug>/task_packet.md`。
6. 同目录生成 `context_summary.md`。
7. 同目录生成 `context_audit.md`，记录预算上限、默认读取结果和后续扩容审计。
8. 输出 `context_budget.level`、`context_budget.max_full_docs`、`context_budget.max_summary_docs`。
9. 把 `Context Plan` 拆成 `read_first`、`expand_if_needed`、`forbidden_by_default`。
10. 如果 `--output` 指向 json，写入 task_packet_path、context_summary_path、context_audit_path、risk_level、modules、context_budget。

### `context-budget-gate`

必须支持：

```text
--task-packet <path>
--type <summary|full>
--doc <path>
--reason <text>
--stage <name>
```

实现步骤：

1. 从 Task Packet 或相邻 `context_audit.md` 读取预算等级和上限。
2. 统计当前已读取的 `summary` / `full` 数量。
3. 如果本次读取会超预算，返回非 0，除非用户或调用方显式允许 over-budget。
4. 输出结构化结果，至少包含 `allowed`、`used`、`limit`、`over_budget`。

### `context-expand`

必须支持：

```text
--task-packet <path>
--stage <name>
--type <optional_full|optional_summary|forbidden_full|forbidden_summary>
--doc <path>
--reason <text>
```

实现步骤：

1. 调用 `context-budget-gate`。
2. 把本次扩容追加记录到 `context_audit.md`。
3. 返回全文路径以及可用的摘要路径。
4. 未命中摘要时返回空摘要路径，但不得伪造。

### `verify-fast`

实现步骤：

1. 从 target_profile.commands 选择最低成本命令，优先级 lint -> typecheck -> unit -> build。
2. 命令存在则执行并记录到 `runtime/verification/`。
3. 命令未知则输出 `TODO(confirm command)`，返回 2，不伪装成功。

### `verify-module`

实现步骤：

1. 接收 module/path。
2. 查 `module-routing.md` 中推荐命令。
3. 有命令则执行。
4. 无命令则降级到 `verify-fast` 或返回 2。
5. 写 verification summary。

### `prebuild-review`

实现步骤：

1. 读取 task_packet_path。
2. 检查是否存在 review 结果。
3. 检查是否有未处理 fail finding。
4. 输出 `allow_build: yes|no`。
5. `allow_build=no` 时返回非 0。

### `postflight-check`

实现步骤：

1. 读取 task_packet、review、verification。
2. 检查验证是否存在。
3. 汇总 assumptions、unverified、risks。
4. 生成 `runtime/postflight/<timestamp>-summary.md`。
5. 如果缺验证且未说明原因，返回非 0。

### `trace-archive`

实现步骤：

1. 接收 task_packet_path。
2. 找到同任务的 spec、plan、review、verification、postflight。
3. 复制到 `archive/traces/<timestamp>-<slug>/`。
4. 生成 `trace_index.md`。

## 3. 一键部署验收条件

`full` 模式完成后必须满足：

- `harness_Engineering/scripts/harness-index.sh list` 可运行。
- 所有生成脚本语法检查通过。
- `preflight-context.sh --skip-git --task "Harness deploy smoke" <known path>` 能生成 Task Packet、Context Summary 和 Context Audit。
- `harness_Engineering/knowledge/context_manifest.yaml` 存在，且 `knowledge/summaries/` 目录可发现。
- `context-budget-gate.sh` 和 `context-expand.sh` 存在。
- `AGENTS.md` 中登记的 command / skill 文件真实存在。
- 如果是纯 Cursor Plugin 分发仓库，`check_deployed_harness.py <repo> --mode plugin --plugin-runtime cursor` 通过。
- 如果是纯 Codex Plugin 分发仓库，`check_deployed_harness.py <repo> --mode plugin --plugin-runtime codex` 通过。
- 如果是纯 Claude Code Plugin 分发仓库，`check_deployed_harness.py <repo> --mode plugin --plugin-runtime claude` 和 `claude plugin validate --strict <repo>` 通过。
- 如果是 Codex + Claude 双兼容分发仓库，`check_deployed_harness.py <repo> --mode plugin --plugin-runtime both`、`claude plugin validate --strict <repo>` 和 Codex plugin validator 通过。
- 如果是三端兼容分发仓库，`check_deployed_harness.py <repo> --mode plugin --plugin-runtime all` 通过。
- 如果是已部署 Harness 的仓库同时需要 Plugin 分发，`check_deployed_harness.py <repo> --plugin --plugin-runtime <codex|claude|cursor|both|all>` 通过。
- 未确认命令全部出现在 `TODO(confirm)`，没有伪造成功。
