![Story World Architect](assets/world-architect-hero.png)

# Story World Architect · 小说世界观架构师

[简体中文](README.md) | **English**

A comprehensive worldbuilding Agent Skill for fiction and original IP: builds causally grounded worlds across geography, production, institutions, social classes, and everyday life, then compiles rigorous internal canon into an engaging, book-styled reader compendium (DOCX). Current version: **v1.4.0**.

By default, the skill reasons and writes in **Simplified Chinese (`简体中文`)**. You can explicitly ask to start or write in **English**, **Traditional Chinese**, or any other language—the skill adapts its prose register, cultural framing, and table-of-contents headings (`--toc-title Contents`) accordingly.

## Core Capabilities

- **Full-Lifecycle Worldbuilding**: Create worlds from scratch, expand existing lore, audit rule loopholes, lock canon snapshots, and evolve world states from verified story events.
- **Causal & Everyday Deduction**: Traces `Constraint → Allocation → Incentive → Institution / Habit → Everyday Consequence → Ongoing Pressure → Potential Shift` down to household routines, regional contrasts, and institutional friction.
- **Four Design Anchors & Upfront Blueprint**: Aligns cultural/historical reference points, baseline time (`T0`), grit & relief scale, currency/purchasing-power index, and up to four TOC levels before drafting full chapters.
- **Internal Canon vs. Reader Compendium**: Maintains structured IDs (`RULE`, `INST`, `FAC`, `CON`, `SEED`, `LOOP`, `REG`, `CHAR`) on the author workbench while presenting smooth, human-centered prose and concrete everyday vignettes to readers.
- **Downstream Vernacular & Sensory Handoff**: Exports forms of address, street idioms, trade jargon, everyday utensils/foods, and anachronism taboos via `15_大纲接口.md` so downstream outlines and chapter prose sound lived-in from page one.
- **Book-Grade DOCX Compilation & Layout QA**: Ships with a clean A4 editorial template (serif body, sans-serif hierarchy, restrained ink-navy / indigo / charcoal / ochre-bronze palette), syncs real PDF bookmark page numbers, verifies glyph bounds, and renders page-by-page PNGs for visual inspection.

## Companion Studio Pipeline

Each skill works standalone or as part of a connected three-stage novel pipeline:

1. **Story World Architect**: Establishes world rules, social ecosystems, reader worldbooks, and downstream handoff contracts.
2. [Story Outline Architect](https://github.com/LilHaopeng/story-outline-architect): Consumes world rules and conflict seeds to architect Story DNA, multi-track arcs, sequences, and chapter outlines.
3. [Story Prose Writer](https://github.com/LilHaopeng/story-prose-writer): Draws on world vernacular slices and chapter outlines to calibrate voice, write natural chapters, and maintain continuity.

## Installation

1. **Via `skill-installer` (Codex, etc.)**
   ```text
   $skill-installer Install skills/story-world-architect from https://github.com/LilHaopeng/story-world-architect
   ```
2. **Manual Local Installation (Antigravity / Claude Code / Codex / Cursor)**
   Clone this repository and copy `skills/story-world-architect/` into your host's skills directory:
   - **Antigravity**: `~/.gemini/config/skills/story-world-architect`
   - **Claude Code**: `~/.claude/skills/story-world-architect`
   - **Codex**: `~/.codex/skills/story-world-architect` or `~/.agents/skills/story-world-architect`
   - **Cursor**: `~/.cursor/skills/story-world-architect`

## Quick Start

**Writing in English (explicitly selected)**:

```text
$story-world-architect
Design a seasonal archipelago world in English where island guilds migrate ahead of monsoon currents.
Align the core rules, four design anchors, and a 4-level chapter plan with me first, then deliver a reader-facing World Compendium DOCX.
```

**Default Simplified Chinese**:

```text
$story-world-architect
我想设计一个依赖季节迁徙维持生产的群岛世界。先核对核心规则、创作锚点与四级目录，确认后生成读者向世界设定集 DOCX。
```

## Helper Scripts & Dependencies

Install Python dependencies (Python 3.10+) when using automated validation, DOCX compilation, and PDF layout verification (PDF export requires LibreOffice or a bookmark-preserving converter):

```bash
python -m pip install -r requirements.txt
```

| Script | Purpose |
|---|---|
| `init_world_project.py` | Non-destructively initializes world canon files and design anchors (`--lang`, `--mode`, `--audience`) |
| `validate_world.py` | Validates required fields, anchor sections, object IDs, and cross-file references |
| `lock_world.py` | Creates immutable versioned canon snapshots upon user confirmation |
| `extract_reader_template.py` | Distills custom user reference DOCX files into clean reusable templates |
| `build_reader_docx.py` | Compiles Markdown into a 4-level bookmarked DOCX (`--pages-from-pdf`, `--subtitle`, `--toc-title Contents`) |
| `verify_reader_docx.py` | Verifies text coverage, TOC jumps/page numbers, template font slots, page bounds, and sparse chapter tails |
| `render_pdf_pages.py` | Renders exported PDFs into per-page PNGs (supports `PyMuPDF` or `pypdfium2 + Pillow` / `pdf2image`) |

### Local English / Chinese DOCX Build & Page-Sync Workflow

```bash
python skills/story-world-architect/scripts/build_reader_docx.py --source worldbook.md --out worldbook.docx --subtitle "World Compendium" --toc-title Contents
mkdir -p qa/round1 qa/round2
soffice --headless --convert-to pdf --outdir qa/round1 worldbook.docx

python skills/story-world-architect/scripts/build_reader_docx.py --source worldbook.md --out worldbook.docx --subtitle "World Compendium" --toc-title Contents --pages-from-pdf qa/round1/worldbook.pdf
soffice --headless --convert-to pdf --outdir qa/round2 worldbook.docx

python skills/story-world-architect/scripts/verify_reader_docx.py --source worldbook.md --docx worldbook.docx --pdf qa/round2/worldbook.pdf --toc-title Contents --report qa/check.json
python skills/story-world-architect/scripts/render_pdf_pages.py --pdf qa/round2/worldbook.pdf --out qa/round2-pages
```

Run unit tests:

```bash
python -B -m unittest discover -s tests -v
```

## Privacy & License

All scripts operate strictly on local files and never upload manuscripts. Released under the [MIT License](LICENSE) (Copyright © 2026 LilHaopeng); third-party packages retain their respective upstream licenses.
