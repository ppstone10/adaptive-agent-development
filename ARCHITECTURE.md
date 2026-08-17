# 架构

## 组件

- `AGENTS.md`：始终加载的任务判级、上下文预算、路由、范围、验证和完成策略。
- `skills/project-bootstrap`：建立最小且可信的项目上下文。
- `skills/focused-fix`：局部根因修复流程。
- `skills/full-development`：标准、重大和关键三档完整开发流程。
- `skills/spec-driven-change`：为需要持久行为契约的任务提供轻量/完整 Spec、稳定规范 ID、就近追溯和指定文件静态检查。
- `skills/sync-project-knowledge`：按影响同步文档并蒸馏经验。
- `skills/record-task-log`：在 L2-L5 收尾时按等级追加每日 Agent 任务记录。
- `skills/track-change-trace`：为复杂调查和重大修改建立稳定编号并追加跟踪修改演进。
- `scripts/install.py`：安装或更新受管工作流区块与项目 Skill。
- `scripts/audit.py`：执行只读结构审计。
- `skills/full-development/references/research-guide.md`：仅在新方案触发时加载的有限调研方法。
- `skills/full-development/references/delivery-closure.md`：仅在重大、关键或多范围变更收尾时加载的检查方法。

## 安装模型

本包是发布源。项目会在 `.agents/skills` 下获得每个 Skill 的副本、一个工作流清单，以及由通用受管区和项目自有区组成的 `AGENTS.md`。更新只替换受管区和用户明确要求刷新的 Skill 目录。

## 运行模型

1. Agent 读取 `AGENTS.md`。
2. Agent 按最高风险维度判定任务等级。
3. L0/L1 直接执行；L2 加载 `focused-fix`；L3-L5 加载 `full-development` 的相应档位。
4. 新内容或新方法在定案前进行有限网络调研；既有模式修改跳过。
5. 按任务行为影响决定是否加载 `spec-driven-change`：普通 L2 跳过，相关 L3 使用轻量档，涉及持久契约的 L4/L5 使用完整档。
6. 项目文档按事实所有权触发加载，不作为启动时的固定阅读包。
7. 只有持久项目事实或经验变化时才加载 `sync-project-knowledge`。
8. 结束时用已有证据执行最小收尾；代码类修改生成 Commit 文稿，但不自动提交或推送。
9. 将执行时间、等级、状态和分级结果追加到当天 worklog；L0/L1 由根规则直接记录，L2-L5 按需加载 `record-task-log`。
10. 复杂 L2/演进型 L3 按需、L4/L5 强制使用 `track-change-trace`，在当天 TRACE 追加开始、实质调整和最终映射。

## 不变量

- 通用规则与项目专属规则使用相互独立的受管标记。
- 安装后的 Skill 仍是可单独使用的标准 Agent Skill。
- 核心指令描述能力，不绑定厂商专属工具。
- 更广验证可以覆盖更窄验证；重复检查必须有具体理由。
- 概述文档负责当前事实，TRACE 负责过程证据。
- 面向人的文本默认使用中文，技术兼容所需标识保持原值。
- 前置调研与收尾均为条件触发，不得成为每轮固定的网络搜索或命令清单。
- 每天每个项目只有一个 worklog 文件；日志按时间追加且不拥有当前项目事实。
- 每天每个项目只有一个 TRACE 文件；检查点不可改写，结论变化通过更正或取代事件表达。
- worklog 使用任务编号索引执行结果，TRACE 使用同一编号跟踪修改演进，两者都不拥有当前项目事实。
- DESIGN 拥有项目级意图，Spec 拥有功能级持久行为与验收；Spec 的追溯就近维护，任务 TRACE 只引用规范 ID。
