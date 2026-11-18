"""Render and validate a recruitment PDF. Run via make cv-pdf / cv-pdf-check."""
import argparse
from collections import Counter
from html.parser import HTMLParser
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import re
import subprocess
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


def validate_pdf(path, content, running_header=()):
    import pymupdf

    with pymupdf.open(path) as document:
        require(not document.needs_pass and len(document) > 0, "PDF is locked or has no pages")
        # CSS page counters are generated presentation, not CV source content.
        extracted = "\n".join(
            block[4] for index, page in enumerate(document)
            for block in page.get_text("blocks") if block[6] == 0
            and not (re.fullmatch(rf"0?{index + 1} / 0?{len(document)}", block[4].strip())
                     and block[1] > page.rect.height * 0.9)
            and not (block[1] < page.rect.height * 0.05
                     and block[4].strip()
                     and all(line.strip() in running_header for line in block[4].strip().splitlines())))
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
            # Load every embedded face, including weights unused by the current content.
            page.evaluate("Promise.all([...document.fonts].map(font => font.load()))")
            page.evaluate("document.fonts.ready")
            require(not failures, f"Failed document resources: {failures}")
            require(page.evaluate('''() => [...document.fonts].every(font => font.status === 'loaded')'''), "Embedded fonts did not load")
            page.evaluate("window.paginateCV()")
            page.pdf(path=str(target), prefer_css_page_size=True, scale=1,
                     display_header_footer=False, print_background=False, tagged=True, outline=True)
            return {"playwright": version("playwright"), "chromium": browser.version}
        finally:
            browser.close()


