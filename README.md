![世界观架构师 · Story World Architect](assets/world-architect-hero.png)

# 小说世界观架构师 · Story World Architect

**简体中文** | [English](README_EN.md)

面向长篇小说与原创 IP 的世界构建 Agent Skill：建立规则、生产、权力、家庭与时代变迁的深层因果，并将严谨的内部设定编排成有烟火气、书籍观感舒适的读者向世界设定集（DOCX）。当前版本 **v1.4.1**。

默认采用**简体中文**推演与成稿；同时支持按你的要求切换为**英文（English）**、**繁体中文**或其他语言起笔，自动匹配目标语种的叙述语感与目录标题规范。

## 核心能力与设计取向

- **全周期世界构建**：支持从零构建世界、扩展既有设定、审查规则漏洞，以及随正文连载演进正典与时代状态。
- **社会与日常因果推演**：从核心约束出发，沿“资源分配 → 行为激励 → 制度形成 → 日常后果 → 持续压力”链条推演地域面貌、组织权力、阶层流动与普通人的柴米油盐。
- **创作锚点与目录先行**：动笔前对齐核心命题、四项创作锚点（现实参照、基准时间 T0、基调与救济尺度、货币与购买力口径）、按需细至四级的目录与篇幅预算，确认后连贯推进成稿。
- **内部正典与读者成稿分离**：内部工作台维护严密的规则编号、状态与兼容接口；读者版采用叙述式说明与简短生活事务切片，兼具可读性与设定查考价值。
- **母语质感与页面呼吸**：让人、机构与器物承担具体动作，消除政策摘要腔、空主语与机械正反四段论；交替长短段落、生活切片与简明对照小表，保持书页视觉清爽。
- **语言与日常肌理交接**：向下游大纲与正文同步输出称谓礼数、市井俗谚、行业行话、日常饮食器物与时代出戏词禁区，让人物一开口就长在世界里。
- **书籍级排版与闭环校验**：内置 A4 书籍感模板（宋体正文 + 微软雅黑标题 + 墨黛/黛蓝/玄灰/赭石暗金克制配色），自动生成最多四级目录与书签跳转，经 PDF 真实页码回填、文字边界核对与逐页 PNG 渲染验收后交付。

## 配套创作工作流

同系列六大技能既可独立使用，也可按体量与媒介串联成完整的小说与短剧创作管线：

