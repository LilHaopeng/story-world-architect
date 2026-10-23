#!/usr/bin/env python3
"""Render an already exported PDF into PNGs; this does not convert DOCX files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import fitz
except ImportError:
    fitz = None  # type: ignore[assignment]


def _render_with_fitz(pdf: Path, out: Path, dpi: int) -> int:
    with fitz.open(pdf) as document:
        if document.needs_pass:
            raise ValueError("Encrypted PDFs must be unlocked before rendering.")
        if not len(document):
            raise ValueError("The input PDF has no pages.")
        out.mkdir(parents=True, exist_ok=True)
        for number, page in enumerate(document, 1):
            page.get_pixmap(dpi=dpi, alpha=False).save(out / f"page-{number}.png")
        return len(document)


def _render_with_fallback(pdf: Path, out: Path, dpi: int) -> int:
    try:
        import pypdf
    except ImportError:
        pypdf = None
    if pypdf is not None:
        with pdf.open("rb") as handle:
            reader = pypdf.PdfReader(handle)
            if reader.is_encrypted:
                raise ValueError("Encrypted PDFs must be unlocked before rendering.")
            if not len(reader.pages):
                raise ValueError("The input PDF has no pages.")
    try:
        import pypdfium2
    except ImportError:
        pypdfium2 = None
    if pypdfium2 is not None:
        document = pypdfium2.PdfDocument(str(pdf))
        try:
            count = len(document)
            if not count:
                raise ValueError("The input PDF has no pages.")
            out.mkdir(parents=True, exist_ok=True)
            scale = dpi / 72.0
            for number, page in enumerate(document, 1):
                try:
                    bitmap = page.render(scale=scale)
                    try:
                        image = bitmap.to_pil()
                        try:
                            image.save(out / f"page-{number}.png")
                        finally:
                            image.close()
                    finally:
                        bitmap.close()
                finally:
                    page.close()
            return count
        finally:
            document.close()
    try:
        from pdf2image import convert_from_path
        from pdf2image.exceptions import PDFInfoNotInstalledError
    except ImportError as exc:
        raise RuntimeError("Neither PyMuPDF (fitz), pypdfium2, nor pdf2image is installed.") from exc
    try:
        images = convert_from_path(str(pdf), dpi=dpi)
    except PDFInfoNotInstalledError as exc:
        raise RuntimeError("pdf2image requires Poppler tools (pdfinfo and pdftoppm/pdftocairo) on PATH.") from exc
    try:
        if not images:
            raise ValueError("The input PDF has no pages.")
        out.mkdir(parents=True, exist_ok=True)
        for number, image in enumerate(images, 1):
            image.save(out / f"page-{number}.png")
        return len(images)
    finally:
        for image in images:
            image.close()


def render(pdf: Path, out: Path, dpi: int = 150) -> int:
    if not pdf.is_file():
        raise ValueError("The input PDF does not exist.")
    if not 72 <= dpi <= 600:
        raise ValueError("DPI must be between 72 and 600.")
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError("Use a new or empty output directory; old page images must not be reused.")
    if fitz is not None:
        return _render_with_fitz(pdf, out, dpi)
    return _render_with_fallback(pdf, out, dpi)


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
