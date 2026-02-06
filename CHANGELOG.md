# Changelog

All notable changes to this project will be documented in this file. The format follows the guidelines from keepachangelog.com and Semantic Versioning.

## [Unreleased]

- _In process._

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
