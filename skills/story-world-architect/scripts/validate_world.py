#!/usr/bin/env python3
"""Validate structural invariants for story-world-architect artifacts."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SCOPE_ORDER = {"core": 0, "system": 1, "conflict": 2, "handoff": 3}
FIELD_RE = re.compile(r"^\s*[-*]\s+(?:\*\*)?([^：:]+?)(?:\*\*)?\s*[：:]\s*(.*?)\s*$")
HEADING_ID_RE = re.compile(
    r"^##\s+((?:RULE|INST|FAC|HIST|CON|SEED|WCR)-\d{3})\b.*$",
    re.IGNORECASE | re.MULTILINE,
)
ANY_ID_RE = re.compile(
    r"\b(?:RULE|INST|FAC|HIST|CON|SEED|WS|WCR)-\d{3}\b", re.IGNORECASE
)
PLACEHOLDER_RE = re.compile(
    r"\[(?:待确认|待补充)\]|\b(?:TODO|TBD)\b|\{[^{}\n]{0,80}\}", re.IGNORECASE
)
VERSION_RE = re.compile(r"^v\d+\.\d+(?:\.\d+)?(?:[-+][A-Za-z0-9._-]+)?$")


@dataclass
class Issue:
    level: str
    code: str
    path: str
    message: str


def safe_root(raw: str) -> Path:
    root = Path(raw).expanduser().resolve()
    if root.parent == root:
        raise ValueError("Refusing to validate a filesystem root.")
    return root


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def read_text(path: Path, issues: list[Issue], root: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        issues.append(Issue("error", "encoding", relative(path, root), "文件不是有效 UTF-8。"))
    except OSError as exc:
        issues.append(Issue("error", "read_error", relative(path, root), f"无法读取：{exc}"))
    return ""


def normalize_label(label: str) -> str:
    return re.sub(r"[\s*`_]+", "", label).lower()


def fields(text: str) -> dict[str, str]:
    found: dict[str, str] = {}
    for line in text.splitlines():
        match = FIELD_RE.match(line)
        if match:
            found[normalize_label(match.group(1))] = match.group(2).strip()
    return found


def add_missing_fields(
    path: Path,
    text: str,
    required: Iterable[str],
    issues: list[Issue],
    root: Path,
    level: str = "error",
) -> dict[str, str]:
    found = fields(text)
    for label in required:
        if normalize_label(label) not in found:
            issues.append(
                Issue(level, "missing_field", relative(path, root), f"缺少字段：{label}")
            )
    return found


def object_blocks(text: str) -> list[tuple[str, str]]:
    matches = list(HEADING_ID_RE.finditer(text))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(1).upper(), text[match.start():end]))
    return blocks


def discover_scope(world: Path) -> str:
    if (world / "15_大纲接口.md").exists():
        return "handoff"
    if (world / "13_剧情种子.md").exists():
        return "conflict"
    if any((world / name).exists() for name in ("03_物理与空间.md", "11_信息与治理能力.md")):
        return "system"
    return "core"


def world_files(world: Path) -> list[Path]:
    return sorted((path for path in world.glob("*.md") if path.is_file()), key=lambda p: p.name)


def require_files(
    world: Path, scope: str, issues: list[Issue], root: Path
) -> None:
    core = (
        "世界观索引.md",
        "世界观工作状态.md",
        "00_世界核心.md",
        "01_硬规则.md",
        "02_当前时代.md",
        "14_当前世界状态.md",
    )
    system = (
        "03_物理与空间.md",
        "04_资源与生态.md",
        "05_力量与技术.md",
        "06_经济与物流.md",
        "07_政治法律与制度.md",
        "08_社会阶层与文化.md",
        "09_历史债务.md",
        "10_势力网络.md",
        "11_信息与治理能力.md",
    )
    conflict = ("12_结构冲突.md", "13_剧情种子.md")
    handoff = ("15_大纲接口.md", "世界观变更.md")
    required = list(core)
    if scope == "system":
        required.extend(system)
    if SCOPE_ORDER[scope] >= SCOPE_ORDER["conflict"]:
        required.extend(conflict)
    if SCOPE_ORDER[scope] >= SCOPE_ORDER["handoff"]:
        required.extend(handoff)
    for name in required:
        path = world / name
        if not path.exists():
            issues.append(Issue("error", "missing_file", relative(path, root), "缺少目标范围要求的文件。"))


def validate(root: Path, scope: str, strict: bool) -> tuple[list[Issue], dict[str, int | str]]:
    issues: list[Issue] = []
    world = root / "设定" / "世界观"
    require_files(world, scope, issues, root)
    files = world_files(world) if world.exists() else []
    texts = {path: read_text(path, issues, root) for path in files}

    field_requirements: dict[str, tuple[str, ...]] = {
        "世界观索引.md": (
            "项目名", "深度", "世界观状态", "当前版本", "正典基线", "适用故事范围", "不展开范围", "权威来源"
        ),
        "00_世界核心.md": (
            "一句话世界命题", "类型承诺", "核心体验", "故事舞台", "时间跨度", "预计体量", "世界常态", "时代异常", "世界问题", "不可妥协设定", "允许调整项", "不展开范围"
        ),
        "02_当前时代.md": (
            "当前年份/纪年", "旧均衡", "变化触发器", "为什么是现在", "临界点", "若无人干预的趋势"
        ),
        "14_当前世界状态.md": ("状态基准时间", "世界观版本", "正典状态", "证据截止"),
        "15_大纲接口.md": (
            "接口状态", "接口模式", "接口版本", "世界观状态", "世界观版本", "正典基准时间", "来源索引", "当前状态文件", "适用故事范围", "不适用范围", "最近审计"
        ),
    }
    for name, required in field_requirements.items():
        path = world / name
        if path.exists():
            data = add_missing_fields(path, texts[path], required, issues, root)
            if name in {"世界观索引.md", "14_当前世界状态.md", "15_大纲接口.md"}:
                version_key = "当前版本" if name == "世界观索引.md" else "世界观版本"
                value = data.get(normalize_label(version_key), "")
                if value and not VERSION_RE.fullmatch(value.split()[0]):
                    issues.append(Issue("warning", "version_format", relative(path, root), f"{version_key} 建议使用 v1.0 形式。"))

    version_sources: dict[str, str] = {}
    for name, label in (
        ("世界观索引.md", "当前版本"),
        ("14_当前世界状态.md", "世界观版本"),
        ("15_大纲接口.md", "世界观版本"),
    ):
        path = world / name
        if path.exists():
            value = fields(texts[path]).get(normalize_label(label), "").strip()
            if value:
                version_sources[name] = value.split()[0]
    if len(set(version_sources.values())) > 1:
        detail = ", ".join(f"{name}={version}" for name, version in version_sources.items())
        issues.append(Issue("error", "world_version_drift", "设定/世界观", f"世界观版本未对齐：{detail}"))

    definitions: dict[str, Path] = {}
    objects: dict[str, tuple[Path, str]] = {}
    for path, text in texts.items():
        for object_id, block in object_blocks(text):
            if object_id in definitions:
                issues.append(
                    Issue("error", "duplicate_id", relative(path, root), f"ID {object_id} 已在 {relative(definitions[object_id], root)} 定义。")
                )
            else:
                definitions[object_id] = path
                objects[object_id] = (path, block)

    required_object_fields: dict[str, tuple[str, ...]] = {
        "RULE": (
            "ID", "状态", "正典级别", "作者真相", "世界内常见认知", "适用范围", "成立条件", "限制/风险/反制", "可观察证据", "执行者或制度反应", "例外及其来源", "受益者", "受损者", "日常生活影响", "剧情含义", "与其他规则关系", "来源"
        ),
        "INST": (
            "ID", "状态", "授权来源", "实际受益者", "执行者", "覆盖范围", "正常运行", "失败模式", "执法与申诉", "绕过成本", "尾部风险承担者"
        ),
        "FAC": (
            "ID", "状态", "公开目标", "真实目标", "资源与能力", "依赖对象", "主要约束", "常用策略", "可接受损失", "决策中心/内部激励"
        ),
        "CON": (
            "ID", "状态", "来源规则/制度", "争夺对象", "利益相关者", "各方目标", "持续供能", "为什么难以一次解决", "延续受益者", "外部性承担者", "当前阶段", "升级路径", "临界点", "可逆窗口", "可能的新均衡", "人物入口", "日常可见证据"
        ),
        "SEED": (
            "ID", "状态", "来源冲突", "类型/情绪回报", "触发器", "为什么是现在", "利益相关者", "个人入口", "初始诱因或损失", "两难选择", "失败代价", "升级向量", "潜在世界状态变化", "依赖", "禁止假设", "不预设的人物决定"
        ),
    }
    for object_id, (path, block) in objects.items():
        prefix = object_id.split("-", 1)[0]
        required = required_object_fields.get(prefix)
        if not required:
            continue
        data = add_missing_fields(path, block, required, issues, root)
        declared = data.get("id", "").upper()
        if declared and object_id not in declared:
            issues.append(Issue("error", "id_heading_mismatch", relative(path, root), f"标题 {object_id} 与 ID 字段 {declared} 不一致。"))
        if prefix == "RULE":
            canon = data.get(normalize_label("正典级别"), "").lower()
            if canon and canon not in {"hard", "soft", "belief", "open", "retired"}:
                issues.append(Issue("warning", "invalid_canon", relative(path, root), f"{object_id} 的正典级别不在约定枚举中。"))

    if SCOPE_ORDER[scope] >= SCOPE_ORDER["conflict"]:
        for prefix, filename in (("RULE", "01_硬规则.md"), ("CON", "12_结构冲突.md"), ("SEED", "13_剧情种子.md")):
            if not any(object_id.startswith(prefix + "-") for object_id in definitions):
                issues.append(Issue("error", "missing_object", f"设定/世界观/{filename}", f"目标范围至少需要一个 {prefix} 对象。"))

    reference_level = "error" if strict else "warning"
    known_ws = set(
        match.group(0).upper()
        for match in ANY_ID_RE.finditer(texts.get(world / "14_当前世界状态.md", ""))
        if match.group(0).upper().startswith("WS-")
    )
    known_ids = set(definitions) | known_ws
    reference_files = [world / name for name in ("12_结构冲突.md", "13_剧情种子.md", "15_大纲接口.md") if (world / name).exists()]
    for path in reference_files:
        text = texts[path]
        for match in ANY_ID_RE.finditer(text):
            object_id = match.group(0).upper()
            if object_id.startswith("WCR-"):
                continue
            if object_id not in known_ids:
                issues.append(Issue(reference_level, "invalid_reference", relative(path, root), f"引用未定义：{object_id}"))

    placeholder_count = 0
    for path, text in texts.items():
        matches = list(PLACEHOLDER_RE.finditer(text))
        if not matches:
            continue
        placeholder_count += len(matches)
        sample = ", ".join(sorted({match.group(0) for match in matches})[:3])
        issues.append(
            Issue("error" if strict else "warning", "placeholder", relative(path, root), f"存在 {len(matches)} 个未决占位符：{sample}")
        )

    counts: dict[str, int | str] = {
        "scope": scope,
        "files": len(files),
        "rules": sum(object_id.startswith("RULE-") for object_id in definitions),
        "institutions": sum(object_id.startswith("INST-") for object_id in definitions),
        "factions": sum(object_id.startswith("FAC-") for object_id in definitions),
        "conflicts": sum(object_id.startswith("CON-") for object_id in definitions),
        "seeds": sum(object_id.startswith("SEED-") for object_id in definitions),
        "placeholders": placeholder_count,
        "errors": sum(issue.level == "error" for issue in issues),
        "warnings": sum(issue.level == "warning" for issue in issues),
    }
    return issues, counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate worldbuilding artifact structure.")
    parser.add_argument("--root", required=True, help="Fiction project root")
    parser.add_argument(
        "--scope", choices=("auto", "core", "system", "conflict", "handoff"), default="auto"
    )
    parser.add_argument("--strict", action="store_true", help="Treat placeholders and broken references as errors")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    try:
        root = safe_root(args.root)
    except ValueError as exc:
        parser.error(str(exc))
    world = root / "设定" / "世界观"
    scope = discover_scope(world) if args.scope == "auto" else args.scope
    issues, counts = validate(root, scope, args.strict)

    if args.json:
        print(json.dumps({"root": str(root), "counts": counts, "issues": [asdict(issue) for issue in issues]}, ensure_ascii=False, indent=2))
    else:
        print(f"root={root}")
        print(f"scope={scope} strict={str(args.strict).lower()}")
        for issue in issues:
            print(f"[{issue.level.upper()}] {issue.code} {issue.path}: {issue.message}")
        print("summary " + " ".join(f"{key}={value}" for key, value in counts.items() if key != "scope"))

    return 1 if counts["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
