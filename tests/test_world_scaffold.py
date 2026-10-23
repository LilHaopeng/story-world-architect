"""Canonical scaffold and structural validation; no private story inputs required."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "story-world-architect" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from validate_world import validate


LOOP = """## LOOP-001 重复申领窗口

- ID：LOOP-001
- 状态：draft
- 正典级别：open
- 来源规则或制度：RULE-001
- 成立条件：申请记录异步同步
- 获利者与受害者：申请者获利，地方预算承担损失
- 边界与限制：仅在同步前成立
- 代价：需要多次到场
- 证据或开放问题：是否实际出现尚未确认
"""

REGION = """## REG-001 山外地区

- ID：REG-001
- 状态：reviewed
- 正典级别：soft
- 主舞台对照：与山城相邻
- 共同规则：RULE-001
- 差异：地方采用不同结算周期
- 跨境路径：经陆路通行
- 来源：作者草案
"""

CHARACTER = """## CHAR-001 桥头修理者

- ID：CHAR-001
- 状态：active
- 正典级别：belief
- 当前位置：REG-001
- 出生年或年龄：约三十岁
- 资源来源：修理收入
- 当前活动：等待配件
- 来源：角色自述
"""


class WorldScaffoldTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="world-scaffold-test-")
        self.folder = Path(self.temporary.name)
        self.project = self.folder / "project"
        self.world = self.project / "设定" / "世界观"

    def tearDown(self):
        self.temporary.cleanup()

    def initialize(self, mode="compact"):
        return subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(SCRIPTS / "init_world_project.py"),
             "--root", str(self.project), "--title", "公开测试世界", "--mode", mode],
            check=True, text=True, encoding="utf-8", capture_output=True,
        )

    def write(self, name, text):
        path = self.world / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def complete_placeholders(self):
        for path in self.world.glob("*.md"):
            path.write_text(path.read_text(encoding="utf-8").replace("[待确认]", "尚未确定（open）"),
                            encoding="utf-8")

    def test_every_depth_creates_open_anchors_without_prescribing_a_world(self):
        for mode in ("compact", "standard", "deep"):
            with self.subTest(mode=mode):
                self.project = self.folder / mode
                self.world = self.project / "设定" / "世界观"
                self.initialize(mode)
                anchor = self.world / "00_创作锚点.md"
                self.assertTrue(anchor.is_file(), "every depth needs the author anchor scaffold")
                text = anchor.read_text(encoding="utf-8")
                for section in ("ANCHOR-REGIME", "ANCHOR-TIME", "ANCHOR-GRIT", "ANCHOR-CURRENCY"):
                    self.assertIn("## " + section, text)
                self.assertIn("- 状态：draft", text)
                self.assertIn("- 正典级别：open", text)
                self.assertNotIn("2056", text)
                self.assertEqual(len(list(self.world.glob("*.md"))), 11 if mode == "compact" else 20)

    def test_repeated_initialization_preserves_existing_anchor_bytes(self):
        self.initialize()
        anchor = self.world / "00_创作锚点.md"
        user_bytes = "# 作者已确认的锚点\r\n\r\n未来纪年仍未定。\r\n".encode("utf-8")
        anchor.write_bytes(user_bytes)
        before = {path.relative_to(self.project): path.read_bytes() for path in self.project.rglob("*") if path.is_file()}
        result = self.initialize("deep")
        self.assertIn("skipped=11", result.stdout)
        for path, content in before.items():
            self.assertEqual((self.project / path).read_bytes(), content)

    def test_legacy_project_without_anchors_is_valid(self):
        self.initialize()
        anchor = self.world / "00_创作锚点.md"
        if anchor.exists():
            anchor.unlink()
        self.complete_placeholders()
        issues, counts = validate(self.project, "handoff", True)
        self.assertEqual(counts["errors"], 0, issues)
        self.assertFalse(any(issue.code == "missing_file" and "创作锚点" in issue.path for issue in issues))

    def test_existing_anchors_need_each_named_section(self):
        self.initialize()
        self.write("00_创作锚点.md", "# 创作锚点\n\n- 状态：draft\n- 正典级别：open\n")
        issues, _ = validate(self.project, "core", False)
        missing = [issue for issue in issues if issue.code == "missing_anchor_section"]
        self.assertEqual(len(missing), 4)
        self.assertTrue(all(issue.level == "error" for issue in missing))

    def test_anchor_field_cannot_be_borrowed_from_another_section(self):
        self.initialize()
        self.write("00_创作锚点.md", """# 创作锚点

