"""Exercise the PDF quality gate with valid and deliberately damaged documents."""
from pathlib import Path
import tempfile
import unittest

import pymupdf

from pdf import CVContent, validate_pdf

FONT = Path(__file__).parent / 'fonts/UbuntuSans-Regular.ttf'
HTML = '''<h1>Candidate</h1><p><a href="mailto:candidate@example.com">candidate@example.com</a></p>
<h2>Professional Experience</h2><h3>Example Company</h3>
<div class="role-metadata"><p><strong>Engineer | 2024-Present</strong></p></div>
<p>Delivered systems.</p><h2>Languages</h2><p>English</p>'''
LINES = ['Candidate', 'candidate@example.com', 'Professional Experience', 'Example Company',
         'Engineer | 2024-Present', 'Delivered systems.', 'Languages', 'English']


class PDFTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'test.pdf'

    def create(self, lines=LINES, size=10.5, href='mailto:candidate@example.com', split=False):
        with pymupdf.open() as document:
            page = document.new_page(width=595.28, height=841.89)
            page.insert_font(fontname='CVRegular', fontfile=str(FONT))
            y = 50
            for index, line in enumerate(lines):
                if split and index == 4:
                    page = document.new_page(width=595.28, height=841.89)
                    page.insert_font(fontname='CVRegular', fontfile=str(FONT))
                    y = 50
                page.insert_text((40, y), line, fontsize=size, fontname='CVRegular')
                if line == 'candidate@example.com':
                    page.insert_link({'kind': pymupdf.LINK_URI, 'uri': href,
                                      'from': pymupdf.Rect(40, y-12, 180, y+2)})
                y += 16
            document.save(self.path)

    def test_valid_pdf(self):
        self.create()
        report = validate_pdf(self.path, CVContent(HTML))
        self.assertEqual(report['links'], 1)
        self.assertEqual(report['warnings'], [])

    def test_missing_languages_rejected(self):
        self.create(lines=LINES[:-2])
        with self.assertRaisesRegex(ValueError, 'content differs'):
            validate_pdf(self.path, CVContent(HTML))

    def test_changed_link_warns_without_blocking(self):
        self.create(href='mailto:wrong@example.com')
        report = validate_pdf(self.path, CVContent(HTML))
        self.assertTrue(any('links' in warning for warning in report['warnings']))

    def test_font_size_is_reported_without_blocking(self):
        self.create(size=9)
        report = validate_pdf(self.path, CVContent(HTML))
        self.assertEqual(report['pages'][0]['minimum_font_pt'], 9)

    def test_page_break_and_split_heading_do_not_block(self):
        self.create(split=True)
        report = validate_pdf(self.path, CVContent(HTML))
        self.assertEqual(len(report['pages']), 2)

    def test_reordered_text_warns_without_blocking(self):
        self.create(lines=list(reversed(LINES)))
        report = validate_pdf(self.path, CVContent(HTML))
        self.assertTrue(any('order' in warning for warning in report['warnings']))

    def test_duplicated_text_rejected(self):
        self.create(lines=LINES + ['Delivered systems.'])
        with self.assertRaisesRegex(ValueError, 'content differs'):
            validate_pdf(self.path, CVContent(HTML))

    def test_changed_text_rejected(self):
        self.create(lines=[line.replace('Delivered systems.', 'Delivered software.') for line in LINES])
        with self.assertRaisesRegex(ValueError, 'content differs'):
            validate_pdf(self.path, CVContent(HTML))

    def test_corrupt_pdf_rejected(self):
        self.path.write_bytes(b'not a PDF')
        with self.assertRaises(pymupdf.FileDataError):
            validate_pdf(self.path, CVContent(HTML))

    def test_empty_pdf_rejected(self):
        with pymupdf.open() as document:
            document.new_page()
            document.save(self.path)
        with self.assertRaisesRegex(ValueError, 'no extractable text'):
            validate_pdf(self.path, CVContent(HTML))

    def test_arbitrary_page_count_and_geometry_do_not_block(self):
        self.create()
        with pymupdf.open(self.path) as document:
            for _ in range(4):
                document.new_page(width=400, height=300)
            document.saveIncr()
        report = validate_pdf(self.path, CVContent(HTML))
        self.assertEqual(len(report['pages']), 5)
        self.assertEqual(report['pages'][-1]['width_pt'], 400)
        self.assertTrue(any('no extractable text' in warning for warning in report['warnings']))
