"""Regressions for a single Markdown source, including unseen company names."""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest

from check import Content, compare, expected

ROOT = Path(__file__).resolve().parent.parent
PANDOC = shutil.which(os.environ.get("PANDOC", "pandoc"))
SOURCE = """# Candidate

**Architect**

[candidate@example.com](mailto:candidate@example.com)

## Professional Experience

## A Completely New Company

**Architect | 2024 – Present**\x20\x20
Industry\x20\x20
[company.example](https://company.example/)

Delivered systems.

### Key Responsibilities & Achievements

- Built a reliable service.

### Technologies

Python · SQL
---

## Languages

Polish · English

## Certifications

**A newly added certificate**
"""


class GeneratorTests(unittest.TestCase):
    def render(self, source):
        # No experience.md exists here: accessing a second source must fail the test.
        with tempfile.TemporaryDirectory() as directory:
            return subprocess.check_output(
                [PANDOC, "--from=markdown-smart", "--to=html5", "--section-divs",
                 f"--lua-filter={ROOT / 'cv/layout.lua'}"],
                input=source, text=True, cwd=directory,
            )

    def test_new_company_contact_and_trailing_sections_without_second_source(self):
        html = self.render(SOURCE)
        compare(Content(html), expected(SOURCE, PANDOC))
        self.assertIn('<h3>A Completely New Company</h3>', html)
        self.assertIn('class="role-metadata"', html)
        self.assertIn('class="technologies"', html)
        self.assertIn('<h2>Languages</h2>', html)
        self.assertIn('<h2>Certifications</h2>', html)
        self.assertNotIn('Key Responsibilities &amp; Achievements', html)

    def test_current_cv_without_second_source(self):
        source = (ROOT / "cv/cv.md").read_text()
        compare(Content(self.render(source)), expected(source, PANDOC))

    def test_content_check_rejects_missing_contact(self):
        reference = expected(SOURCE, PANDOC)
        html = self.render(SOURCE).replace('candidate@example.com</a>', 'omitted</a>')
        with self.assertRaisesRegex(AssertionError, "content"):
            compare(Content(html), reference)

    def test_content_check_rejects_changed_href(self):
        html = self.render(SOURCE).replace('mailto:candidate@example.com', 'mailto:wrong@example.com')
        with self.assertRaisesRegex(AssertionError, "href"):
            compare(Content(html), expected(SOURCE, PANDOC))