- 状态：draft
- 正典级别：open

## ANCHOR-REGIME

- 现实与文化参照：完全架空
- 政体与治理结构：多个地方共同体
- 命名口径：使用本地词源

## ANCHOR-TIME

- 发表偏好：仅为测试，放错了位置
- T0与纪年：冬至后的第一个月
- 历史分叉：尚未确定
- 人物出生与技术时间线：按相对时间记录

## ANCHOR-GRIT

- 基调：生活喜剧
- 救济资格：尚未确定
- 救济额度：尚未确定
- 救济申请与执行：尚未确定
- 代价与受益者：尚未确定

## ANCHOR-CURRENCY

- 法定货币与相对指数：只用生活成本指数
- 锚定地区：山城
- 锚定日期：T0
- 换算公式：一份日常餐食为一单位
- 未知项与未定项：不把未定币值写为硬事实
""")
        issues, _ = validate(self.project, "core", False)
        self.assertTrue(any(issue.code == "missing_field" and "ANCHOR-REGIME" in issue.message
                            and "发表偏好" in issue.message for issue in issues), issues)

    def test_optional_objects_are_defined_without_promoting_their_canon(self):
        self.initialize()
        self.write("16_可选对象.md", LOOP + "\n" + REGION + "\n" + CHARACTER)
        self.complete_placeholders()
        issues, counts = validate(self.project, "handoff", True)
        self.assertEqual(counts.get("loops"), 1)
        self.assertEqual(counts.get("regions"), 1)
        self.assertEqual(counts.get("characters"), 1)
        self.assertEqual(counts["errors"], 0, issues)
        self.assertFalse(any(issue.code == "invalid_canon" for issue in issues))

    def test_optional_objects_require_their_own_fields(self):
        self.initialize()
        cases = ((LOOP, "证据或开放问题"), (REGION, "跨境路径"), (CHARACTER, "出生年或年龄"))
        for complete, missing in cases:
            with self.subTest(missing=missing):
                incomplete = "\n".join(line for line in complete.splitlines() if not line.startswith("- " + missing + "："))
                self.write("16_可选对象.md", incomplete)
                issues, _ = validate(self.project, "core", False)
                self.assertTrue(any(issue.code == "missing_field" and missing in issue.message for issue in issues), issues)

    def test_dangling_references_in_any_top_level_canon_file_are_strict_errors(self):
        self.initialize()
        self.write("附加笔记.md", "# 附加笔记\n\n引用 RULE-999、LOOP-002、REG-003 与 CHAR-004。\n")
        self.complete_placeholders()
        issues, _ = validate(self.project, "core", True)
        dangling = [issue for issue in issues if issue.code == "invalid_reference"]
        self.assertEqual({issue.message.split("：")[-1] for issue in dangling},
                         {"RULE-999", "LOOP-002", "REG-003", "CHAR-004"})
        self.assertTrue(all(issue.level == "error" for issue in dangling))
        ordinary, _ = validate(self.project, "core", False)
        self.assertTrue(all(issue.level == "warning" for issue in ordinary if issue.code == "invalid_reference"))

    def test_reader_and_snapshot_subfolders_do_not_define_or_reference_canon(self):
        self.initialize()
        self.write("阅读版/正文.md", "# 正文\n\nCHAR-900 暂未出场。\n\n" + CHARACTER)
        self.write("版本/v0.0/旧稿.md", "# 旧稿\n\nLOOP-900 已废弃。\n" + LOOP)
        self.complete_placeholders()
        issues, counts = validate(self.project, "handoff", True)
        self.assertEqual(counts.get("characters"), 0)
        self.assertEqual(counts.get("loops"), 0)
        self.assertEqual(counts["errors"], 0, issues)

    def test_quoted_examples_are_not_object_definitions(self):
        self.initialize()
        self.write("附加笔记.md", """# 使用说明

普通叙述只提到 LOOP-700 和 CHAR-700，不定义它们。

> ## REG-700 引文里的示例
> - ID：REG-700

```markdown
## LOOP-800 代码块里的示例

- ID：LOOP-800
- 状态：draft
```
""")
        issues, counts = validate(self.project, "core", False)
        self.assertEqual(counts.get("loops"), 0)
        self.assertEqual(counts.get("regions"), 0)
        self.assertEqual(counts.get("characters"), 0)
        self.assertFalse(any(issue.code == "missing_field" and "附加笔记" in issue.path for issue in issues))


if __name__ == "__main__":
    unittest.main()
