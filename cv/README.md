# CV: Markdown → HTML → PDF

Generator jest niezależny od Hugo i publikowania portfolio. Jedynym źródłem
tekstu gotowego CV jest zatwierdzony `cv/cv.md` z PR #12 (`dac6ae2`).
Zawiera on już kontakt, doświadczenie i Languages. `experience.md` służy
filtrowi do rozpoznania nagłówków firm; nie jest ponownie dołączany.
Szablon, filtr i CSS nie zawierają kopii treści CV.

## Uruchomienie

Wymagania: GNU Make i [Pandoc](https://pandoc.org/installing.html) 3.x.
Na Ubuntu/WSL: `sudo apt install make pandoc` (sprawdź wersję Pandoc).
Z katalogu głównego repozytorium:

```sh
make cv
```

Otwórz `cv/generated.html` w przeglądarce. To samodzielny HTML z osadzonym CSS
oraz fontami Ubuntu Sans Regular/Bold 1.006. Nie wymaga serwera, JavaScriptu,
zasobów sieciowych ani zależności npm. Fonty są dostarczone wraz z licencją
w `cv/fonts/`; nie trzeba ich instalować w systemie. Użycie plików statycznych
pozwala Chromium osadzić w PDF fonty TrueType, zamiast fontów Type 3.

Po zmianie Markdown lub CSS ponownie wykonaj `make cv`.
Własny Pandoc: `make cv PANDOC=/ścieżka/do/pandoc`.
HTML i lokalny katalog podglądu `cv/review/` są ignorowane przez Git.

## Wydruk / zapis jako PDF

1. Otwórz HTML, poczekaj na wyświetlenie fontu i wybierz drukowanie (`Ctrl+P`).
2. Wybierz A4, orientację pionową i skalę 100%.
3. Wyłącz nagłówki i stopki przeglądarki (adres, datę, tytuł).
4. Pozostaw marginesy z CSS — 12 mm góra/dół, 14 mm lewo/prawo.
   Nie ustawiaj własnych marginesów w oknie drukowania.
5. Wybierz drukarkę lub „Zapisz jako PDF”. Tła nie są wymagane.

Pełna obecna treść mieści się na **trzech stronach A4**, przy tekście minimum
10,5 pt i interlinii 1,28. Długie opisy stanowisk i listy mogą przechodzić
między stronami. Krótkie metadane pozostają przy nagłówku firmy i początku
opisu; nagłówki nie pozostają osamotnione. Usunięto reguły `break-after: avoid`
z końców list i opisów oraz separatorów, które tworzyły niepotrzebne łańcuchy
blokad. Nie ma wymuszonej wysokości strony, skalowania tekstu ani ukrywania treści.
Przed wysłaniem sprawdź podgląd wydruku w używanej przeglądarce.

## Treść i układ

Pliki Markdown nie są redagowane przez generator. Filtr Lua:

- zagnieżdża firmy jako H3 w sekcji Professional Experience;
- usuwa z HTML powtarzane tytuły „Key Responsibilities & Achievements”;
- składa „Technologies” i pełną listę technologii jako metadane: na ekranie
  etykieta zajmuje osobny wiersz, a w wydruku lista rozpoczyna się obok niej
  i zawija w razie potrzeby;
- kompaktuje branżę i stronę firmy do wspólnego wiersza;
- odczytuje technologie poprzedzające `---` jako tekst, także gdy Pandoc
  rozpoznał je jako nagłówek Setext;
- obsługuje także poprzedni wariant źródła z samodzielnym linkiem
  `[Professional experience](experience.md)`, bez utraty kolejnych sekcji.

Zachowano jedną kolejność czytania: firma → stanowisko i okres → opis
oraz osiągnięcia → technologie. Tekst i wszystkie adresy linków pozostają
zgodne ze źródłem. Numer telefonu jest zwykłym tekstem, tak jak w Markdown.
E-mail ma odnośnik `mailto:`, a LinkedIn, GitHub i portfolio pełne adresy HTTPS.
HTML używa nagłówków, akapitów i list; PDF ma zaznaczalny tekst i klikalne linki.
Nie testowano konkretnego komercyjnego parsera ATS.

## Kontrola kompletności

Opcjonalna kontrola wymaga dodatkowo Python 3 (tylko biblioteka standardowa):

```sh
make cv-check
```

Kontrola niezależnie renderuje źródła przez Pandoc i porównuje cały tekst
z wygenerowanym HTML, z wyjątkiem uzgodnionych powtórzonych nagłówków.
Sprawdza obecność pełnego doświadczenia dokładnie raz, wszystkie `href`,
poprawność adresu `mailto:`, unikalność identyfikatorów oraz osadzenie fontu.
Test regresji sprawdza też starszy wariant z linkiem do doświadczenia,
z zachowaniem kontaktu i końcowej sekcji Languages.
Nie jest to automatyczny generator PDF.

## QA — 11 listopada 2026

Przyczyna wcześniejszego braku kontaktu/Languages: branch zawierał starsze
źródło `7fd17c0`, sprzed zatwierdzonego PR #12. Źródła CV zsynchronizowano
z `origin/main` (`dac6ae2`) bez ręcznych zmian zaakceptowanych treści.

Pandoc 3.6.4 i Chromium 156: sprawdzono desktop 1200 px, telefon 375 px
oraz wszystkie trzy strony PDF. Treść HTML jest zgodna z oboma źródłami,
bez duplikacji; tekst PDF odpowiada HTML. Minimum w PDF wynosi 10,5 pt.
Nie ma przycięć ani poziomego przewijania. Wszystkie dziewięć par firma–stanowisko
pozostaje na tej samej stronie. Wszystkie 13 linków w PDF odpowiada HTML.

Kontrola HTTP 12 linków WWW: dziesięć kończy się HTTP 200 (Nord Partner
przekierowuje do `https://pib-broker.pl/`); LinkedIn odpowiada 999, FTG 403.
Dostępności tych dwóch stron nie potwierdzono automatycznie. Nie zmieniano
adresów zapisanych w zaakceptowanych źródłach. Sprawdzono składnię `mailto:`
oraz zgodność z wyświetlanym adresem; nie wysyłano wiadomości.

Lokalne artefakty do oceny: `review/cv-print.pdf`, `review/page-1.png`,
`review/page-2.png`, `review/page-3.png`, `review/desktop.png`, `review/mobile.png`.
Istniejący PDF w `static/files/` pozostaje bez zmian. Nie wykonywano publikacji.
