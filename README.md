# Adaptive Agent Development

一个可移植、与具体 Agent 厂商无关的开发工作流，根据项目风险分配上下文和验证成本。

本包用根目录 `AGENTS.md` 作为始终加载的轻量控制层，用四个按需 Agent Skill 分别处理项目初始化、精准修复、完整开发和知识同步。适用于支持 `AGENTS.md` 与开放 `SKILL.md` 格式的 Agent；不支持原生 Skill 加载时，可按 `AGENTS.md` 指引直接读取对应 Skill。

除路径、命令、代码标识符、标准名称和无法合理翻译的专有名词外，本包及其生成内容默认使用中文。

## 接入项目

```bash
python3 scripts/install.py /path/to/project
```

安装器会新增或刷新受管工作流区块，将 Skill 复制到 `.agents/skills/`，并写入 `.agents/workflow.json`。项目自己的 `AGENTS.md` 定制区会被保留。接入已有但未受管的 `AGENTS.md` 时使用 `--merge`；明确刷新已安装 Skill 时使用 `--force`。

无修改预演与只读审计：

```bash
python3 scripts/install.py /path/to/project --dry-run
python3 scripts/audit.py /path/to/project
```

## 设计重点

- 默认采用足够完成任务的最轻流程。
- 仅在需要其中事实时加载文档和 Skill。
- 局部缺陷沿最短证据路径完成修复。
- 避免重复执行已被更广检查覆盖的验证。
- 仅同步确实受到变更影响的持久知识。
- 可移植核心不绑定任何厂商专属工具、模式或配置。

行为规则见 `DESIGN.md`，包结构见 `ARCHITECTURE.md`。
