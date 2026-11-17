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


CVContent = Content


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(text):
    # PDF uppercases section headings and adds bullet glyphs. Neither changes content.
    return re.sub(r"[\s•\u00ad]", "", text).casefold()


def content_tokens(text):
    # Compare content independently of columns, page breaks and extraction order.
    return Counter(re.findall(r"\w+|[^\w\s•\u00ad]", text.casefold()))


def validate_pdf(path, content):
    import pymupdf

    with pymupdf.open(path) as document:
        require(not document.needs_pass and len(document) > 0, "PDF is locked or has no pages")
        # CSS page counters are generated presentation, not CV source content.
        extracted = "\n".join(
            block[4] for index, page in enumerate(document)
            for block in page.get_text("blocks") if block[6] == 0
            and not (block[4].strip() == f"{index + 1} / {len(document)}"
                     and block[1] > page.rect.height * 0.9))
        require(extracted.strip(), "PDF has no extractable text")
        reference = " ".join(content.text)
        require(content_tokens(reference) == content_tokens(extracted),
                "PDF content differs from HTML: missing, duplicated or changed text")
        warnings = []
        if normalized(reference) != normalized(extracted):
            warnings.append("Text extraction order differs from HTML; review reading order visually")
        page_details = []
        links = []
        for index, page in enumerate(document):
            spans = [span for block in page.get_text("dict")["blocks"] if "lines" in block
                     for line in block["lines"] for span in line["spans"] if span["text"].strip()]
            if not spans:
                warnings.append(f"Page {index + 1} has no extractable text")
            links.extend(link["uri"] for link in page.get_links() if link.get("uri"))
            page_details.append({"page": index + 1,
                                 "minimum_font_pt": round(min(s["size"] for s in spans), 2) if spans else None,
                                 "width_pt": round(page.rect.width, 2),
                                 "height_pt": round(page.rect.height, 2),
                                 "words": len(page.get_text().split())})
        if Counter(links) != Counter(content.links):
            warnings.append("PDF links differ from HTML; review clickable links")
        return {"pages": page_details, "links": len(links), "warnings": warnings,
                "checks": ["readable PDF with text", "complete text independent of extraction order"]}


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
            require(page.evaluate('''() => [...document.fonts].every(font => font.status === 'loaded')'''), "Embedded fonts did not load")
            page.evaluate("window.paginateCV()")
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
    for preview in review.glob("page-*.png"):
        if re.fullmatch(r"page-\d+\.png", preview.name):
            preview.unlink()
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
    print(f"PASS: {len(report['pages'])} pages, complete text, {report['links']} PDF links")
    for warning in report["warnings"]:
        print(f"WARNING: {warning}")
    print(f"PDF: {output}; QA and page previews: {review}")


if __name__ == "__main__":
    try:
        main()
    except ImportError as error:
        raise SystemExit("Missing PDF dependencies. Run make cv-setup.") from error
    except (ValueError, FileNotFoundError) as error:
        raise SystemExit(f"CV PDF: {error}") from error
