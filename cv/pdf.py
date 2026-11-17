"""Render and validate a recruitment PDF. Run via make cv-pdf / cv-pdf-check."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import re
import tempfile

from check import Content


class CVContent(Content):
    """Read text, links and company/role pairs from the generated semantic HTML."""
    def __init__(self, html):
        self.pairs = []
        self.heading = False
        self.role = False
        self.strong = False
        super().__init__(html)

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        attrs = dict(attrs)
        if tag == "h3":
            self.heading = True
            self.pairs.append({"company": "", "role": ""})
        if tag == "div" and "role-metadata" in attrs.get("class", "").split():
            self.role = True
        if tag == "strong" and self.role:
            self.strong = True

    def handle_endtag(self, tag):
        if tag == "h3":
            self.heading = False
        if tag == "strong":
            self.strong = False
        if tag == "div":
            self.role = False

    def handle_data(self, data):
        super().handle_data(data)
        if self.heading:
            self.pairs[-1]["company"] += data
        if self.role and self.strong:
            self.pairs[-1]["role"] += data


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(text):
    # PDF uppercases section headings and adds bullet glyphs. Neither changes content.
    return re.sub(r"[\s•\u00ad]", "", text).casefold()


def validate_pdf(path, content, expected_pages=4):
    import pymupdf

    with pymupdf.open(path) as document:
        require(len(document) == expected_pages,
                f"Expected {expected_pages} A4 pages, got {len(document)}")
        require(normalized("".join(content.text)) == normalized("".join(p.get_text() for p in document)),
                "PDF text differs from HTML: missing, duplicated, reordered or extra content")
        page_details = []
        links = []
        for index, page in enumerate(document):
            require(abs(page.rect.width - 595.28) < 1 and abs(page.rect.height - 841.89) < 1,
                    f"Page {index + 1} is not A4 portrait")
            spans = [span for block in page.get_text("dict")["blocks"] if "lines" in block
                     for line in block["lines"] for span in line["spans"] if span["text"].strip()]
            require(spans, f"Page {index + 1} is empty or has no extractable text")
            minimum = min(span["size"] for span in spans)
            require(minimum >= 10.49, f"Page {index + 1}: text below 10.5 pt ({minimum:.2f})")
            require(all(-0.5 <= s["bbox"][0] < s["bbox"][2] <= page.rect.width + 0.5
                        and -0.5 <= s["bbox"][1] < s["bbox"][3] <= page.rect.height + 0.5 for s in spans),
                    f"Page {index + 1}: text extends beyond page bounds")
            fonts = page.get_fonts()
            require(all(f[2] != "Type3" and document.extract_font(f[0])[3] for f in fonts),
                    f"Page {index + 1}: missing embedded font or Type 3 font")
            page_links = page.get_links()
            require(all(link.get("uri") for link in page_links), "Unexpected local or unresolved PDF link")
            links.extend(link["uri"] for link in page_links)
            page_details.append({"page": index + 1, "minimum_font_pt": round(minimum, 2),
                                 "words": len(page.get_text().split())})

        require(Counter(links) == Counter(content.links), "PDF hrefs differ from HTML")
        for pair in content.pairs:
            require(pair["role"], f"Missing role metadata for {pair['company']}")
            together = False
            for page in document:
                companies = page.search_for(pair["company"])
                roles = page.search_for(pair["role"])
                if companies and roles:
                    together |= any(0 <= roles[0].y0 - company.y1 < 40 for company in companies)
            require(together, f"Orphaned company heading or split role metadata: {pair['company']}")

        return {"pages": page_details, "links": len(links), "company_role_pairs": len(content.pairs),
                "checks": ["complete text in reading order", "A4 portrait", "10.5 pt minimum",
                           "no text outside pages", "embedded fonts without Type 3",
                           "exact hrefs", "company and role stay together"]}


def render_pdf(html, target):
    from playwright.sync_api import sync_playwright, Error as BrowserError

    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch()
        except BrowserError as error:
            raise ValueError(f"Chromium could not start. Run make cv-setup. {error}") from error
        try:
            context = browser.new_context(offline=True, viewport={"width": 1200, "height": 1100})
            page = context.new_page()
            failures = []
            page.on("requestfailed", lambda request: failures.append(request.url))
            page.emulate_media(media="print")
            page.goto(html.resolve().as_uri(), wait_until="load")
            page.evaluate("document.fonts.ready")
            require(not failures, f"Failed document resources: {failures}")
            require(page.evaluate('''() => [...document.fonts].length >= 2 &&
                [...document.fonts].every(font => font.status === 'loaded')'''), "Embedded fonts did not load")
            page.pdf(path=str(target), prefer_css_page_size=True, scale=1,
                     display_header_footer=False, print_background=False, tagged=True, outline=True)
            return {"playwright": version("playwright"), "chromium": browser.version}
        finally:
            browser.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true", help="Validate the saved PDF without overwriting it")
    args = parser.parse_args()
    html, output, review = Path("cv/generated.html"), Path("cv/generated.pdf"), Path("cv/review")
    main_html = re.search(r'<main class="cv">(.*?)</main>', html.read_text(), flags=re.S)
    require(main_html, "Missing CV main element")
    content = CVContent(main_html[1])
    if args.check_only:
        require(output.is_file(), "PDF does not exist. Run make cv-pdf first.")
        report = validate_pdf(output, content)
    else:
        # Promote only a validated candidate. A failed export preserves the previous PDF.
        with tempfile.TemporaryDirectory(prefix="cv-pdf-", dir=output.parent) as temporary:
            candidate = Path(temporary) / "candidate.pdf"
            renderer = render_pdf(html, candidate)
            report = validate_pdf(candidate, content)
            candidate.replace(output)
        report["renderer"] = renderer

    import pymupdf
    review.mkdir(exist_ok=True)
    with pymupdf.open(output) as document:
        for index, page in enumerate(document):
            page.get_pixmap(matrix=pymupdf.Matrix(1.3, 1.3)).save(review / f"page-{index + 1}.png")
    report.update({"validated_at_utc": datetime.now(timezone.utc).isoformat(),
                   "source_sha256": fingerprint(Path("cv/cv.md")), "html_sha256": fingerprint(html),
                   "pdf_sha256": fingerprint(output), "pymupdf": version("PyMuPDF")})
    if args.check_only:
        previous = review / "pdf-qa.json"
        if previous.exists():
            recorded = json.loads(previous.read_text())
            if recorded.get("pdf_sha256") == report["pdf_sha256"] and "renderer" in recorded:
                report["renderer"] = recorded["renderer"]
    (review / "pdf-qa.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"PASS: {len(report['pages'])} A4 pages, minimum 10.5 pt, full text, {report['links']} links, "
          f"{report['company_role_pairs']} company/role pairs")
    print(f"PDF: {output}; QA and page previews: {review}")


if __name__ == "__main__":
    try:
        main()
    except ImportError as error:
        raise SystemExit("Missing PDF dependencies. Run make cv-setup.") from error
    except (ValueError, FileNotFoundError) as error:
        raise SystemExit(f"CV PDF: {error}") from error