- **长篇与精品小说三件套**
  1. **小说世界观架构师 · Story World Architect**：构建世界规则、社会生态、读者设定集与下游交接接口。
  2. [小说大纲架构师 · Story Outline Architect](https://github.com/LilHaopeng/story-outline-architect)：引用世界正典与冲突种子，设计故事弧、剧情段与具象章纲。
  3. [小说正文写作 · Story Prose Writer](https://github.com/LilHaopeng/story-prose-writer)：调用世界语言肌理与章纲，完成声口校准、正文撰写与跨章连续性审校。
- **市场雷达、高概念短篇与 AI 短剧工作流**
  4. [网文与短剧市场雷达 · Webnovel Market Radar](https://github.com/LilHaopeng/webnovel-market-radar)：短篇网文、长篇网文与 AI 短剧/漫剧三轨实时扫榜与选题简报生成。
  5. [短篇网文与微短剧爽文创作室 · Webnovel Short Studio](https://github.com/LilHaopeng/webnovel-short-studio)：5 万字以内高概念脑洞短篇（盐选/番茄短故事）与微短剧式分章爽文一体化创作。
  6. [AI 短剧与沙雕短剧编剧室 · AI Drama Script Studio](https://github.com/LilHaopeng/ai-drama-script-studio)：原生及小说改编 AI 短剧（MiniMax-H3）、2D/3D 高奇观漫剧与沙雕短剧视听剧本工作室。

## 安装方式

1. **通过 `skill-installer` 安装（Codex 等）**
   ```text
   $skill-installer 请从 https://github.com/LilHaopeng/story-world-architect 安装 skills/story-world-architect
   ```
2. **手动复制到本地技能目录（Antigravity / Claude Code / Codex / Cursor）**
   克隆本仓库，将 `skills/story-world-architect/` 完整复制到对应客户端的技能目录：
   - **Antigravity**：`~/.gemini/config/skills/story-world-architect`
   - **Claude Code**：`~/.claude/skills/story-world-architect`
   - **Codex**：`~/.codex/skills/story-world-architect` 或 `~/.agents/skills/story-world-architect`
   - **Cursor**：`~/.cursor/skills/story-world-architect`

## 快速上手

**默认简体中文新建设定集**：

```text
$story-world-architect
我想设计一个依赖季节迁徙维持生产的群岛世界。
先在对话中核对核心规则、时间与购买力尺度、按需细至四级的目录和篇幅，确认后交付读者向世界设定集 DOCX。
```

**指定英文或其他语言起笔**：

```text
$story-world-architect
Design a seasonal archipelago world in English. Review the core rules, four anchors, and a 4-level outline with me first, then compile the reader-facing World Compendium DOCX.
```

## 版本亮点

### v1.4.1：去机械节拍约束与有机叙事分布

- **有机章节编排与防同质化**：移除对生活切片与表格频率的机械硬性配额，改为按章节内容密度自然交替长短段落、制度推演与市井切片，防止多部设定集呈现同一种固定模具感。
- **全生态接口联动**：无缝衔接上游 `webnovel-market-radar` 长篇选题简报与下游 `ai-drama-script-studio` IP 漫剧改编。

### v1.4.0：书籍级排版美学、下游语言肌理交接与多语种支持

- **书籍级默认排版升级**：`reader-template.docx` 升级为标准 A4 开本、宋体 11.5 磅正文（暖墨黑 `#222222`、首行缩进 2 字符、1.48 倍行距）配微软雅黑四级标题，采用墨黛蓝（`#1B263B`）、黛蓝（`#2B4C7E`）、玄青灰（`#3D405B`）与赭石暗金（`#9C4A1A`）的克制书籍配色，告别办公汇报风。
- **下游语言与日常肌理切片**：`15_大纲接口.md` 新增称谓礼数、市井行话、饮食器物与时代违和词红线，直接赋能下游正文与人物对白。
- **页面视觉节律与多语种起笔**：强化长篇设定集的段落呼吸感与标点洁癖；默认简体中文写作，支持主动选择英文或其他语言起笔（`build_reader_docx.py` 与 `verify_reader_docx.py` 支持 `--toc-title Contents`）。

### v1.3.1：深化世界运行机制与多后端 PDF 兼容

- **运行机制三项检查**：支持资源—权力维持成本推演、条件化链式反馈、公开价值与实际行为落差分析，以及“无主角运行 / 移除核心设定”反事实诊断。
- **多后端 PDF 校验渲染**：已安装 `PyMuPDF (fitz)` 时自动优先使用；未安装时无缝切换至 `pypdf`（书签页码）+ `pdfplumber`（真实文字坐标与稀疏尾页检测）+ `pypdfium2 / Pillow`（逐页 PNG 渲染）。

## 辅助脚本与环境配置

仅通过对话推演世界观时无需运行脚本；使用自动化正典校验与排版级 DOCX 构建时，需 Python 3.10+ 并安装依赖（PDF 导出需本机具备 LibreOffice 或保留书签的导出工具）：

```bash
python -m pip install -r requirements.txt
```

| 脚本 | 功能说明 |
|---|---|
| `init_world_project.py` | 非破坏性初始化正典目录、模块骨架与创作锚点（支持 `--lang`、`--mode`、`--audience`） |
| `validate_world.py` | 校验内部字段、创作锚点、对象 ID（`RULE/INST/FAC/CON/SEED/LOOP/REG/CHAR`）与跨文件引用 |
| `lock_world.py` | 在定稿确认后创建不可覆盖的正典版本快照 |
| `extract_reader_template.py` | 从自定义参考 DOCX 提取干净样式模板并清理残留元数据 |
| `build_reader_docx.py` | 将 Markdown 编译为带封面与四级目录跳转的 DOCX，支持 `--pages-from-pdf` 与 `--toc-title` |
| `verify_reader_docx.py` | 核对源文覆盖、目录页码、书签跳转、样式槽位与页面文字边界，提示章末稀疏页 |
| `render_pdf_pages.py` | 将导出的 PDF 渲染为逐页 PNG 图像以便视觉检查 |

### 本地 DOCX 构建与真实页码同步示例

```bash
# 1. 初次构建 DOCX 并导出首轮 PDF 计算真实排版页码
python skills/story-world-architect/scripts/build_reader_docx.py --source worldbook.md --out worldbook.docx
mkdir -p qa/round1 qa/round2
soffice --headless --convert-to pdf --outdir qa/round1 worldbook.docx

# 2. 回填真实目录页码并导出最终 PDF
python skills/story-world-architect/scripts/build_reader_docx.py --source worldbook.md --out worldbook.docx --pages-from-pdf qa/round1/worldbook.pdf
soffice --headless --convert-to pdf --outdir qa/round2 worldbook.docx

# 3. 结构与版面校验 + 逐页渲染预览图
python skills/story-world-architect/scripts/verify_reader_docx.py --source worldbook.md --docx worldbook.docx --pdf qa/round2/worldbook.pdf --report qa/check.json
python skills/story-world-architect/scripts/render_pdf_pages.py --pdf qa/round2/worldbook.pdf --out qa/round2-pages
```

运行回归测试：

```bash
python -B -m unittest discover -s tests -v
```

## 隐私与许可证

所有辅助脚本均在本地工作区内读写文件，不会上传你的设定原稿。本仓库采用 [MIT License](LICENSE) 开源（Copyright © 2026 LilHaopeng）；外部依赖组件遵循各自上游许可证。
