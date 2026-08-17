#!/usr/bin/env python3
"""对已安装工作流执行只读结构审计。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQUIRED_SKILLS = {
    "project-bootstrap",
    "focused-fix",
    "full-development",
    "sync-project-knowledge",
    "record-task-log",
    "spec-driven-change",
    "track-change-trace",
}

DAILY_FILE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
WORKLOG_HEADING = re.compile(
    r"^## (?:T-\S+ · )?(\d{2}:\d{2}:\d{2})[–-]\d{2}:\d{2}:\d{2} · L[0-5] ·"
)
LEGACY_SIMPLE_LOG = re.compile(
    r"^- (\d{2}:\d{2}:\d{2})[–-]\d{2}:\d{2}:\d{2} · L[01] ·"
)
TRACE_CHECKPOINT = re.compile(r"^### (\d{2}:\d{2}:\d{2}) ·")


def seconds(value: str) -> int:
    hour, minute, second = (int(part) for part in value.split(":"))
    return hour * 3600 + minute * 60 + second


def check_nondecreasing(
    path: Path, entries: list[tuple[int, str]], problems: list[str]
) -> None:
    previous: tuple[int, str] | None = None
    for line_number, value in entries:
        if previous is not None and seconds(value) < seconds(previous[1]):
            problems.append(
                f"{path}: 第 {line_number} 行时间 {value} 早于前一记录 {previous[1]}"
            )
        previous = (line_number, value)


def check_history_order(project: Path, problems: list[str]) -> None:
    worklogs = project / "docs" / "worklogs"
    if worklogs.is_dir():
        for path in sorted(worklogs.iterdir()):
            if not path.is_file() or not DAILY_FILE.fullmatch(path.name):
                continue
            entries: list[tuple[int, str]] = []
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                match = WORKLOG_HEADING.match(line)
                legacy = LEGACY_SIMPLE_LOG.match(line)
                if match:
                    entries.append((line_number, match.group(1)))
                elif legacy:
                    entries.append((line_number, legacy.group(1)))
                    problems.append(
                        f"{path}: 第 {line_number} 行 L0/L1 不是独立二级标题"
                    )
            check_nondecreasing(path, entries, problems)

    traces = project / "docs" / "traces"
    if traces.is_dir():
        for path in sorted(traces.iterdir()):
            if not path.is_file() or not DAILY_FILE.fullmatch(path.name):
                continue
            entries: list[tuple[int, str]] = []
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                match = TRACE_CHECKPOINT.match(line)
                if match:
                    entries.append((line_number, match.group(1)))
            check_nondecreasing(path, entries, problems)


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

    check_history_order(project, problems)

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
