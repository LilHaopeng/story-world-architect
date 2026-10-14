#!/usr/bin/env python3
"""Render an already exported PDF into PNGs; this does not convert DOCX files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz


def render(pdf: Path, out: Path, dpi: int = 150) -> int:
    if not pdf.is_file():
        raise ValueError("The input PDF does not exist.")
    if not 72 <= dpi <= 600:
        raise ValueError("DPI must be between 72 and 600.")
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError("Use a new or empty output directory; old page images must not be reused.")
    with fitz.open(pdf) as document:
        if document.needs_pass:
            raise ValueError("Encrypted PDFs must be unlocked before rendering.")
        if not len(document):
            raise ValueError("The input PDF has no pages.")
        out.mkdir(parents=True, exist_ok=True)
        for number, page in enumerate(document, 1):
            page.get_pixmap(dpi=dpi, alpha=False).save(out / f"page-{number}.png")
        return len(document)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--dpi", default=150, type=int)
    args = parser.parse_args()
    try:
        count = render(args.pdf, args.out, args.dpi)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")
    print(json.dumps({"pages": count, "dpi": args.dpi, "requires_visual_review": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
