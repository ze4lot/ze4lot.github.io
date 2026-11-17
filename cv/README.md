# CV: Markdown → HTML → PDF

Generator jest niezależny od Hugo i publikowania portfolio.
**`cv/cv.md` jest jedynym źródłem treści i struktury gotowego CV.**
`experience.md` pozostaje materiałem roboczym; generator i kontrole nie czytają
tego pliku ani nie wymagają utrzymywania dwóch zgodnych kopii doświadczenia.

## HTML

Wymagania: GNU Make i [Pandoc](https://pandoc.org/installing.html) 3.x
(zweryfikowano z 3.6.4). Z katalogu głównego repozytorium:

```sh
make cv
make cv-check
```

Otwórz `cv/generated.html` w przeglądarce. To samodzielny HTML z osadzonym CSS
oraz fontami Ubuntu Sans Regular/Bold 1.006. Nie wymaga serwera, JavaScriptu,
zasobów sieciowych, zależności npm ani narzędzi do eksportu PDF.
Fonty wraz z licencją są w `cv/fonts/`; nie trzeba ich instalować w systemie.

Po zmianie Markdown lub CSS ponownie wykonaj `make cv`.
Własny Pandoc: `make cv PANDOC=/ścieżka/do/pandoc`.
HTML, PDF, środowisko Pythona i lokalne podglądy są ignorowane przez Git.

## Automatyczny eksport PDF

Dodatkowo potrzebne są Python 3.10+ z modułem `venv`, dostęp do pobrania pakietów
podczas instalacji i biblioteki systemowe wymagane przez Chromium.
Jednorazowo:

```sh
make cv-setup
```

Tworzy to `.venv-cv/` i instaluje ustalone wersje Playwright 1.65.2, PyMuPDF
1.28.2 i greenlet 3.5.6. Przeglądarka dobrana przez Playwright jest instalowana
w `.venv-cv/browsers/`, niezależnie od wspólnego cache i przeglądarek użytkownika.
Nie zmienia to zależności portfolio. W razie brakujących bibliotek systemowych
zobacz [instalację Playwright](https://playwright.dev/python/docs/browsers#install-system-dependencies).

Następnie:

```sh
make cv-pdf
```

Polecenie odtwarza HTML, sprawdza jego zgodność ze źródłem, uruchamia Chromium
bez dostępu do sieci, czeka na osadzone fonty i generuje **`cv/generated.pdf`**.
Używa A4 i marginesów z CSS, skali 100%, bez nagłówków/stopek przeglądarki.
PDF zawiera tekst, linki i znaczniki struktury dokumentu.
**Poprzedni PDF jest zastępowany dopiero po przejściu podstawowej kontroli eksportu i kompletności treści.**
Nie nadpisuje plików w `static/files/`.

Po eksporcie powstają również:

- `cv/review/page-N.png` — podgląd każdej wygenerowanej strony;
  nieaktualne podglądy poprzedniego eksportu są usuwane;
- `cv/review/pdf-qa.json` — wyniki kontroli, wersje renderera oraz SHA-256 źródła,
  HTML i PDF.

Powtarzalność dotyczy składu i ustawień; metadane czasu w PDF mogą się różnić.
Aby sprawdzić zapisany PDF względem aktualnego Markdown, bez ponownego eksportu:

```sh
make cv-pdf-check
```

Zmienne `CV_VENV` i `CV_PYTHON` pozwalają wskazać inne środowisko Pythona.
`make cv-setup` trzeba powtórzyć po zmianie `requirements-pdf.txt`.

## Kontrole i testy

`make cv-check` wymaga tylko Python 3 i Pandoc. Niezależnie renderuje źródło
bez filtra układu i porównuje pełny tekst i linki z HTML, z wyjątkiem
uzgodnionych powtórzonych nagłówków osiągnięć. Brak, zmiana lub powielenie
treści albo linków blokuje generowanie. Powtórzone identyfikatory HTML i brak
wykrytego osadzonego fontu są ostrzeżeniami.

Kontrola PDF blokuje eksport tylko wtedy, gdy plik jest nieczytelny,
zablokowany, nie zawiera stron lub tekstu albo jego treść jest niekompletna.
Porównuje liczności słów i znaków interpunkcyjnych z HTML, bez narzucania
kolejności ekstrakcji — pozwala to później stosować układy wielokolumnowe.
Nie jest to porównanie znaczenia ani gwarancja poprawnej kolejności czytania.
Różnice kolejności tekstu lub linków oraz strony bez tekstu są raportowane
jako ostrzeżenia i nie blokują zapisu PDF.

Nie ma sztywnego limitu stron, minimum wielkości fontu ani walidacji geometrii,
położenia nagłówków lub osadzenia fontów PDF. Liczba i wymiary stron oraz
najmniejszy rozmiar tekstu są informacjami w `cv/review/pdf-qa.json`.
Renderer nadal czeka na załadowanie zadeklarowanych fontów i zasobów.
Błąd renderowania lub ładowania zasobów zatrzymuje eksport; poprzedni PDF
pozostaje zachowany.

**Przed wysłaniem CV przejrzyj wszystkie podglądy stron:** oceń czytelność,
ucięcia, kolejność czytania, podziały stron i linki. Udany eksport techniczny
nie oznacza zatwierdzenia składu. Narzędzia nie sprawdzają dostępności stron
WWW ani konkretnego komercyjnego parsera ATS.

Po `make cv-setup` uruchom testy regresji:

```sh
make cv-test
```

Testy obejmują jedno źródło treści, nieznaną wcześniej firmę, kontakt i sekcje
końcowe, brak lub zmianę tekstu/linków w HTML, uszkodzony lub pusty PDF oraz
brak, zmianę i duplikację tekstu w PDF. Sprawdzają też, że zmiany liczby stron,
fontu, geometrii, podziałów, kolejności ekstrakcji i linków PDF nie blokują
poprawnego eksportu z kompletną treścią.

## Konwencje Markdown i układ

Generator nie zmienia Markdown. W sekcji `## Professional Experience`
każda firma ma nagłówek `##`, a po nim akapit rozpoczynający się od
`**Stanowisko | okres**`. Filtr `layout.lua` rozpoznaje tę strukturę bez listy
nazw firm z zewnętrznego pliku. Kolejna sekcja `##` bez takiego akapitu
(np. Languages) kończy doświadczenie.

Filtr zagnieżdża firmy jako H3, usuwa powtarzane nagłówki
„Key Responsibilities & Achievements” i składa technologie jako metadane.
Na ekranie etykieta „Technologies” zajmuje osobny wiersz; w druku lista
rozpoczyna się obok niej. Branża i strona firmy są w jednym wierszu.
Obsługiwane są też technologie błędnie odczytane przez Markdown jako nagłówki
Setext wskutek braku pustej linii przed `---`.

Zachowano układ firma → stanowisko i okres → opis i osiągnięcia → technologie.
Długie opisy i listy mogą przechodzić między stronami; krótkie metadane
pozostają z nagłówkiem firmy i początkiem opisu. Nie ma ukrywania treści
ani skalowania tekstu. Numer telefonu pozostaje tekstem zgodnie ze źródłem.

## Ręczne drukowanie z przeglądarki

Otwórz HTML, poczekaj na fonty i wybierz `Ctrl+P`: A4, pionowo, skala 100%,
bez nagłówków i stopek. Pozostaw marginesy CSS — 12 mm góra/dół,
14 mm lewo/prawo. Tła nie są wymagane.
Do przygotowania dokumentu rekrutacyjnego zalecane jest `make cv-pdf`,
które stosuje te ustawienia i uruchamia kontrolę wyniku.

## Ostatnia weryfikacja — 17 listopada 2026

Zaktualizowano AKRA i EURA7, zachowując korekty Agent Orchestration i Bikeparks.
Uproszczono QA do poprawności eksportu i kompletności treści, z diagnostyką
nieblokującą zmian składu. Aktualny eksport i testy sprawdzono poleceniami
`make cv`, `make cv-check`, `make cv-pdf`, `make cv-pdf-check` i `make cv-test`.
CSS oraz istniejący PDF portfolio pozostały bez zmian.
