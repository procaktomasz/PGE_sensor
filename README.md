# PGE Sensor

## 🇵🇱 Wersja polska

### Opis
Ten projekt łączy prosty skrypt CLI oraz integrację Home Assistant do pobierania informacji o zaległościach z portalu PGE Sensor. Dane są scrapowane bezpośrednio z panelu klienta i prezentowane jako:
- komunikat w konsoli (`pge_scraper.py`) dla szybkiej kontroli salda,
- sensory w Home Assistant (stan konta + termin płatności) poprzez komponent `custom_components/pge_sensor`.

### Wymagania
- Python 3.10+ z zainstalowanymi bibliotekami `requests` oraz `beautifulsoup4`.
- Aktywne konto w serwisie https://ebok.gkpge.pl.
- (Opcjonalnie) instancja Home Assistant z możliwością instalacji niestandardowych komponentów.

### Instalacja przez HACS
1. W Home Assistant otwórz HACS → Integracje i kliknij menu z trzema kropkami → `Custom repositories`.
2. Dodaj `https://github.com/procaktomasz/PGE_sensor` jako repozytorium typu `Integration` i zatwierdź.
3. Wróć do listy integracji HACS, wyszukaj „PGE Sensor” i zainstaluj komponent.
4. Po restarcie HA dodaj integrację „PGE Sensor” z poziomu ustawień (`Konfiguracja → Urządzenia i Usługi`).

### Integracja z Home Assistant
1. Skompletuj katalog `custom_components/pge_sensor` w folderze `config/custom_components` swojej instalacji HA.
2. Przeładuj HA lub wykonaj `Odśwież integracje`.
3. Dodaj integrację „PGE Sensor” z poziomu interfejsu (Konfiguracja → Urządzenia i Usługi → Dodaj integrację) i podaj dane logowania.
4. Koordynator aktualizuje dane co 12 godzin (`SCAN_INTERVAL`). Sensory:
   - `PGE Balance` (`sensor.pge_balance`) – saldo w PLN.
   - `PGE Payment Due Date` (`sensor.pge_payment_due_date`) – termin płatności.

### Rozwiązywanie problemów
- Jeśli portal wymaga dodatkowej autoryzacji (SMS, e-mail), zaloguj się ręcznie w przeglądarce i zaakceptuj żądanie.
- Brak danych w sensorach zwykle oznacza, że na koncie nie ma zaległości lub format tabel na stronie uległ zmianie.
- Aktywuj logowanie debug w Home Assistant dodając w `configuration.yaml`:
  ```yaml
  logger:
    logs:
      custom_components.pge_sensor: debug
  ```

### Kontrybucje i licencja
Pull requesty, zgłoszenia błędów i usprawnienia są mile widziane. Projekt jest licencjonowany na zasadach MIT (patrz plik `LICENSE`).

### Nota prawna
To projekt prywatny, który nie jest powiązany, sponsorowany ani wspierany przez PGE Polska Grupa Energetyczna S.A. Wszystkie nazwy produktów, znaki towarowe i zastrzeżone znaki towarowe wspomniane w repozytorium należą do ich właścicieli. Służą wyłącznie do celów identyfikacyjnych.

Źródłem danych dla integracji jest https://ebok.gkpge.pl/. Autor jednoznacznie odrzuca odpowiedzialność za interpretację danych prezentowanych przez integrację. Masz pytania? Utwórz zgłoszenie w repozytorium.

---

## 🇬🇧 English section

### Overview
This repository ships both a lightweight CLI scraper (`pge_scraper.py`) and a Home Assistant custom integration located in `custom_components/pge_sensor`. The code signs in to the PGE Sensor customer portal, parses outstanding invoices and exposes:
- console output for quick balance checks,
- Home Assistant sensors with the outstanding amount and optional due date.

### Requirements
- Python 3.10+ with `requests` and `beautifulsoup4` available.
- Valid credentials for https://ebok.gkpge.pl.
- (Optional) Home Assistant instance that allows custom components.

### HACS installation
1. In Home Assistant go to HACS → Integrations and open the ⁝ menu → `Custom repositories`.
2. Add `https://github.com/procaktomasz/PGE_sensor` as a repository of type `Integration` and confirm.
3. Search for “PGE Sensor” in the HACS integrations catalog and install it.
4. Restart Home Assistant if prompted, then add the “PGE Sensor” integration via `Settings → Devices & Services`.

### Home Assistant integration
1. Copy the `custom_components/pge_sensor` directory into `config/custom_components` inside your HA setup.
2. Reload Home Assistant (or use the “Reload integrations” UI action).
3. Add the “PGE Sensor” integration via the UI and supply your login/password.
4. The `DataUpdateCoordinator` refreshes the portal every 12 hours. Available entities:
   - `PGE Balance` (`sensor.pge_balance`) – outstanding amount in PLN.
   - `PGE Payment Due Date` (`sensor.pge_payment_due_date`) – next due date if present.

### Troubleshooting
- Solve any two-factor prompts directly in the official portal before running the scraper.
- Empty sensors typically mean no unpaid invoices or a layout change on the eBOK website.
- Enable debug logging within Home Assistant by adding:
  ```yaml
  logger:
    logs:
      custom_components.pge_sensor: debug
  ```

### Contributing & license
Issues and pull requests are welcome. The project is released under the MIT License (see `LICENSE`).

### Legal notice
This is a personal project and is not affiliated with, sponsored, or endorsed by PGE Polska Grupa Energetyczna S.A. All product names, trademarks, and registered trademarks referenced here belong to their respective owners and are used for identification purposes only.

The data source for this integration is https://ebok.gkpge.pl/. The author disclaims any responsibility for how the presented data is interpreted or used. Anything else? Open an issue.
