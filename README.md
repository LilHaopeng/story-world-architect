![世界观架构师 · Story World Architect](assets/world-architect-hero.png)

# 小说世界观架构师 · Story World Architect

面向中文小说与原创 IP 的通用 Agent Skill：帮助你构建自洽运转的世界，并将严谨的底层设定编排成有生活质感、适合读者与爱好者阅读的世界设定集。可按 OpenAI Codex、Claude Code、Cursor 等宿主的技能规范安装；脚本运行仍取决于宿主提供的执行权限、依赖与字体。

## 核心能力与设计取向

- **全周期世界构建**：支持从零构建世界、扩展已有设定、审查规则漏洞，以及随剧情推进维护正典与时代状态。
- **社会与日常因果推演**：从特殊规则出发，推演其对地域面貌、生产资源、组织权力、阶层流动、家庭结构与日常生活习惯的连锁影响。
- **创作锚点与目录先行**：动笔前先核对核心命题、四项创作锚点、按需细至四级的目录与篇幅预算；方案确认后连贯推进成稿，避免反复打断。
- **内部正典与读者成稿分离**：内部维护严密的规则编号、状态与大纲接口；读者版则采用叙述式说明与少量生活片段，既有可读性又保持设定集定位。
- **自然中文与节奏控制**：控制连续阅读的信息密度，避免机械填表、翻译腔或重复说理，根据空间、制度、历史与人物切换合适的观察视角。
- **尊重作品基调**：补足制度起源、技术冲击、灰色地带与跨地域差异，贴合你设定的世界冷暖基调与救济尺度，不套用固定模板。
- **排版构建与核对**：生成带封面、最多四级目录及正文的 DOCX 文档，经 PDF 导出回填真实页码，配合脚本核对文本覆盖、目录跳转与版面边界，再逐页检查视觉效果。

**适用边界**：本技能专注于世界观架构、设定集编排与大纲接口交接，不直接代写小说正文；自动化脚本负责结构、引用与排版数据校验，而世界观的逻辑推演、文风打磨与最终版面效果则由创作者与模型共同把关。

## 安装与跨平台支持

本技能采用 Agent Skills 目录结构（`SKILL.md` + `references/` + `scripts/` + `assets/`）。技能规范可移植，不代表各宿主的安装位置、调用语法或脚本权限完全一致：

1. **通过 `skill-installer` 安装（OpenAI Codex 等）**
   ```text
   $skill-installer 请从 https://github.com/LilHaopeng/story-world-architect 安装 skills/story-world-architect
   ```
