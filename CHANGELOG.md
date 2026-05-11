# Changelog

All notable changes to this project will be documented in this file. The format follows the guidelines from keepachangelog.com and Semantic Versioning.

## [Unreleased]

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
