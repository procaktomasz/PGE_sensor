# Changelog

All notable changes to this project will be documented in this file. The format follows the guidelines from keepachangelog.com and Semantic Versioning.

## [Unreleased]

- _No entries yet._

## [1.1.0] - 2026-02-01

### Changed

- Zmniejszono domyślny interwał odpytywania do 8 godzin i dodano 30-minutowe retry po błędach.
- Po udanym zapytaniu przywracany jest długi interwał, aby ograniczyć ruch.
- Sensory utrzymują ostatnią znaną wartość zamiast przechodzić w stan `unavailable` przy chwilowych błędach.

## [1.0.0] - 2026-01-31

### Added

- Initial release of the PGE Sensor integration.