2. **本地或项目目录安装（Codex / Claude Code / Cursor 等）**
   克隆本仓库，将 `skills/story-world-architect/` 整个文件夹复制到相应宿主的技能目录：

   | 宿主 | 项目目录 | 个人目录 |
   | --- | --- | --- |
   | [Codex](https://learn.chatgpt.com/docs/build-skills) | `.agents/skills/` | `~/.agents/skills/` |
   | [Claude Code](https://code.claude.com/docs/en/skills) | `.claude/skills/` | `~/.claude/skills/` |
   | [Cursor](https://cursor.com/docs/skills) | `.cursor/skills/` 或 `.agents/skills/` | `~/.cursor/skills/` 或 `~/.agents/skills/` |

   若本地已有修改过的同名技能，更新前先做好备份。目录规则以对应客户端当前文档为准。
3. **云端 Agent 技能管理器**
   按平台要求打包或导入完整的 `skills/story-world-architect` 目录；不要假定平台会自动识别整个仓库中的嵌套技能。云端会话是否加载本地技能、能否执行 Python，须分别核对。

复制或导入时请保留完整技能目录（含 `SKILL.md`、`references/`、`scripts/`、`assets/`、`agents/` 等）。`agents/openai.yaml` 是 OpenAI 宿主的可选界面元数据；其他宿主主要读取 `SKILL.md` 及其引用资源。安装后若未显示，请检查目录、权限及宿主的刷新或重启要求。

## 快速上手

新建世界设定集：

以下是 Codex 调用示例；Claude Code 可用 `/story-world-architect`，其他宿主按自身技能选择器或调用语法启用。

```text
$story-world-architect
我想设计一个依赖季节迁徙维持生产的群岛世界。
先在对话中核对核心规则、时间与尺度、按需细至四级的目录和篇幅，不要直接写小说剧情。
最终希望交付读者向世界设定集 DOCX。
```

用于已有项目时，可直接提供当前正典或参考文档，指定仅做规则审查、增量修订或重编读者版：

- **日常审查与目录讨论**：直接在对话中完成，仅在你需要交付文档时才生成 DOCX。
- **版本锁定**：当你确认设定定稿并明确指令锁版时，才会创建正典快照。

## 版本更新

### v1.3.1：深化世界运行机制与多后端沙盒兼容

在既有工作流基础上强化了社会运行的深层推演，并升级了跨平台 PDF 校验与渲染兼容性，向下兼容已有作品正典、四级目录与默认排版：

- **资源—权力反馈**：梳理优势地位的维持条件与运转成本，推演技术替代、合作或竞争如何打破既有循环。
- **条件化链式推演**：追踪规则成立的前提、参与者的应对策略与传播时延，呈现多元的演变方向。
- **价值—行为落差**：区分公开倡导的规范、实际执行的奖惩、私人信念与受限选择，保留文化与阶层内部的真实分歧。
- **反事实检查**：按需检验“无主角介入时世界如何运转”以及“移除核心设定后哪些选择会改变”，让设定真正融入世界肌理。
- **多后端 PDF 兼容**：已有 `PyMuPDF (fitz)` 时优先使用；否则分别由 `pypdf` 读取标题大纲、`pdfplumber` 测量真实文字坐标、`pypdfium2` 配合 `Pillow` 渲染页面。另支持 `pdf2image` 渲染，但需要 Poppler。缺少坐标后端时明确报错，不用估算坐标冒充版面校验。

详细推演方法见 [创作锚点与运行机制](skills/story-world-architect/references/design-anchors.md)。

### v1.3.0：创作锚点、读者编排与四级目录

- **四项创作锚点**：支持核对现实与文化参照、叙事基准时间（T0）与历史分岔、世界基调与救济尺度、货币与相对购买力。未定项可保持开放或使用相对尺度。
- **制度与压力推演**：补齐制度的发起、采纳与阻力链条，追踪技术变化对既有义务的冲击；支持按需记录漏洞与套利路径（`LOOP`）、地域对照（`REG`）与跨章人物连续性（`CHAR`）。
- **读者向文风优化**：强化具体、自然的中文表达，集中讲透核心机制，提早点明跨地域差异，让人物自然融入场景与事务。
- **四级目录与版面告警**：支持 `Heading 1–4` 与 `Contents 1–4` 及旧模板样式补齐；自动提示章末稀疏页，供创作者按需调整。

## 辅助脚本与环境配置

仅使用对话指令进行世界观推演和文本创作时，无需安装或运行任何 Python 脚本。当你需要自动化正典校验或生成排版级 DOCX 时，可使用配套脚本（需 Python 3.10+）。

从仓库根目录安装依赖：

```bash
python -m pip install -r requirements.txt
```

- **默认依赖**：`python-docx`、`lxml`、`pypdf`、`pdfplumber`、`pypdfium2`、`Pillow`，无需安装 PyMuPDF。
- **可选后端**：本地已有 `PyMuPDF (fitz)` 时自动优先使用；`pdf2image` 可替代页面渲染，但还需安装 Poppler 并配置 PATH。只有其中任意一个 PDF 包，并不足以完成全套流程。
- **其他运行条件**：DOCX 转 PDF 仍需 LibreOffice 或其他保留标题书签的导出器；字体、文件权限与宿主执行权限也须就绪。自动回退仅处理后端未安装，不掩盖损坏 PDF 或已安装后端的运行错误。
- **安装位置**：单独安装技能目录时，运行 `python -m pip install -r <技能目录>/requirements.txt`。仓库根目录的 requirements.txt 会引用同一份依赖清单。

| 阶段 | 首选后端（已安装时） | 替代后端与条件 |
| --- | --- | --- |
| 标题大纲与页码 | PyMuPDF | pypdf |
| 文字坐标、字体与稀疏页核对 | PyMuPDF | pdfplumber；不能用 pypdf 的纯文字结果代替坐标 |
| PDF 逐页 PNG | PyMuPDF | pypdfium2 + Pillow；或 pdf2image + Poppler |

| 脚本 | 功能说明 |
| --- | --- |
| `init_world_project.py` | 初始化项目结构，补充缺失的内部正典与创作锚点文件（不覆盖已有原稿） |
| `validate_world.py` | 校验内部正典字段、创作锚点、对象 ID 与跨文件引用，兼容旧版项目结构 |
| `lock_world.py` | 在确认定稿后创建不可覆盖的正典版本快照 |
| `extract_reader_template.py` | 从参考 DOCX 中提取字号、配色与段落样式，生成干净的可复用模板 |
| `build_reader_docx.py` | 将读者向 Markdown 编译为带封面与目录跳转的 DOCX，并根据渲染 PDF 同步真实页码 |
| `verify_reader_docx.py` | 核对源文覆盖率、标题层级、目录页码、书签跳转与版面边界，提示章末稀疏页 |
| `render_pdf_pages.py` | 将导出的 PDF 渲染为逐页 PNG 图像，便于直观检查最终版面 |

完整参数说明可查看各脚本的 `--help` 或 [DOCX 交付规范](skills/story-world-architect/references/docx-delivery.md)。

### 本地 DOCX 构建与页码同步流程

DOCX 构建器支持标准 UTF-8 Markdown 的正文段落、1–4 级标题、基础列表、行内强调与比较表格（遇到图片、代码块或复杂嵌套格式时会主动提示，避免静默丢失格式）。

以 `worldbook.md`（首行为 `# 书名`，正文使用连贯的 1–4 级标题）为例，在仓库根目录执行以下流程即可完成构建、真实页码回填与逐页预览（PDF 转换需环境装有 [LibreOffice](https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html) 或支持保留书签的导出工具）：

```bash
# 1. 初次构建 DOCX（此时目录页码为占位符）
python skills/story-world-architect/scripts/build_reader_docx.py --source worldbook.md --out worldbook.docx

# 2. 导出首轮 PDF 以计算真实排版页码
mkdir -p qa/round1 qa/round2
soffice --headless --convert-to pdf --outdir qa/round1 worldbook.docx

# 3. 根据首轮 PDF 回填真实目录页码，并生成最终 PDF
python skills/story-world-architect/scripts/build_reader_docx.py --source worldbook.md --out worldbook.docx --pages-from-pdf qa/round1/worldbook.pdf
soffice --headless --convert-to pdf --outdir qa/round2 worldbook.docx

# 4. 校验文档完整性并渲染逐页预览图
python skills/story-world-architect/scripts/verify_reader_docx.py --source worldbook.md --docx worldbook.docx --pdf qa/round2/worldbook.pdf --report qa/check.json
python skills/story-world-architect/scripts/render_pdf_pages.py --pdf qa/round2/worldbook.pdf --out qa/round2-pages
```

以上命令示例使用 Bash；PowerShell 用户可用 `New-Item -ItemType Directory -Force qa/round1, qa/round2` 创建目录，并按本机安装位置调用 LibreOffice。若回填后分页变化，应继续用最新 PDF 回填、重新导出并核对，直到页码稳定；两轮并不保证收敛。

## 默认排版与自定义模板

内置默认模板（[reader-template.docx](skills/story-world-architect/assets/reader-template.docx)）可直接使用：

- **字体与字号**：正文采用微软雅黑 12 磅，四级标题分别为 18 / 16 / 14 / 12.5 磅，目录项为 12 / 11 / 10.5 / 10 磅。
- **视觉细节**：第四级标题采用琥珀金棕（`#C55A11`）点缀，自带页眉与页码。

如果你有偏好的排版风格，可通过 `extract_reader_template.py` 提取自己的参考文档样式并优先应用。由于模板仅记录字体名称，跨设备渲染时请确保本地已安装对应字体，以获得一致的分页效果。

## 数据隐私与本地运行

- **本地处理**：所有辅助脚本均在本地或当前沙盒内读写文件，不会上传你的设定原稿；你的原创世界观与文稿版权完全归你个人所有。
- **分享提示**：自动生成的验证报告（如 `artifact.json`、`check.json`）及 `qa/` 目录可能包含本地文件路径，公开分享或提交代码前建议将测试输出与个人原稿排除在外。

## 测试与贡献

运行单元测试：

```bash
python -B -m unittest discover -s tests -v
```

默认依赖即可运行新增的替代后端回归用例。部分历史 PDF 夹具使用可选的 PyMuPDF：未安装时这些用例会明确跳过；如需完整执行它们，可另行安装 PyMuPDF，并核对其上游许可。替代后端测试会主动屏蔽 fitz，避免因环境预装 PyMuPDF 而漏测回退路线。

本次验证范围是 Windows 下的脚本回归与后端切换，不等于已在 Claude Code、Cursor、所有云端沙盒或其他操作系统中完成端到端验收。

欢迎提交 Issue 或 Pull Request 分享改进建议。反馈排版或脚本问题时，附上最小复现文本即可，无需提供私人原稿。

## 许可证

本仓库的创作规范、原创脚本与通用模板采用 [MIT License](LICENSE) 开源（Copyright © 2026 LilHaopeng）。第三方依赖及其随附组件保留各自的许可，不因本仓库采用 MIT 而改变；分发或部署时请核对实际安装版本的许可与声明。可选 [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/about.html) 后端遵循其上游许可条件，不包含在本仓库的 MIT 授权中。
