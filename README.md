# ze4lot.github.io

Portfolio: Hugo **0.170.0**, standalone Dart Sass **1.108.2**, Node.js **18**
and Go (Hugo Modules). Toha stays pinned to **v4.8.0** in `go.mod`.
Use the same tool versions locally as in the PR, publishing and theme-update
workflows. Install the [standalone Dart Sass binary](https://gohugo.io/functions/css/sass/#dart-sass)
outside the repository and add its directory to `PATH`; the npm `sass` package
does not provide the embedded protocol required by Hugo.

```sh
npm ci
hugo --minify
```

Hugo 0.170 removed embedded LibSass and the extended edition, so Dart Sass is
required even with the existing theme. `peaceiris/actions-hugo@v3.3.0` installs
both pinned binaries in CI. Warnings about `languageCode`, `.Site.Data`,
`.Site.LanguageCode` and deprecated Sass APIs do not fail this pinned build;
migrating the theme and its Sass dependencies is separate work.

After a push to `main`, the publishing workflow uploads `public/` and deploys
it with the official GitHub Pages actions and the automatic `GITHUB_TOKEN`
(`pages: write`, `id-token: write`). It no longer needs `PERSONAL_TOKEN` or
pushes to `gh-pages`. The `github-pages` environment must allow `main` (as it
already does in this repository). PRs build only; they never deploy.

Generator CV: `make cv` → `cv/generated.html`.
Eksport PDF: `make cv-setup` (jednorazowo), potem `make cv-pdf`
→ `static/files/Maciej_Plocki_CV.pdf` (przycisk „My Resume” w About).
Wymagania i kontrola jakości: [cv/README.md](cv/README.md).

Sekcja Experience w portfolio czyta bezpośrednio `Professional Experience`
z `cv/cv.md`: te same firmy, stanowiska, okresy, branże, opisy, osiągnięcia
i technologie, w tej samej kolejności. Nie utrzymujemy drugiej kopii treści
w YAML. Po edycji CV przebuduj portfolio (`hugo --minify`) i PDF (`make cv-pdf`).
Ustawienia sekcji pozostają w `data/en/sections/experiences.yaml`.

Sekcja About pod hero pobiera również imię i nazwisko, tytuł zawodowy oraz pełne
`Professional Summary` z `cv/cv.md`, bez osobnej kopii w `about.yaml`.
