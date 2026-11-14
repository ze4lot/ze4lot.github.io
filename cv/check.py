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


def render(markdown, filtered=False):
    args = [pandoc, "--from=markdown-smart", "--to=html5"]
    if filtered:
        args.append("--lua-filter=cv/include-experience.lua")
    return subprocess.check_output(args, input=markdown, text=True)


def expected(markdown):
    # Only the explicitly approved presentation omissions, independent of Lua.
    markdown = markdown.replace("[Professional experience](experience.md)", experience)
    markdown = re.sub(r"(?m)^### Key Responsibilities & Achievements\s*$", "", markdown)
    return Content(render(markdown))


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
    experience = re.sub(r"\A# [^\n]+\n", "", Path("cv/experience.md").read_text())
    reference = expected(source)
    assert reference.normalized().count(expected(experience).normalized()) == 1, "Experience source differs or is duplicated"
    html = Path("cv/generated.html").read_text()
    main = re.search(r'<main class="cv">(.*?)</main>', html, flags=re.S)
    assert main, "Missing CV main element"
    actual = Content(main[1])
    compare(actual, reference)
    assert "data:font/" in html or "data:application/" in html, "Font is not embedded"
    print(f"PASS: complete content from both sources, no duplication, {len(actual.links)} exact hrefs")

    # Regression: linked experience must not lose contact or trailing Languages.
    legacy = re.sub(
        r"(## Professional Experience\s*\n).*?(?=^## Languages\s*$)",
        r"\1\n[Professional experience](experience.md)\n\n",
        source, flags=re.M | re.S,
    )
    assert legacy != source, "Legacy fixture did not replace inline experience"
    compare(Content(render(legacy, filtered=True)), reference)
    print("PASS: legacy link expansion preserves contact and trailing Languages exactly once")
