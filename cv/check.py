"""Check content and hrefs independently of the layout filter (stdlib + Pandoc)."""
import argparse
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit


class Content(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.links = []
        self.ids = []
        self.feed(html)

    def handle_data(self, data):
        self.text.append(data)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if "id" in attrs:
            self.ids.append(attrs["id"])

    def normalized(self):
        return " ".join(" ".join(self.text).split())


def render(markdown, pandoc="pandoc"):
    args = [pandoc, "--from=markdown-smart", "--to=html5"]
    return subprocess.check_output(args, input=markdown, text=True)


def expected(markdown, pandoc="pandoc"):
    # Only the explicitly approved presentation omissions, independent of Lua.
    markdown = re.sub(r"(?m)^### Key Responsibilities & Achievements\s*$", "", markdown)
    return Content(render(markdown, pandoc))


def compare(actual, reference):
    assert actual.normalized() == reference.normalized(), "Missing, duplicated or reordered content"
    assert Counter(actual.links) == Counter(reference.links), "Missing, duplicated or changed href"
    assert len(actual.ids) == len(set(actual.ids)), "Duplicate HTML ids"
    for href in actual.links:
        assert href and not re.search(r"\s", href), f"Invalid href: {href!r}"
        parsed = urlsplit(href)
        if parsed.scheme in ("https", "http"):
            assert parsed.netloc, f"Missing hostname: {href}"
        elif parsed.scheme == "mailto":
            assert re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", unquote(parsed.path)), href
        elif href.startswith("#"):
            assert unquote(href[1:]) in actual.ids, href
        else:
            raise AssertionError(f"Unexpected or local href: {href}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pandoc", default="pandoc")
    pandoc = parser.parse_args().pandoc
    source = Path("cv/cv.md").read_text()
    reference = expected(source, pandoc)
    html = Path("cv/generated.html").read_text()
    main = re.search(r'<main class="cv">(.*?)</main>', html, flags=re.S)
    assert main, "Missing CV main element"
    actual = Content(main[1])
    compare(actual, reference)
    assert "data:font/" in html or "data:application/" in html, "Font is not embedded"
    print(f"PASS: complete cv.md content, no duplication, {len(actual.links)} exact hrefs")
