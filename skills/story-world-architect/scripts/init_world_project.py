#!/usr/bin/env python3
"""Create a non-destructive story-world-architect project skeleton."""

from __future__ import annotations

import argparse
from pathlib import Path


def safe_root(raw: str) -> Path:
    root = Path(raw).expanduser().resolve()
    if root.parent == root:
        raise ValueError("Refusing to initialize a filesystem root.")
    return root


def module_template(name: str) -> str:
    return f"""# {name}

- 状态：draft
- 是否启用：是
- 与故事承诺的关系：[待确认]
- 权威来源：[待确认]

## 事实与约束

[待确认]

## 分配与流动

[待确认]

## 受益者、受损者与风险承担者

[待确认]

## 激励与常见策略

[待确认]

## 制度、执行能力与绕过路径

[待确认]

## 日常生活中的可见证据

[待确认]

## 对其他模块的二阶影响

[待确认]

## 可生成的冲突

[待确认]
"""


def templates(title: str, mode: str, audience: str = "reader") -> dict[str, str]:
    prefix = "设定/世界观/"
    base: dict[str, str] = {
        prefix + "世界观索引.md": f"""# 世界观索引

- 项目名：{title}
- 深度：{mode}
- 世界观状态：draft
- 当前版本：v0.1
- 正典基线：[待确认]
- 适用故事范围：[待确认]
- 不展开范围：[待确认]
- 权威来源：[待确认]
- 交付对象：{audience}

## 模块路由

| 文件 | 是否启用 | 为什么影响故事 | 权威来源 | 最近更新 |
|---|---|---|---|---|
""",
        prefix + "世界观工作状态.md": """# 世界观工作状态

- 工作模式：create
- 当前阶段：Stage 0
- 当前活动模块：[待确认]
- 已确认内容：无
- 最新锁定版本：无
- 与大纲接口状态：未生成
- 最新 DOCX 交付：无
- 读者版正文：无
- 来源冲突：无
- 研究项：无
- 待确认：[待确认]
""",
        prefix + "00_世界核心.md": """# 世界核心

- 状态：draft
- 一句话世界命题：[待确认]
- 类型承诺：[待确认]
- 核心体验：[待确认]
- 故事舞台：[待确认]
- 时间跨度：[待确认]
- 预计体量：[待确认]
- 世界常态：[待确认]
- 时代异常：[待确认]
- 世界问题：[待确认]
- 不可妥协设定：[待确认]
- 允许调整项：[待确认]
- 不展开范围：[待确认]

## 因果总链

| 起始约束 | 分配结果 | 行为激励 | 稳定它的制度 | 累积压力 | 结构冲突 | 日常可见证据 |
|---|---|---|---|---|---|---|
""",
        prefix + "01_硬规则.md": """# 硬规则

## RULE-001 规则名

- ID：RULE-001
- 状态：draft
- 正典级别：hard
- 作者真相：[待确认]
- 世界内常见认知：[待确认]
- 适用范围：[待确认]
- 成立条件：[待确认]
- 限制/风险/反制：[待确认]
- 可观察证据：[待确认]
- 执行者或制度反应：[待确认]
- 例外及其来源：[待确认]
- 受益者：[待确认]
- 受损者：[待确认]
- 日常生活影响：[待确认]
- 剧情含义：[待确认]
- 与其他规则关系：[待确认]
- 来源：[待确认]
""",
        prefix + "02_当前时代.md": """# 当前时代

- 状态：draft
- 当前年份/纪年：[待确认]
- 旧均衡：[待确认]
- 变化触发器：[待确认]
- 为什么是现在：[待确认]
- 失效中的制度：[待确认]
- 新受益者：[待确认]
- 新受损者：[待确认]
- 临界点：[待确认]
- 公众感知：[待确认]
- 各势力认知差：[待确认]
- 若无人干预的趋势：[待确认]
""",
        prefix + "12_结构冲突.md": """# 结构冲突

## CON-001 冲突名

- ID：CON-001
- 状态：active
- 来源规则/制度：RULE-001
- 争夺对象：[待确认]
- 利益相关者：[待确认]
- 各方目标：[待确认]
- 持续供能：[待确认]
- 为什么难以一次解决：[待确认]
- 延续受益者：[待确认]
- 外部性承担者：[待确认]
- 当前阶段：[待确认]
- 升级路径：[待确认]
- 临界点：[待确认]
- 可逆窗口：[待确认]
- 可能的新均衡：[待确认]
- 人物入口：[待确认]
- 日常可见证据：[待确认]
""",
        prefix + "13_剧情种子.md": """# 剧情种子

## SEED-001 种子名

- ID：SEED-001
- 状态：active
- 来源冲突：CON-001
- 类型/情绪回报：[待确认]
- 触发器：[待确认]
- 为什么是现在：[待确认]
- 利益相关者：[待确认]
- 个人入口：[待确认]
- 初始诱因或损失：[待确认]
- 两难选择：[待确认]
- 失败代价：[待确认]
- 升级向量：[待确认]
- 潜在世界状态变化：[待确认]
- 依赖：RULE-001
- 禁止假设：[待确认]
- 可组合种子：[待确认]
- 不预设的人物决定：[待确认]
""",
        prefix + "14_当前世界状态.md": """# 当前世界状态

- 状态基准时间：[待确认]
- 世界观版本：v0.1
- 正典状态：draft
- 证据截止：[待确认]

| State ID | 对象 | 当前状态 | 来源规则/事件 | 可观察证据 | 趋势 | 可逆性 | 最近更新 |
|---|---|---|---|---|---|---|---|
| WS-001 | [待确认] | [待确认] | RULE-001 | [待确认] | [待确认] | [待确认] | [待确认] |

## 当前压力排序

| 排名 | 压力 | 受影响对象 | 临界点 | 预计传播时延 |
|---:|---|---|---|---|
""",
        prefix + "15_大纲接口.md": """# 世界观 → 大纲接口

- 接口状态：draft
- 接口模式：world-first
- 接口版本：1
- 世界观状态：draft
- 世界观版本：v0.1
- 正典基准时间：[待确认]
- 来源索引：设定/世界观/世界观索引.md
- 当前状态文件：设定/世界观/14_当前世界状态.md
- 适用故事范围：[待确认]
- 不适用范围：[待确认]
- 最近审计：未审计

## 类型与体验边界

- 世界可稳定支持的类型承诺：[待确认]
- 核心体验：[待确认]
- 体量建议及理由：[待确认]
- 不应被大纲破坏的体验：[待确认]

## 锁定硬规则

| Rule ID | 摘要 | 正典级别 | 对大纲的约束 | 允许的例外/变更路径 |
|---|---|---|---|---|
| RULE-001 | [待确认] | hard | [待确认] | 通过 WCR 变更 |

## 可调整与开放项

| 对象 | 状态 | 可调整范围 | 必须确认的边界 |
|---|---|---|---|

## 当前时代与“为什么是现在”

- 旧均衡：[待确认]
- 变化触发器：[待确认]
- 当前危机：[待确认]
- 临界点：[待确认]
- 无人干预趋势：[待确认]

## 可选结构冲突

| Conflict ID | 争夺对象 | 利益相关者 | 持续供能 | 个人入口 | 升级/新均衡 |
|---|---|---|---|---|---|
| CON-001 | [待确认] | [待确认] | RULE-001 | [待确认] | [待确认] |

## 可选剧情种子

| Seed ID | 来源冲突 | 触发器 | 个人入口 | 两难与代价 | 状态变化潜力 | 类型回报 |
|---|---|---|---|---|---|---|
| SEED-001 | CON-001 | [待确认] | [待确认] | [待确认] | [待确认] | [待确认] |

## 势力与个人机会

| Faction ID | 可进入的身份/关系/债务 | 可提供资源 | 会施加的约束 | 信息盲区 |
|---|---|---|---|---|

## 信息边界

- 作者真相：[待确认]
- 公众认知：[待确认]
- 主角开篇可知范围：[待确认]
- 可公平铺垫但暂不揭示的内容：[待确认]

## 禁止假设

- 禁止无依据绕过的规则：[待确认]
- 禁止提前成立的技术/制度/关系：[待确认]
- 禁止把 belief 当 hard truth 的条目：[待确认]

## 世界状态读取点

| State ID | 开篇状态 | 大纲可施加的压力 | 可能变化方向 | 必须记录的二阶后果 |
|---|---|---|---|---|
| WS-001 | [待确认] | [待确认] | [待确认] | [待确认] |

## 开放问题与研究项

| 项目 | 为什么影响大纲 | 最迟确认层级 | 临时处理 |
|---|---|---|---|

## 兼容性声明

- 已确认兼容的大纲版本：无
- 已知冲突：[待确认]
- 下次世界观版本变化时必须复核：[待确认]
""",
        prefix + "世界观变更.md": """# 世界观变更记录

> hard 规则、时代危机、主要制度/势力或锁定接口的变化先登记 WCR，再同步下游。
""",
    }

    if mode in {"standard", "deep"}:
        modules = {
            "03_物理与空间.md": "物理与空间",
            "04_资源与生态.md": "资源与生态",
            "05_力量与技术.md": "力量与技术",
            "06_经济与物流.md": "经济与物流",
            "07_政治法律与制度.md": "政治法律与制度",
            "08_社会阶层与文化.md": "社会阶层与文化",
            "09_历史债务.md": "历史债务",
            "10_势力网络.md": "势力网络",
            "11_信息与治理能力.md": "信息与治理能力",
        }
        base.update({prefix + filename: module_template(name) for filename, name in modules.items()})

    return base


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create missing files for a story-world-architect project."
    )
    parser.add_argument("--root", required=True, help="Fiction project root")
    parser.add_argument("--title", default="未命名小说", help="Project title")
    parser.add_argument(
        "--mode",
        choices=("compact", "standard", "deep"),
        default="standard",
        help="Worldbuilding artifact depth",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show actions without writing")
    parser.add_argument("--audience", choices=("reader", "author", "handoff"), default="reader", help="Intended deliverable; does not change canon validation")
    args = parser.parse_args()

    try:
        root = safe_root(args.root)
    except ValueError as exc:
        parser.error(str(exc))

    files = templates(args.title.strip() or "未命名小说", args.mode, args.audience)
    world = root / "设定" / "世界观"
    directories = {world, world / "版本"}
    if args.mode == "deep":
        directories.update({world / "研究", world / "模拟"})

    created: list[Path] = []
    skipped: list[Path] = []
    for directory in sorted(directories, key=str):
        if not args.dry_run:
            directory.mkdir(parents=True, exist_ok=True)

    for relative, content in files.items():
        destination = root / Path(relative)
        if destination.exists():
            skipped.append(destination)
            continue
        created.append(destination)
        if args.dry_run:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(content.rstrip() + "\n")

    print(f"root={root}")
    print(f"mode={args.mode}")
    print(f"created={len(created)}")
    for path in created:
        print(f"  + {path.relative_to(root)}")
    print(f"skipped={len(skipped)}")
    for path in skipped:
        print(f"  = {path.relative_to(root)}")
    if args.dry_run:
        print("dry_run=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
