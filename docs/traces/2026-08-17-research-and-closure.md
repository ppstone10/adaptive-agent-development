# 前置调研与最小收尾

- 日期：2026-08-17
- 范围：新方案调研、交付收敛和 Commit 文稿
- 工作流等级：重大

## 意图与边界

新功能和新方法不能只凭 Agent 记忆直接设计，应先参考成熟做法；同时，收尾不能演变为重新读文档、重新测试和重复总结。目标是在提高方案质量与形成闭环的同时，保持实际实现优先。

## 调研来源与提取方法

- OpenAI Codex 官方文档说明 Codex 会在工作前读取 `AGENTS.md`，支持全局与项目分层，并建议规则保持简洁、专用规则靠近适用目录。
- GitHub Copilot 官方文档支持仓库级、路径级和 Agent 指令，并让目录树中更近的 `AGENTS.md` 优先，证明“通用规则 + 项目或局部规则”的分层方式已被成熟产品采用。
- OpenCode 官方文档支持项目和全局 `AGENTS.md`，并明确建议根据具体任务按需读取外部规则，而不是预先加载所有参考内容。
- Conventional Commits 1.0.0 使用 `<type>[optional scope]: <description>` 结构，允许正文和页脚，并用 `!` 或 `BREAKING CHANGE:` 标识不兼容变更。

来源：

- https://developers.openai.com/codex/guides/agents-md
- https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot
- https://opencode.ai/docs/rules/
- https://www.conventionalcommits.org/en/v1.0.0/

## 设计决策

- 前置调研只由新功能、新方法、新依赖、新协议或项目无成熟先例触发，局部缺陷与既有模式修改跳过。
- 调研通常限制为 2～4 个高质量来源，以决策问题和停止条件控制成本。
- 最小收尾规则放入始终加载的 `AGENTS.md`；重大收尾细节作为按需参考资料。
- 收尾复用本轮已有差异和验证结果，不默认运行任何命令。
- 代码类修改必须生成 Commit 文稿，但提交与推送始终由用户决定。

## 验证

- 校验四个 Skill 的结构和引用。
- 编译安装与审计脚本。
- 验证全新安装、已有项目升级、项目专属区保留和版本更新。
- 检查中文内容与文本格式。

## 剩余风险

网络资料质量与可访问性会随环境变化。流程要求优先权威来源并保留未验证结论，但不能自动保证外部方法适合当前项目；最终选择仍需服从项目约束和实际验证。
