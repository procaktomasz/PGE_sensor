# Changelog

All notable changes to this project will be documented in this file. The format follows the guidelines from keepachangelog.com and Semantic Versioning.

## [Unreleased]

## [1.6.0] - 2026-11-12

### Added
- PL: Czytelny wybór konta w kreatorze konfiguracji: adres punktu poboru, numer PPE, numer konta oraz oznaczenia (domyślne, prosument, ARCHIWALNE). Konta aktywne są wyświetlane przed archiwalnymi (#7, dzięki uprzejmości @ciechompl).
- EN: Readable account selection in the config flow: supply point address, PPE number, account number and flags (default, prosument, ARCHIVED). Active accounts are listed before archived ones (#7, courtesy of @ciechompl).
- PL: Nowe sensory: kwota rzeczywistej faktury rozliczeniowej, wartość rozliczenia energii (PLN), prognozowany pobór z dokumentu płatności, data potwierdzonego salda banku oraz bank S1 i S2 po opuście (#8, dzięki uprzejmości @ciechompl). Opis w `docs/settlement-sensors.md`.
- EN: New sensors: actual settlement invoice amount, energy settlement value (PLN), forecast consumption from the payment document, confirmed bank balance date, and bank S1 and S2 after the discount factor (#8, courtesy of @ciechompl). Details in `docs/settlement-sensors.md`.
- PL: Testy jednostkowe w folderze `tests/`.
- EN: Unit tests in the `tests/` folder.

### Changed
- PL: Nowo tworzone encje dostają krótkie identyfikatory, np. `sensor.pge_saldo` przy jednym koncie lub `sensor.pge_<numer_konta>_saldo` przy kilku kontach. Identyfikatory istniejących encji nie są zmieniane.
- EN: Newly created entities get short IDs, e.g. `sensor.pge_saldo` for a single account or `sensor.pge_<account_number>_saldo` for multiple accounts. Existing entity IDs are not changed.
- PL: Energia pobrana, wprowadzona i okres rozliczeniowy pochodzą z ostatniej rzeczywistej faktury (`INVOICE`). Prognoza (`PREPAYMENT_INVOICE`) nie zastępuje już pomiaru.
- EN: Consumed energy, feed-in energy and billing period now come from the latest actual invoice (`INVOICE`). A forecast (`PREPAYMENT_INVOICE`) no longer replaces the measurement.
- PL: `PGE Magazyn energii` pokazuje sumę stref S1/S2 po zastosowaniu współczynnika opustu PGE zamiast surowego salda pierwszej strefy.
- EN: `PGE Magazyn energii` shows the sum of zones S1/S2 after PGE's discount factor instead of the raw balance of the first zone.
- PL: Sensory energii z faktury, prognozy i banku nie mają już `state_class` (nie są licznikami kumulacyjnymi). Nie należy ich używać jako źródła w panelu Energia.
- EN: Invoice energy, forecast and bank sensors no longer have a `state_class` (they are not cumulative meters). Do not use them as sources in the Energy dashboard.
- PL: Zmieniono nazwy wyświetlane części sensorów, aby jasno opisywały źródło danych. Identyfikatory encji pozostają bez zmian.
- EN: Display names of some sensors were changed to describe the data source clearly. Entity IDs remain unchanged.

### Deprecated
- PL: Sensor „Zużycie po rozliczeniu” jest wycofany i automatycznie wyłączany, ponieważ wartość PLN była wystawiana jako kWh. Historia encji jest zachowana. Poprawną kwotę pokazuje nowy sensor „Wartość rozliczenia energii (PLN)”.
- EN: The "Zużycie po rozliczeniu" sensor is deprecated and disabled automatically because a PLN value was exposed as kWh. Entity history is kept. The correct amount is provided by the new "Wartość rozliczenia energii (PLN)" sensor.

## [1.5.2] - 2026-11-12

### Fixed
- PL: Dodano brakujący plik `hacs.json`. Bez niego HACS odrzucał instalację integracji z repozytorium (zgłoszenie #10).
- EN: Added the missing `hacs.json` file. Without it HACS refused to install the integration from the repository (issue #10).

## [1.5.1] - 2026-08-13

### Fixed
- PL: Poprawiono obsługę błędów podczas logowania w kreatorze dodawania integracji. Błędy związane z połączeniem, przekroczeniem limitu zapytań (np. API zwracające 403 lub timeout) nie będą już błędnie zgłaszane jako "invalid_auth" (nieprawidłowe dane logowania), lecz poprawnie jako "cannot_connect". Ułatwi to diagnozę problemów np. przy dodawaniu kolejnych kont.
- EN: Fixed error handling during login in the config flow. Connection errors and rate limits (e.g. API returning 403 or timeout) will no longer incorrectly report as "invalid_auth" (invalid credentials), but properly as "cannot_connect". This improves diagnostics e.g. when adding multiple accounts.

## [1.5.0] - 2026-08-13

### Added
- PL: Pełne wsparcie dla kont posiadających wiele Punktów Poboru Energii (PPE) / wiele liczników! Od teraz podczas konfiguracji możesz wybrać konkretny licznik do zaimportowania lub dodać wszystkie naraz. Każdy licznik trafia do Home Assistanta jako osobne, odpowiednio nazwane urządzenie ze swoimi własnymi sensorami (dzięki uprzejmości @JarDol). Kolejne punkty można dodać później, uruchamiając dodawanie integracji ponownie z tymi samymi danymi logowania.
- EN: Full support for accounts with multiple points of consumption (PPE) / multiple meters! During configuration, you can now pick a specific meter to import or add all of them at once. Each meter is imported into Home Assistant as a distinct, properly named device with its own set of sensors (courtesy of @JarDol). Additional points can be added later by running "Add integration" again with the same credentials.

## [1.4.4] - 2026-08-11

### Added
- PL: Dodano automatyczne sortowanie rozbicia miesięcznego w atrybutach sensora `PGE Magazyn energii` od najnowszej do najstarszej daty.
- EN: Added automatic sorting of monthly breakdowns in the `PGE Magazyn energii` sensor attributes from newest to oldest date.

### Fixed
- PL: Usunięto błąd "Login failed: incorrect credentials" wywoływany przez wysyłanie wygasłego tokenu do punktu logowania po upływie 8-godzinnej sesji w tle.
- EN: Fixed "Login failed: incorrect credentials" caused by sending a stale token to the login endpoint after the 8-hour background session expired.

## [1.4.3] - 2026-08-10

### Fixed
- PL: Naprawiono błąd wygasania sesji po kilku godzinach, który powodował, że Home Assistant wyrzucał błąd "Failed to fetch billing accounts".
- EN: Fixed session expiration bug that caused Home Assistant to throw "Failed to fetch billing accounts" after several hours.

## [1.4.2] - 2026-08-09

### Added
- PL: Dodano sensor `PGE Okres rozliczeniowy` podający w formie tekstu przedział dat, za który została wystawiona najnowsza faktura.
- EN: Added `PGE Okres rozliczeniowy` (Billing Period) sensor exposing the date range for the latest invoice.
- PL: Dodano sensor `PGE Bieżąca płatność` podający kwotę, jaka pozostała do zapłaty dla najnowszej faktury.
- EN: Added `PGE Bieżąca płatność` (Current Payment) sensor exposing the exact remaining amount to be paid for the latest invoice.

### Fixed
- PL: Usunięto błąd, który wymuszał wyzerowanie sensora `PGE Saldo` jeśli najnowsze dokumenty miały status opłaconych. Zmiana przywraca prawidłowe wyświetlanie nadpłat oraz zadłużeń innych niż standardowe faktury.
- EN: Removed a bug that forced the `PGE Saldo` sensor to 0.0 if recent documents were paid. This change restores accurate reporting of overpayments and non-invoice debts.

## [1.4.1] - 2026-08-07

### Added
- PL: Dodano nowy sensor `PGE Magazyn energii`, który podaje ilość pozostałej energii do rozliczenia (w kWh) oraz wyświetla w atrybutach szczegółowe, miesięczne podsumowanie rozliczeń magazynu prosumenckiego.
- EN: Added new `PGE Magazyn energii` (Energy Storage) sensor exposing the remaining energy balance and detailed monthly prosumer storage data as attributes.
- PL: Dodano nowe sensory energii dla ostatniej faktury: Kwota faktury, Energia pobrana, Energia wprowadzona (dla prosumentów) oraz Zużycie po rozliczeniu (wyrażone w kWh z obsługą Panelu Energia).
- EN: Added new energy sensors for the latest invoice: Invoice Amount, Consumed Energy, Feed-in Energy (for prosumers) and Settled Energy (in kWh, compatible with HA Energy Dashboard).
- PL: Dodano nowe atrybuty do głównego sensora salda (m m.in. PPE, Data opłacenia, Status płatności).
- EN: Added new attributes to the main balance sensor (e.g. PPE, Paid Date, Payment Status).

### Fixed
- PL: Naprawiono błąd polegający na niezwracaniu zerowego salda po opłaceniu faktury przez odczytywanie statusu bezpośrednio z dokumentu zamiast z salda ogólnego.
- EN: Fixed an issue where the balance would not return 0.0 after invoice payment by checking the payment status directly from the document instead of the general balance.

## [1.3.0] - 2026-07-10

### Added
- PL: Przejście na nowe, stabilniejsze i szybsze API PGE (zamiast powolnego parsowania HTML z portalu eBOK).
- EN: Transition to a new, more stable and faster PGE API (replacing slow HTML scraping of the eBOK portal).

### Changed
- PL: Oczyszczono repozytorium ze starych, niepotrzebnych skryptów diagnostycznych i zrzutów HAR. Uporządkowano kod.
- EN: Cleaned up the repository from old diagnostic scripts and HAR dumps. Code refactoring.

## [1.2.7] - 2026-05-19

### Fixed
- PL: Naprawiono błąd parsowania odpowiedzi z częściowym kodem HTML w XML podczas przekierowań (zastąpiono `xml.etree.ElementTree` przez `BeautifulSoup`).
- EN: Fixed parsing error of partial HTML within XML responses during redirects (replaced `xml.etree.ElementTree` with `BeautifulSoup`).

## [1.2.6] - 2026-05-13

### Fixed
- PL: Naprawiono błąd parsowania faktur wynikający ze zmiany struktury tabel HTML na stronie PGE eBOK (nowe klasy, brak ID tabeli `fakturaDoZaplaty`). Skrypt dynamicznie rozpoznaje teraz kolumny "Płatne do" oraz "Do zapłaty" niezależnie od sztywnej struktury dokumentu.
- EN: Fixed invoice parsing error caused by HTML table structure changes on the PGE eBOK website. The script now dynamically identifies "Płatne do" (Due date) and "Do zapłaty" (Amount to pay) columns.

## [1.2.5] - 2026-05-12

### Fixed
- PL: Poprawiono błąd parsowania eBOK, przez który zerowe saldo zwracane w formacie "0 zł" (zamiast "0,00 zł") rzucało ostrzeżeniami w logach Home Assistanta.
- EN: Fixed an eBOK parsing issue where zero balances formatted as "0 PLN" (instead of "0,00 PLN") triggered warnings in Home Assistant logs.

## [1.2.4] - 2026-05-11

### Fixed
- PL: Usprawniono parsowanie eBOK dla kont z zerowym saldem, dodając obsługę nowych wariantów komunikatów (np. "brak nierozliczonych", "nie masz żadnych rachunków").
- EN: Improved eBOK parsing for zero-balance accounts by supporting new message variants.
- PL: Dodano wykrywanie prac serwisowych (np. "przerwa techniczna"), zapobiegając błędnemu raportowaniu zerowego salda, gdy portal jest niedostępny.
- EN: Added maintenance detection to prevent falsely reporting zero balance when the portal is down.
- PL: Rozszerzono wyrażenia regularne do wyciągania kwoty salda o nowe słowa kluczowe ("należność", "bieżące" itd.).
- EN: Expanded balance extraction regex with new keywords.

## [1.2.3] - 2026-04-28

### Fixed
- PL: Zredukowano fałszywe ostrzeżenia "Could not parse outstanding payments" dla kont z zerowym saldem poprzez dodanie rozpoznawania komunikatu "brak danych" na stronie eBOK.
- EN: Reduced false positive "Could not parse outstanding payments" warnings for zero-balance accounts by recognizing the "brak danych" (no data) message on the eBOK website.

### Changed
- PL: Ujednolicono działanie samodzielnego skryptu `pge_scraper.py`, aby poprawnie obsługiwał konta z zerowym saldem, zwracając 0.0 zamiast zgłaszać błąd.
- EN: The standalone `pge_scraper.py` script now gracefully handles zero-balance accounts by returning 0.0 instead of raising an error, consistent with the Home Assistant integration.

## [1.2.2] - 2026-03-02

### Fixed

- PL: Naprawiono błąd "Could not find any outstanding payments in response" gdy użytkownik nie ma żadnych faktur do zapłaty. Zamiast wyrzucać wyjątek, integracja teraz zwraca saldo 0.0.
- EN: Fixed "Could not find any outstanding payments in response" error when user has no outstanding invoices. The integration now gracefully returns 0.0 balance instead of raising an exception.

## [1.2.1] - 2026-02-06

### Fixed

- PL: Odtworzono kompletną klasę `PgeEbokCoordinator`, dzięki czemu komponent ładuje się poprawnie w Home Assistant nawet po ręcznej instalacji.
- EN: Restored the full `PgeEbokCoordinator` definition so the component imports correctly in Home Assistant, including manual deployments.

## [1.2.0] - 2026-02-05

### Fixed

- Eliminowano `PgeScraperError` dla kont z saldem 0 PLN poprzez rozpoznawanie komunikatów „brak zaległości” i zwracanie kontrolnej wartości `0.0`.
- Parser finansów uwzględnia teraz dodatkowe frazy i wzorce kwot, co zwiększa odporność na zmiany frontendu PGE.

### Changed

- Koordynator przywraca/skraca interwały z jednego miejsca i obejmuje niespodziewane wyjątki, aby logi oraz retry zachowywały się przewidywalnie.
- Dokumentacja opisuje aktualny 8-godzinny interwał odczytu oraz 30-minutowe próby po błędach.

## [1.1.0] - 2026-02-01

### Changed

- Zmniejszono domyślny interwał odpytywania do 8 godzin i dodano 30-minutowe retry po błędach.
- Po udanym zapytaniu przywracany jest długi interwał, aby ograniczyć ruch.
- Sensory utrzymują ostatnią znaną wartość zamiast przechodzić w stan `unavailable` przy chwilowych błędach.

## [1.0.0] - 2026-01-31

### Added

- Initial release of the PGE Sensor integration.
- Inicjalizacja projektu