class Headings(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.headings = []
        self.current = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == "h2":
            self.current = []

    def handle_data(self, data):
        if self.current is not None:
            self.current.append(data)

    def handle_endtag(self, tag):
        if tag == "h2" and self.current is not None:
            self.headings.append(" ".join("".join(self.current).split()).upper())
            self.current = None


def finalize_pdf(pdf, html):
    """Add ActualText to the tagged H2 text runs, without changing tracking.

    Chromium tags the separator as H2 and its text as a NonStruct child.
    Resolve those children from the structure tree, never from glyph codes or
    guessed MCID numbers. Fail closed if Chromium changes this representation.
    """
    import pymupdf

    headings = Headings(Path(html).read_text()).headings
    with pymupdf.open(pdf) as document:
        require(all(font[1] == "ttf" and font[2] == "Type0"
                    for page in document for font in page.get_fonts()),
                "Blueprint requires embedded CID TrueType fonts")
        tagged = []
        for xref in range(1, document.xref_length()):
            if document.xref_get_key(xref, "S") != ("name", "/H2"):
                continue
            page_type, page_ref = document.xref_get_key(xref, "Pg")
            require(page_type == "xref", "Heading has no page reference")
            children = re.findall(r"(\d+) 0 R", document.xref_get_key(xref, "K")[1])
            require(len(children) == 1, "Expected one tagged text child per H2")
            kind, mcid = document.xref_get_key(int(children[0]), "K")
            require(kind == "int", "Expected heading text MCID")
            tagged.append((int(page_ref.split()[0]), int(mcid), int(children[0])))
        require(len(tagged) == len(headings), "PDF/HTML heading counts differ")
        pages = {page.xref: page for page in document}
        for (page_xref, mcid, child), text in zip(tagged, headings):
            pattern = rb"/NonStruct(\s*<<\s*/MCID\s+" + str(mcid).encode() + rb"\s*)(>>\s*BDC)"
            actual = ("\ufeff" + text).encode("utf-16-be").hex().encode()
            replacements = 0
            for stream in pages[page_xref].get_contents():
                data, count = re.subn(pattern, lambda m: b"/Span" + m[1] + b" /ActualText <" + actual + b"> " + m[2],
                                      document.xref_stream(stream))
                if count:
                    document.update_stream(stream, data)
                replacements += count
            require(replacements == 1, "Heading text stream was not uniquely identified")
            # Poppler recognizes ActualText on Span; keep the structure tag consistent.
            document.xref_set_key(child, "S", "/Span")
        for index, page in enumerate(document):
            if index == 0:
                continue
            headers = ("MACIEJ PŁOCKI", "SOFTWARE ARCHITECT")
            top = "".join(b[4] for b in page.get_text("blocks") if b[1] < 35)
            require("".join(top.split()) == "".join("".join(headers).split()),
                    "Unexpected running header text")
            streams = page.get_contents()
            require(len(streams) == 1, "Expected one Chromium page content stream")
            stream = streams[0]
            prefix, separator, body = document.xref_stream(stream).partition(b"/NonStruct")
            runs = list(re.finditer(rb"BT\b.*?\bET", prefix, re.S))
            require(len(runs) == 5, "Expected two header and three footer text runs")
            for run, text in reversed(list(zip(runs[:2], headers))):
                actual = ("\ufeff" + text).encode("utf-16-be").hex().encode()
                prefix = (prefix[:run.start()] + b"/Span <</ActualText <" + actual + b"> >> BDC\n"
                          + run[0] + b"\nEMC" + prefix[run.end():])
            document.update_stream(stream, prefix + separator + body)
        document.saveIncr()
    return {"heading_actual_text": len(headings), "font_type": "CID TrueType"}


def check_poppler(pdf, html, folder):
    """Optional acceptance check: requires pdffonts and pdftotext on PATH."""
    import pymupdf

    from check import Content

    fonts = subprocess.check_output(["pdffonts", str(pdf)], text=True)
    (folder / "pdffonts.txt").write_text(fonts)
    require("Type 3" not in fonts and fonts.count("CID TrueType") == 4,
            "Expected four CID TrueType font subsets and no Type 3")
    html = html.read_text()
    headings = Headings(html).headings
    with pymupdf.open(pdf) as document:
        header_pages = len(document) - 1
    for layout in (False, True):
        output = folder / ("pdftotext-layout.txt" if layout else "pdftotext.txt")
        subprocess.run(["pdftotext", *(["-layout"] if layout else []), str(pdf), str(output)], check=True)
        text = output.read_text()
        require(all(text.count(heading) == 1 for heading in headings),
                "Poppler split or changed a section heading")
        require(text.count("MACIEJ PŁOCKI") == header_pages and text.count("SOFTWARE ARCHITECT") == header_pages,
                "Poppler split or changed a running header")
        if layout:
            # Layout mode preserves source hyphens that default Poppler dehyphenates.
            text = text.replace("MACIEJ PŁOCKI", "").replace("SOFTWARE ARCHITECT", "")
            text = re.sub(r"(?m)^\s*\d+\s*/\s*\d+\s*$", "", text)
            content = Content(re.search(r'<main class="cv">(.*?)</main>', html, re.S)[1])
            require(content_tokens(text) == content_tokens(" ".join(content.text)),
                    "Poppler layout extraction changed CV content")
    print("PASS Poppler: four CID TrueType fonts, intact headings in default/layout extraction, complete content")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true", help="Validate the saved PDF without overwriting it")
    parser.add_argument("--poppler-check", action="store_true", help="Also check fonts and text with Poppler (requires pdffonts/pdftotext)")
    args = parser.parse_args()
    html, output, review = Path("cv/generated.html"), Path("static/files/Maciej_Plocki_CV.pdf"), Path("cv/review")
    main_html = re.search(r'<main class="cv">(.*?)</main>', html.read_text(), flags=re.S)
    require(main_html, "Missing CV main element")
    content = CVContent(main_html[1])
    if args.check_only or args.poppler_check:
        require(output.is_file(), "PDF does not exist. Run make cv-pdf first.")
        report = validate_pdf(output, content, running_header=("MACIEJ PŁOCKI", "SOFTWARE ARCHITECT"))
    else:
        # Promote only a validated candidate. A failed export preserves the previous PDF.
        with tempfile.TemporaryDirectory(prefix="cv-pdf-", dir=output.parent) as temporary:
            candidate = Path(temporary) / "candidate.pdf"
            renderer = render_pdf(html, candidate)
            renderer.update(finalize_pdf(candidate, html))
            report = validate_pdf(candidate, content, running_header=("MACIEJ PŁOCKI", "SOFTWARE ARCHITECT"))
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
    if args.poppler_check:
        check_poppler(output, html, review)
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
