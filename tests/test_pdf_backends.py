"""Exercise real fallback libraries even when optional PyMuPDF is installed."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/story-world-architect/scripts'
sys.path.insert(0, str(SCRIPTS))
import build_reader_docx as builder
import verify_reader_docx as verifier
import render_pdf_pages as renderer


class PdfBackendsTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='world-pdf-backends-')
        self.folder = Path(self.temporary.name)
        self.source = self.folder / 'source.md'
        self.source.write_text('# Book\n\n# First\n\n## Second\n\n### Third\n\n#### Fourth\n\nBody text.\n', encoding='utf-8')
        self.headings = builder.parse_markdown(self.source).headings

    def tearDown(self):
        self.temporary.cleanup()

    def fixture(self, *, off_page=False, encrypted=False, titles=None):
        writer = PdfWriter()
        font = DictionaryObject({NameObject('/Type'): NameObject('/Font'),
                                 NameObject('/Subtype'): NameObject('/Type1'),
                                 NameObject('/BaseFont'): NameObject('/Helvetica')})
        other = DictionaryObject({NameObject('/Type'): NameObject('/Font'),
                                  NameObject('/Subtype'): NameObject('/Type1'),
                                  NameObject('/BaseFont'): NameObject('/Courier')})
        for index in range(2):
            page = writer.add_blank_page(width=595, height=842)
            page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'): DictionaryObject({
                NameObject('/F1'): writer._add_object(font), NameObject('/F2'): writer._add_object(other)})})
            content = b'BT /F1 12 Tf 60 742 Td (First) Tj 0 -24 Td (Second) Tj 0 -24 Td (Third) Tj 0 -24 Td (Fourth) Tj 0 -24 Td (Body ) Tj /F2 12 Tf (text.) Tj ET\n'
            if off_page:
                content += b'BT /F1 12 Tf -8 600 Td (OUTSIDE) Tj ET\n'
            stream = DecodedStreamObject()
            stream.set_data(content)
            page[NameObject('/Contents')] = writer._add_object(stream)
        parent = None
        for level, title in (titles or self.headings):
            parent = writer.add_outline_item(title, 1, parent=parent if level > 1 else None)
        if encrypted:
            writer.encrypt('secret')
        pdf = self.folder / ('encrypted.pdf' if encrypted else 'fixture.pdf')
        with pdf.open('wb') as handle:
            writer.write(handle)
        return pdf

    def test_pypdf_nested_outline_and_repeated_titles(self):
        headings = [(1, '重复'), (2, '重复'), (3, 'A long heading ' * 10), (4, 'Fourth')]
        pdf = self.fixture(titles=headings)
        with patch.dict(sys.modules, {'fitz': None}):
            self.assertEqual(builder.pdf_heading_pages(pdf, headings), [2, 2, 2, 2])
            with self.assertRaises(ValueError):
                builder.pdf_heading_pages(pdf, [(1, 'Wrong')])

    def test_fallback_build_and_verify_preserve_four_levels(self):
        pdf = self.fixture()
        out = self.folder / 'book.docx'
        with patch.dict(sys.modules, {'fitz': None}), patch.object(verifier, 'fitz', None):
            builder.build(self.source, out, pages_from_pdf=pdf)
            report = verifier.verify(self.source, out, pdf)
        self.assertTrue(report['ok'], report['errors'])
        self.assertEqual(report['evidence']['pdf_layout_backend'], 'pdfplumber')
        self.assertEqual(report['evidence']['headings'], 4)
        self.assertIn('Helvetica', report['evidence']['pdf_fonts_by_text_characters'])
        self.assertIn('Courier', report['evidence']['pdf_fonts_by_text_characters'])

    def test_pdfplumber_detects_real_off_page_text(self):
        pdf = self.fixture(off_page=True)
        out = self.folder / 'book.docx'
        with patch.dict(sys.modules, {'fitz': None}), patch.object(verifier, 'fitz', None):
            builder.build(self.source, out, pages_from_pdf=pdf)
            report = verifier.verify(self.source, out, pdf)
        self.assertFalse(report['ok'])
        self.assertFalse(report['checks']['measurable_page_boundaries'])
        self.assertTrue(any(item['bbox'][0] < 0 for item in report['evidence']['page_boundary_anomalies']))

    def test_layout_missing_backend_fails_without_synthetic_coordinates(self):
        pdf = self.fixture()
        with patch.object(verifier, 'fitz', None), patch.dict(sys.modules, {'pdfplumber': None}):
            with self.assertRaisesRegex(RuntimeError, 'cannot measure text bounds'):
                with verifier._open_pdf(pdf):
                    pass

    def test_pypdf_missing_backend_and_encryption_fail_explicitly(self):
        pdf = self.fixture()
        with patch.dict(sys.modules, {'fitz': None, 'pypdf': None}):
            with self.assertRaisesRegex(RuntimeError, 'nor pypdf'):
                builder.pdf_heading_pages(pdf, self.headings)
        encrypted = self.fixture(encrypted=True)
        with patch.dict(sys.modules, {'fitz': None}):
            with self.assertRaisesRegex(ValueError, 'Encrypted'):
                builder.pdf_heading_pages(encrypted, self.headings)

    def test_pdfium_real_raster_and_stale_directory(self):
        pdf = self.fixture()
        out = self.folder / 'pages'
        with patch.object(renderer, 'fitz', None):
            self.assertEqual(renderer.render(pdf, out, 72), 2)
            with self.assertRaisesRegex(ValueError, 'new or empty'):
                renderer.render(pdf, out, 72)
        for number in (1, 2):
            with Image.open(out / f'page-{number}.png') as image:
                self.assertEqual(image.size, (595, 842))
                self.assertIsNotNone(image.convert('RGB').point(lambda value: 255-value).getbbox())

    def test_renderer_no_backend_dpi_and_encryption(self):
        pdf = self.fixture()
        with patch.object(renderer, 'fitz', None), patch.dict(sys.modules, {'pypdfium2': None, 'pdf2image': None}):
            with self.assertRaisesRegex(RuntimeError, 'nor pdf2image'):
                renderer.render(pdf, self.folder / 'none', 72)
        with self.assertRaisesRegex(ValueError, 'DPI'):
            renderer.render(pdf, self.folder / 'dpi', 1)
        encrypted = self.fixture(encrypted=True)
        with patch.object(renderer, 'fitz', None):
            with self.assertRaisesRegex(ValueError, 'Encrypted'):
                renderer.render(encrypted, self.folder / 'encrypted', 72)

    def test_pdf2image_route_and_poppler_missing_message(self):
        try:
            import pdf2image
        except ImportError:
            self.skipTest('Optional pdf2image route is not installed.')
        from pdf2image.exceptions import PDFInfoNotInstalledError
        pdf = self.fixture()
        # Route and resource handling only; this is not a real Poppler render.
        with patch.object(renderer, 'fitz', None), patch.dict(sys.modules, {'pypdfium2': None}):
            with patch.object(pdf2image, 'convert_from_path', return_value=[Image.new('RGB', (10, 20), 'white')]):
                self.assertEqual(renderer.render(pdf, self.folder / 'poppler-route', 72), 1)
            with patch.object(pdf2image, 'convert_from_path', side_effect=PDFInfoNotInstalledError()):
                with self.assertRaisesRegex(RuntimeError, 'Poppler tools'):
                    renderer.render(pdf, self.folder / 'poppler-missing', 72)

    def test_clis_load_without_fitz(self):
        for name in ('build_reader_docx.py', 'verify_reader_docx.py', 'render_pdf_pages.py'):
            code = "import runpy,sys; sys.modules['fitz']=None; sys.path.insert(0,sys.argv[1]); sys.argv=[sys.argv[2],'--help']; runpy.run_path(sys.argv[0],run_name='__main__')"
            result = subprocess.run([sys.executable, '-B', '-X', 'utf8', '-c', code, str(SCRIPTS), str(SCRIPTS / name)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('usage:', result.stdout)


if __name__ == '__main__':
    unittest.main()
