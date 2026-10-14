# 小说世界观架构师 · Story World Architect

面向中文小说与原创 IP 的 Codex skill：建立能运转的世界，并把严谨设定编排成有生活质感、适合爱好者阅读的世界设定集。

当前公开版本：**1.2.1**。公开版增加了依赖说明、通用渲染路线与模板元数据清理，不包含私人小说、用户原稿或内部项目记录。

## 能做什么

- 从构思新建世界，扩展已有设定，审查规则漏洞，维护正典与时代状态。
- 推演特殊规则怎样影响地域、生产、组织、权力、阶层、家庭、文化与日常生活。
- 先核对核心设定、详细三级目录和篇幅预算，再填充读者正文；已确认方案不反复询问。
- 区分作者内部正典和读者成稿。读者版采用理性叙述与少量事务片段，不写成规则字典，也不强制变成小说剧情。
- 控制连续阅读的信息强度，减少重复论证、人物工具化和机械字段。
- 生成包含封面、三级带页码目录及正文的 DOCX，检查源文覆盖、目录跳转、字体与可测布局问题。

它不直接代写小说章节，也不保证设定天然正确。自动检查不能代替因果推演、连续阅读审查和逐页视觉验收。

## 安装到 Codex

在支持 skill-installer 的 Codex 中发送：

```text
$skill-installer 请从 https://github.com/LilHaopeng/story-world-architect 安装 skills/story-world-architect
```

也可以克隆仓库，将 `skills/story-world-architect/` 整个文件夹复制到当前 Codex 支持的个人或项目 skills 目录。当前官方文档列出的目录包括 `~/.agents/skills/` 和项目的 `.agents/skills/`。请勿覆盖自己改过的同名 skill；更新前保留副本。

安装范围必须包含该文件夹内的 `SKILL.md`、`references/`、`scripts/`、`assets/`、`agents/`、`LICENSE` 和依赖清单，不能只复制入口文件。

参考：[OpenAI 官方 Skills 文档](https://learn.chatgpt.com/docs/build-skills)。未显示新 skill 时，可重启 Codex。

## 开始使用

```text
$story-world-architect
我想设计一个依赖季节迁徙维持生产的群岛世界。
先在对话中核对核心规则、三级目录和篇幅，不要直接写小说剧情。
最终希望交付读者向世界设定集 DOCX。
```

已有项目可以提供当前正典和参考文档，要求只审查、增量修订或重编读者版。审查和目录讨论不会自动生成 DOCX；锁定正典需要用户明确确认。

## 脚本与环境

只使用创作指令时不必运行脚本。辅助脚本使用 Python 3.10+；公开版在 Python 3.14、python-docx 1.2.0、lxml 6.1.1、PyMuPDF 1.28.0 环境中检查。其他平台仍需自行验证字体与版面。

从仓库根目录安装依赖：

```bash
python -m pip install -r requirements.txt
```

在 Codex 提供工作区依赖加载器时，优先使用其解释器和库，不要重复安装或改变全局环境。一般 Python 环境则建议自行创建虚拟环境。

| 脚本 | 用途 |
| --- | --- |
| `init_world_project.py` | 只创建缺失的内部正典文件，默认读者向 |
| `validate_world.py` | 核对内部字段、对象 ID 与引用 |
| `lock_world.py` | 经用户确认后创建不可覆盖的正典快照 |
| `extract_reader_template.py` | 从适用参考提取样式，清理模板内容和元数据 |
| `build_reader_docx.py` | 将读者 Markdown 编排为 DOCX，按渲染 PDF 同步目录页码 |
| `verify_reader_docx.py` | 核对文本、目录、跳转、模板格式与可测文字边界 |
| `render_pdf_pages.py` | 将已导出的 PDF 渲染为逐页 PNG，供人工检查 |

具体参数见各脚本的 `--help` 和 [DOCX 交付规范](skills/story-world-architect/references/docx-delivery.md)。

### 不依赖 Codex 专属工具的 DOCX 路线

构建器支持 UTF-8 Markdown 普通段落、三级标题、简单列表、行内强调和比较表。图片、嵌套列表、代码块及复杂版式不在支持范围内，会明确拒绝，而不是静默丢弃。

以下示例在仓库根目录运行；`worldbook.md` 的第一行是 `# 书名`，正文标题统一使用 `# / ## / ###` 或 `## / ### / ####`。

```bash
python skills/story-world-architect/scripts/build_reader_docx.py --source worldbook.md --out worldbook.docx

# 需另行安装 LibreOffice，并使 soffice 命令可用。
mkdir -p qa/round1 qa/round2
soffice --headless --convert-to pdf --outdir qa/round1 worldbook.docx

python skills/story-world-architect/scripts/build_reader_docx.py --source worldbook.md --out worldbook.docx --pages-from-pdf qa/round1/worldbook.pdf
soffice --headless --convert-to pdf --outdir qa/round2 worldbook.docx

python skills/story-world-architect/scripts/verify_reader_docx.py --source worldbook.md --docx worldbook.docx --pdf qa/round2/worldbook.pdf --report qa/check.json
python skills/story-world-architect/scripts/render_pdf_pages.py --pdf qa/round2/worldbook.pdf --out qa/round2-pages
```

首次构建的页码是占位值，不能交付。若回填后实际页码变化，继续用最新 PDF 回填并渲染到新目录，直到验证通过；最后逐页检查 PNG。Word 等其他导出器必须保留标题书签，验证器才可按 PDF 大纲核对页码。

LibreOffice 有时会受正在运行的实例或旧输出影响；使用新的 QA 目录，必要时按其官方说明设置独立用户配置。转换方式见 [LibreOffice 官方命令行文档](https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html)。本仓库不分发 LibreOffice、Codex 的 documents 技能或其专属渲染器。

## 默认排版

正文微软雅黑 12 磅，三级标题 18/16/14 磅，目录项 12/11/10.5 磅，含页眉和页码。用户的新模板优先，不将默认纸张、配色或篇幅当作不可改规则。

模板仅引用字体名称，不包含字体文件。没有对应字体时会发生替换，不能保证与参考相同的分页；请使用合法具备的字体，或提供自己的参考模板并重新渲染验收。

## 隐私与数据

仓库只包含通用工作流程、脚本和空白模板。辅助脚本在本地处理文件，不主动上传原稿；使用 Codex 或其他模型服务时，数据处理遵循相应产品和你的设置。

提取证据和 QA 报告可能记录本地绝对路径，不应直接公开。发布时排除缓存、原稿、备份和测试输出；清理元数据并不等于完成正文中的个人信息脱敏。

## 测试与贡献

```bash
python -B -m unittest discover -s tests -v
```

测试覆盖辅助工具的可观察行为，不代表一整本设定集的文学质量或所有排版场景。欢迎提交问题和改进；请使用最小复现文本，不要提交私人原稿、密钥或未获授权的第三方内容。

## 许可证

本仓库的指令、原创脚本和通用模板使用 [MIT License](LICENSE)，Copyright © 2026 LilHaopeng。创作流程经过 AI 辅助整理；本仓库不是 OpenAI 官方产品。

MIT 不替代依赖软件或字体的许可。尤其 [PyMuPDF／MuPDF 使用 AGPL 或商业许可](https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright)，使用、分发或服务化相关功能时须核对并遵守适用条款；本仓库不分发其二进制代码，也不将其改标为 MIT。python-docx、lxml、LibreOffice 和字体同样保留各自许可。

许可覆盖发布的 skill 内容，不把使用者的原稿、原创世界观或小说自动纳入本仓库许可，也不要求使用者公开自己的创作。
