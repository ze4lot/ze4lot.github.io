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
        report = validate_pdf(self.path, CVContent(HTML), expected_pages=1)
        self.assertEqual(report['links'], 1)
        self.assertEqual(report['company_role_pairs'], 1)

    def test_missing_languages_rejected(self):
        self.create(lines=LINES[:-2])
        with self.assertRaisesRegex(ValueError, 'text differs'):
            validate_pdf(self.path, CVContent(HTML), expected_pages=1)

    def test_changed_link_rejected(self):
        self.create(href='mailto:wrong@example.com')
        with self.assertRaisesRegex(ValueError, 'hrefs'):
            validate_pdf(self.path, CVContent(HTML), expected_pages=1)

    def test_small_text_rejected(self):
        self.create(size=9)
        with self.assertRaisesRegex(ValueError, 'below 10.5'):
            validate_pdf(self.path, CVContent(HTML), expected_pages=1)

    def test_wrong_page_count_rejected(self):
        self.create()
        with self.assertRaisesRegex(ValueError, 'Expected 4'):
            validate_pdf(self.path, CVContent(HTML))

    def test_orphaned_company_rejected(self):
        self.create(split=True)
        with self.assertRaisesRegex(ValueError, 'Orphaned'):
            validate_pdf(self.path, CVContent(HTML), expected_pages=2)
