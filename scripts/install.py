#!/usr/bin/env python3
"""将可移植工作流安装到仓库，同时保留项目自身规则。"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

MANAGED_START = "<!-- adaptive-agent-development:managed:start -->"
MANAGED_END = "<!-- adaptive-agent-development:managed:end -->"
PROJECT_START = "<!-- adaptive-agent-development:project:start -->"
PROJECT_END = "<!-- adaptive-agent-development:project:end -->"


def marked_block(text: str, start: str, end: str) -> str:
    left = text.index(start)
    right = text.index(end, left) + len(end)
    return text[left:right]


def compose_agents(source: str, existing: str | None, merge: bool) -> str:
    managed = marked_block(source, MANAGED_START, MANAGED_END)
    if existing is None:
        project = (
            f"{PROJECT_START}\n## 项目专属规则\n\n"
            "请在这里填写项目硬性约束、文档权威关系、架构不变量和验证阶梯。\n"
            f"{PROJECT_END}"
        )
        return f"# 自适应 Agent 开发工作流\n\n{managed}\n\n{project}\n"
    if MANAGED_START in existing and MANAGED_END in existing:
        old = marked_block(existing, MANAGED_START, MANAGED_END)
        refreshed = existing.replace(old, managed, 1)
        legacy_title = "# Adaptive agent development workflow\n"
        if refreshed.startswith(legacy_title):
            refreshed = "# 自适应 Agent 开发工作流\n" + refreshed[len(legacy_title) :]
        return refreshed
    if not merge:
        raise ValueError("AGENTS.md 已存在但没有工作流标记；请使用 --merge 重新运行")
    local = existing.strip()
    project = (
        f"{PROJECT_START}\n## 项目专属规则\n\n"
        f"{local}\n{PROJECT_END}"
    )
    return f"# 自适应 Agent 开发工作流\n\n{managed}\n\n{project}\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--merge", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    package = Path(__file__).resolve().parent.parent
    project = args.project.resolve()
    if not project.is_dir():
        raise SystemExit(f"项目目录不存在：{project}")

    agents_path = project / "AGENTS.md"
    existing = agents_path.read_text(encoding="utf-8") if agents_path.exists() else None
    try:
        agents_text = compose_agents(
            (package / "AGENTS.md").read_text(encoding="utf-8"), existing, args.merge
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    installed_skills = project / ".agents" / "skills"
    conflicts = [
        path.name
        for path in (package / "skills").iterdir()
        if (installed_skills / path.name).exists()
    ]
    if conflicts and not args.force:
        raise SystemExit(
            "以下 Skill 已安装；请使用 --force 重新运行：" + ", ".join(conflicts)
        )

    actions = [f"写入 {agents_path}"]
    actions.extend(
        f"安装 Skill {path.name}" for path in sorted((package / "skills").iterdir())
    )
    actions.append(f"写入 {project / '.agents' / 'workflow.json'}")
    if args.dry_run:
        print("\n".join(actions))
        return 0

    # 修改根 AGENTS.md 前先预检工作流目录，避免宿主限制隐藏目录时留下半安装状态。
    installed_skills.mkdir(parents=True, exist_ok=True)
    agents_path.write_text(agents_text, encoding="utf-8")
    for skill in (package / "skills").iterdir():
        target = installed_skills / skill.name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(skill, target)
    manifest = json.loads((package / "workflow.json").read_text(encoding="utf-8"))
    (project / ".agents" / "workflow.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print("\n".join(actions))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
