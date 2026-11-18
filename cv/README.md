# CV: Markdown → HTML → PDF

Generator PDF jest niezależny od Hugo i publikowania portfolio.
Sekcja Experience portfolio również czyta opisy pracodawców bezpośrednio
z `cv/cv.md`; zmiana treści wymaga przebudowania strony oraz dokumentu.
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
oraz statycznymi fontami IBM Plex Sans Regular/Medium/SemiBold/Bold.
Engineering Blueprint jest jedynym stylem dokumentu. Nie wymaga serwera,
zasobów sieciowych ani zależności npm. Osadzony skrypt `paginate.js`
rozmieszcza treść przed drukowaniem; widok ekranowy pozostaje ciągły.
Fonty wraz z licencją są w `cv/fonts/`; nie trzeba ich instalować w systemie.

Po zmianie Markdown lub CSS ponownie wykonaj `make cv`.
Własny Pandoc: `make cv PANDOC=/ścieżka/do/pandoc`.
HTML, środowisko Pythona i lokalne podglądy są ignorowane przez Git.
Wynikowy PDF jest plikiem portfolio i jest przeznaczony do zapisania w Git.

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
bez dostępu do sieci, czeka na osadzone fonty i generuje **`static/files/Maciej_Plocki_CV.pdf`**.
Używa A4 i marginesów z CSS, skali 100%, bez nagłówków/stopek przeglądarki.
PDF zawiera tekst, linki i znaczniki struktury dokumentu. Fonty są osadzane
jako CID TrueType z mapowaniem Unicode. Po eksporcie nagłówki sekcji i running
header otrzymują znaczniki Span / ActualText, aby tracking nie powodował
dodatkowych spacji przy ekstrakcji tekstu przez Poppler. Pozycje liter pozostają
bez zmian. Przeglądarka jest przypięta wersją Playwright; zmiana struktury
PDF niezgodna z tym krokiem zatrzymuje eksport przed zastąpieniem wyniku.
**Poprzedni PDF jest zastępowany dopiero po przejściu podstawowej kontroli eksportu i kompletności treści.**
Każdy eksport zastępuje `static/files/Maciej_Plocki_CV.pdf`. Przycisk „My Resume”
w sekcji About wskazuje `/files/Maciej_Plocki_CV.pdf`; Hugo publikuje go z katalogu
`static/files/`. Nazwa i ścieżka wynikowego PDF są stałe.

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

Nie ma sztywnego limitu stron, minimum wielkości fontu ani walidacji geometrii.
Eksport wymaga osadzenia CID TrueType i oczekiwanej struktury nagłówków PDF. Liczba i wymiary stron oraz
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

Nazwa firmy jest po lewej, a stanowisko i okres po prawej w jednym wierszu;
branża i link pozostają poniżej. Każdy pracodawca jest grupowany w całość
od nagłówka po technologie. Druk unika dzielenia tych grup oraz sekcji
podsumowania i kompetencji między stronami. Blok wyższy niż pełna strona
może zostać podzielony przez przeglądarkę i wymaga przeglądu wizualnego.
Przed eksportem `paginate.js` mierzy naturalną wysokość bloków przy docelowej
szerokości druku i załadowanych fontach. Wypełnia kolejne strony całymi blokami,
a odstępy między blokami dopasowują się w zakresie 12–24 px. Nadmiar wolnego
miejsca zostaje na dole strony. Linie pozostają tylko pod nagłówkami sekcji
nadrzędnych. Wymiary strony i marginesy
pochodzą ze zmiennych CSS; sekcje nie mają narzuconych wysokości.
AKRA Polska i EURA7 są wyjątkiem redakcyjnym: trafiają razem na osobną ostatnią
stronę. Klauzula rekrutacyjna pochodzi z bloku `.recruitment-clause`
w `cv.md` i jest dosuwana do dołu ostatniej strony (9 pt, wyrównanie do lewej).
Jeśli brak klauzuli, dolne 22 mm pozostają zarezerwowane.
Po zamknięciu druku wraca widok ciągły.
Nie ma ukrywania treści ani skalowania tekstu. Numer telefonu pozostaje
tekstem zgodnie ze źródłem.

## Ręczne drukowanie z przeglądarki

Otwórz HTML, poczekaj na fonty i wybierz `Ctrl+P`: A4, pionowo, skala 100%,
bez nagłówków i stopek. Pozostaw marginesy CSS — 16 mm góra/dół,
14 mm lewo/prawo. Tła nie są wymagane.
Do przygotowania dokumentu rekrutacyjnego zalecane jest `make cv-pdf`,
które stosuje te ustawienia i uruchamia kontrolę wyniku.

## Typografia i kontrola ekstrakcji

Engineering Blueprint: IBM Plex Sans, grafit/teal, geometryczne separatory,
tekst główny 11 pt, marginesy 16/14 mm. Na stronach od drugiej running header
mieści się w istniejącym górnym marginesie; stopka używa numeracji `01 / 04`.
Lokalne statyczne fonty i licencja SIL OFL 1.1 znajdują się w `cv/fonts/`.
Nie ma alternatywnych motywów ani zależności od zewnętrznego serwisu fontów.

Opcjonalna dodatkowa kontrola wymaga `pdffonts` i `pdftotext` z Poppler w PATH:

```sh
make cv-pdf-text-check
```

Nie nadpisuje PDF. Sprawdza cztery osadzone podzbiory CID TrueType, brak Type 3,
pełne nagłówki bez dodatkowych spacji w domyślnym oraz layoutowym trybie
`pdftotext`, a w trybie layout także kompletność tekstu względem HTML.
Domyślna ekstrakcja Popplera może usuwać łączniki przy łączeniu wierszy.
Wyniki narzędzi zapisują się jako `cv/review/pdffonts.txt`, `pdftotext.txt`
i `pdftotext-layout.txt`. Poppler nie jest wymagany do eksportu PDF.

## Ostatnia weryfikacja — 18 listopada 2026

Zaakceptowany Engineering Blueprint przeniesiono do standardowego eksportu.
Dokument zachowuje cztery strony A4, treść źródłową i pięć hiperłączy.
Po konsolidacji stylów wszystkie cztery strony są identyczne wizualnie
z zaakceptowanym PDF-em (porównanie rastra i pozycji znaków).
Usunięto kod wariantów, stare fonty oraz podglądy eksperymentu. Archiwalne
PDF-y w `static/files/` pozostają zachowane, a przycisk pobierania nadal
wskazuje jedyny aktualny dokument `Maciej_Plocki_CV.pdf`.
