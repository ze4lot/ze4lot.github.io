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
**Poprzedni PDF jest zastępowany dopiero po przejściu kontroli jakości.**
Nie nadpisuje plików w `static/files/`.

Po eksporcie powstają również:

- `cv/review/page-1.png`, `page-2.png`, `page-3.png`, `page-4.png` — podgląd wszystkich stron;
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
bez filtra układu i porównuje pełny tekst z HTML, z wyjątkiem uzgodnionych
powtórzonych nagłówków osiągnięć. Sprawdza też wszystkie `href`, składnię
`mailto:`, unikalność identyfikatorów i osadzenie fontu.

Kontrola PDF, wykonywana przy każdym eksporcie, sprawdza:

- dokładnie cztery niepuste strony A4 w pionie;
- pełną zgodność tekstu i kolejności z HTML, także kontakt i Languages;
- minimum 10,5 pt oraz brak tekstu poza stroną;
- osadzenie fontów i brak fontów Type 3;
- zgodność linków PDF z HTML;
- obecność nagłówka firmy i stanowiska z okresem na tej samej stronie.

Nie sprawdza dostępności stron WWW ani konkretnego komercyjnego parsera ATS.
Kontrola automatyczna uzupełnia wizualny przegląd przed wysłaniem dokumentu.
Liczba stron jest celowym warunkiem kontroli — rozbudowa treści wymagająca
piątej strony zatrzyma eksport i wymaga świadomej decyzji o składzie.

Po `make cv-setup` uruchom testy regresji:

```sh
make cv-test
```

Obejmują one generowanie bez `experience.md`, nieznaną wcześniej firmę,
zachowanie kontaktu i końcowych sekcji oraz wykrywanie uszkodzonej treści,
linków, małego tekstu, złej liczby stron i osamotnionego nagłówka w PDF.

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

Pandoc 3.6.4, Playwright 1.65.2 / Chromium 159.0.8154.6, PyMuPDF 1.28.2:
cztery strony A4, minimum 10,5 pt, pełny tekst, 13 linków i dziewięć par
firma–stanowisko. Testy regresji przeszły. Zaktualizowano Professional Summary, Core Competencies i Bikeparks oraz
uzgodniony warunek czterech stron. CSS i istniejący PDF portfolio pozostały bez zmian.
