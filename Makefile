PANDOC ?= pandoc

.PHONY: cv cv-check
cv:
	@command -v "$(PANDOC)" >/dev/null 2>&1 || { echo "Install Pandoc (https://pandoc.org/installing.html), then run make cv." >&2; exit 1; }
	$(PANDOC) cv/cv.md --from=markdown-smart --to=html5 \
		--lua-filter=cv/include-experience.lua \
		--standalone --section-divs --embed-resources \
		--template=cv/template.html --css=cv/cv.css \
		--metadata=lang:en --metadata=pagetitle:CV \
		--output=cv/generated.html

cv-check: cv
	python3 cv/check.py --pandoc="$(PANDOC)"
