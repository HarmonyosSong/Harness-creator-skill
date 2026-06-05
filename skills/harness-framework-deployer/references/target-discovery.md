# Target Discovery

部署前先生成 `target_profile`，所有本地化规则都必须来自它。

```text
repo_name:
client_family:
platforms:
build_systems:
package_managers:
entrypoints:
module_patterns:
module_names:
common_layers:
domain_keywords:
high_risk_chains:
source_sets:
build_commands:
test_commands:
lint_commands:
style_conventions:
existing_ai_files:
existing_harness_files:
confidence:
```

## 技术栈识别信号

- Android：`settings.gradle`、`build.gradle`、`build.gradle.kts`、`gradlew`、`AndroidManifest.xml`、`app/src/main`、Kotlin/Java。
- iOS：`.xcodeproj`、`.xcworkspace`、`Podfile`、`Package.swift`、`Info.plist`、Swift/Objective-C。
- HarmonyOS：`build-profile.json5`、`oh-package.json5`、`hvigorfile.ts`、`module.json5`、ArkTS `.ets`。
- Flutter：`pubspec.yaml`、`lib/`、`android/`、`ios/`、`test/`。
- React Native：`package.json`、`metro.config.js`、`android/`、`ios/`、TypeScript/JavaScript 入口。
- Web：`package.json`、`vite.config.*`、`next.config.*`、`src/`、Playwright/Cypress/Vitest/Jest 配置。
- 小程序：`app.json`、`project.config.json`、页面/组件配置。
- 混合仓库：多个端信号并存，Harness 放工作区根目录，并按平台路由。

## 目标仓库语言提取

扫描以下证据：

- 模块名、目录名、包名、target 名、app flavor。
- 页面、路由、组件、服务、测试里的业务词。
- 公共层、基础层、业务层和依赖方向。
- 架构风格：MVC、MVVM、Clean Architecture、Redux、BLoC、Provider、组件化、插件化等。
- 状态管理、路由、网络、日志、埋点、登录、WebView、媒体、支付等高风险链路。
- 构建和验证习惯：CI 文件、npm scripts、Gradle task、xcodebuild scheme、Flutter command、hvigor command 等。

无法确认的命令或规则必须写 `TODO(confirm)`，不得猜。
