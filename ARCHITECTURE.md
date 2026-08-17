# 架构

## 组件

- `AGENTS.md`：始终加载的任务判级、上下文预算、路由、范围、验证和完成策略。
- `skills/project-bootstrap`：建立最小且可信的项目上下文。
- `skills/focused-fix`：局部根因修复流程。
- `skills/full-development`：标准、重大和关键三档完整开发流程。
- `skills/sync-project-knowledge`：按影响同步文档并蒸馏经验。
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
5. 项目文档按事实所有权触发加载，不作为启动时的固定阅读包。
6. 只有持久项目事实或经验变化时才加载 `sync-project-knowledge`。
7. 结束时用已有证据执行最小收尾；代码类修改生成 Commit 文稿，但不自动提交或推送。

## 不变量

- 通用规则与项目专属规则使用相互独立的受管标记。
- 安装后的 Skill 仍是可单独使用的标准 Agent Skill。
- 核心指令描述能力，不绑定厂商专属工具。
- 更广验证可以覆盖更窄验证；重复检查必须有具体理由。
- 概述文档负责当前事实，TRACE 负责过程证据。
- 面向人的文本默认使用中文，技术兼容所需标识保持原值。
- 前置调研与收尾均为条件触发，不得成为每轮固定的网络搜索或命令清单。
