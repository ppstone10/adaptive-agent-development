#!/usr/bin/env python3
"""对已安装工作流执行只读结构审计。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_SKILLS = {
    "project-bootstrap",
    "focused-fix",
    "full-development",
    "sync-project-knowledge",
    "record-task-log",
    "track-change-trace",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    project = args.project.resolve()

    problems: list[str] = []
    agents = project / "AGENTS.md"
    if not agents.exists():
        problems.append("缺少 AGENTS.md")
    elif "adaptive-agent-development:managed:start" not in agents.read_text(
        encoding="utf-8"
    ):
        problems.append("AGENTS.md 中没有受管工作流区块")

    manifest_path = project / ".agents" / "workflow.json"
    version = "未知"
    if not manifest_path.exists():
        problems.append("缺少 .agents/workflow.json")
    else:
        try:
            version = json.loads(manifest_path.read_text(encoding="utf-8"))["version"]
        except (json.JSONDecodeError, KeyError):
            problems.append("工作流清单无效")

    skill_root = project / ".agents" / "skills"
    for name in sorted(REQUIRED_SKILLS):
        if not (skill_root / name / "SKILL.md").is_file():
            problems.append(f"缺少 Skill：{name}")

    existing_docs = [
        name
        for name in ("README.md", "DESIGN.md", "ARCHITECTURE.md", "LEARNING.md")
        if (project / name).exists()
    ]
    print(f"工作流版本：{version}")
    print("项目文档：" + (", ".join(existing_docs) if existing_docs else "无"))
    if problems:
        print("状态：不完整")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("状态：已安装")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
