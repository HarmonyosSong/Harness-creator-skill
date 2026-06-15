# Review Checklist

## 部署前

- 已生成 `target_profile`。
- 构建、测试、lint 命令来自目标仓库证据。
- 已检查已有 `AGENTS.md`、`.codex/`、`.claude/`、`skills/`、`harness_Engineering/`。
- 冲突文件有合并方案，未直接覆盖。

## 部署后

- `<repo>_Harness.md` 存在。
- `harness_Engineering/knowledge/`、`agents/`、`scripts/`、`runtime/`、`archive/` 存在。
- `harness_Engineering/knowledge/context_manifest.yaml`、`knowledge/summaries/`、`scripts/context-budget-gate.sh`、`scripts/context-expand.sh` 存在。
- `runtime/.gitignore` 防止历史任务产物污染提交。
- `harness-index` 可运行。
- `preflight-context` 可生成 Task Packet、Context Summary 和 Context Audit。
- AGENTS / command / skill 名称和实际文件路径一致。
- 未确认内容都标为 `TODO(confirm)`。
- 如果启用了 Cursor 分发，`.cursor-plugin/plugin.json` 存在且路径有效。

## 禁止项

- 不得把参考项目的品牌、模块、业务规则写成通用框架规则。
- 不得复制历史 runtime 任务产物。
- 不得用 `echo success` 伪装验证成功。
- 不得登记不存在的 skill、command 或脚本。
- 不得绕过 Context Budget Gate 直接把全文文档写进默认读取清单。
