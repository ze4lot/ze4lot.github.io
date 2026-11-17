PANDOC ?= pandoc
CV_VENV ?= .venv-cv
CV_PYTHON ?= $(CV_VENV)/bin/python

.PHONY: cv cv-check cv-setup cv-pdf cv-pdf-check cv-test
cv:
	@command -v "$(PANDOC)" >/dev/null 2>&1 || { echo "Install Pandoc (https://pandoc.org/installing.html), then run make cv." >&2; exit 1; }
	"$(PANDOC)" cv/cv.md --from=markdown-smart --to=html5 \
		--lua-filter=cv/layout.lua \
		--standalone --section-divs --embed-resources \
		--template=cv/template.html --css=cv/cv.css \
		--metadata=lang:en --metadata='pagetitle:Maciej Płocki — Software Architect / Technical Lead' \
		--output=cv/generated.html

cv-check: cv
	python3 cv/check.py --pandoc="$(PANDOC)"

# Optional PDF tooling; does not change the portfolio's dependencies.
cv-setup:
	python3 -m venv "$(CV_VENV)"
	"$(CV_PYTHON)" -m pip install -r cv/requirements-pdf.txt
	PLAYWRIGHT_BROWSERS_PATH="$(CV_VENV)/browsers" "$(CV_PYTHON)" -m playwright install chromium --only-shell

cv-pdf: cv-check
	@test -x "$(CV_PYTHON)" || { echo "Run make cv-setup before exporting PDF." >&2; exit 1; }
	PLAYWRIGHT_BROWSERS_PATH="$(CV_VENV)/browsers" "$(CV_PYTHON)" cv/pdf.py

# Validate the saved PDF against freshly generated HTML without overwriting it.
cv-pdf-check: cv-check
	@test -x "$(CV_PYTHON)" || { echo "Run make cv-setup before checking PDF." >&2; exit 1; }
	PLAYWRIGHT_BROWSERS_PATH="$(CV_VENV)/browsers" "$(CV_PYTHON)" cv/pdf.py --check-only

cv-test:
	@test -x "$(CV_PYTHON)" || { echo "Run make cv-setup before testing PDF tooling." >&2; exit 1; }
	PANDOC="$(PANDOC)" "$(CV_PYTHON)" -m unittest discover -s cv -p 'test_*.py'
