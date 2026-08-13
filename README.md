# PGE Sensor

## 🇵🇱 Wersja polska

### Opis
Ten projekt łączy prosty skrypt CLI oraz integrację Home Assistant do pobierania informacji o zaległościach z portalu PGE Sensor. Dane są scrapowane bezpośrednio z panelu klienta i prezentowane jako:
- komunikat w konsoli (`pge_scraper.py`) dla szybkiej kontroli salda oraz szczegółów ostatniej faktury,
- sensory w Home Assistant (stan konta, termin płatności, kwota faktury oraz parametry zużycia energii w kWh) poprzez komponent `custom_components/pge_sensor`.

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
3. Dodaj integrację „PGE Sensor” z poziomu interfejsu (Konfiguracja → Urządzenia i Usługi → Dodaj integrację) i podaj dane logowania. Jeśli konto obsługuje więcej niż jeden punkt poboru (PPE), zostaniesz zapytany, czy dodać wszystkie punkty naraz, czy tylko wybrany — każdy punkt tworzy osobne urządzenie z pełnym kompletem sensorów. Aby dodać kolejny, pojedynczy punkt później, uruchom dodawanie integracji ponownie z tymi samymi danymi logowania.
4. Koordynator aktualizuje dane co 8 godzin (`SCAN_INTERVAL`), a po błędach przechodzi na 30-minutowe próby. Sensory (dla każdego skonfigurowanego punktu poboru):
   - `PGE Saldo` (`sensor.pge_balance`) – Kwota pozostała do zapłaty w PLN. Posiada dodatkowe atrybuty: Punkt Poboru Medium (PPE), Data opłacenia (Paid Date), Status płatności (Payment Status), Numer faktury (Invoice Number) oraz Data wystawienia (Issue Date).
   - `PGE Termin płatności` (`sensor.pge_payment_due_date`) – Termin płatności rachunku.
   - `PGE Kwota faktury` (`sensor.pge_invoice_amount`) – Oryginalna, całkowita kwota na jaką opiewała najnowsza faktura (przed jakimikolwiek wpłatami).
   - `PGE Energia pobrana` (`sensor.pge_consumed_energy`) – Energia pobrana (w kWh). Sumaryczna ilość prądu, która popłynęła z sieci do Twojego domu.
   - `PGE Energia wprowadzona` (`sensor.pge_feed_in_energy`) – Energia wprowadzona (w kWh). Nadwyżka energii wyprodukowana przez Twoją instalację i wprowadzona do sieci.
   - `PGE Zużycie po rozliczeniu` (`sensor.pge_settled_energy`) – Wartość zużycia po rozliczeniu (w kWh). Faktyczna ilość energii, za którą finalnie PGE wystawiło Ci rachunek po "zbilansowaniu" energii pobranej i wprowadzonej do sieci.
   - `PGE Magazyn energii` (`sensor.pge_magazyn_energii`) – Ilość pozostałej do rozliczenia energii. Atrybuty sensora zawierają ponadto pełną historię rozliczonych miesięcy oraz odpowiednie współczynniki.
   - `PGE Okres rozliczeniowy` (`sensor.pge_okres_rozliczeniowy`) – Przedział dat (np. 01.01.2026 - 30.06.2026), za który została wystawiona najnowsza faktura.
   - `PGE Bieżąca płatność` (`sensor.pge_biezaca_platnosc`) – Kwota (w PLN) pozostała do zapłaty wyłącznie za najnowszą, konkretną fakturę (w przeciwieństwie do salda, które obejmuje całe konto).

### Rozwiązywanie problemów
- Jeśli portal wymaga dodatkowej autoryzacji (SMS, e-mail), zaloguj się ręcznie w przeglądarce i zaakceptuj żądanie.
- Brak danych w sensorach zwykle oznacza, że format tabel na stronie uległ zmianie; przy zerowym saldzie sensor `PGE Balance` prezentuje `0` PLN, a data płatności będzie niedostępna.
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
- console output for quick balance checks and latest invoice details,
- Home Assistant sensors with the outstanding amount, due date, invoice amount, and energy consumption metrics (kWh).

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
3. Add the “PGE Sensor” integration via the UI and supply your login/password. If the account has more than one point of consumption (PPE), you'll be asked whether to add all of them at once or just a specific one — each point becomes its own device with a full set of sensors. To add another single point later, run "Add integration" again with the same credentials.
4. The `DataUpdateCoordinator` refreshes the portal every 8 hours and switches to 30-minute retries after failures. Available entities (per configured point of consumption):
   - `PGE Balance` (`sensor.pge_balance`) – Outstanding amount to pay in PLN. Contains extra attributes: PPE, Paid Date, Payment Status, Invoice Number, and Issue Date.
   - `PGE Payment Due Date` (`sensor.pge_payment_due_date`) – Next payment due date if present.
   - `PGE Invoice Amount` (`sensor.pge_invoice_amount`) – The original total amount of the latest invoice.
   - `PGE Consumed Energy` (`sensor.pge_consumed_energy`) – Consumed energy (in kWh). The amount of electricity drawn from the grid.
   - `PGE Feed-in Energy` (`sensor.pge_feed_in_energy`) – Feed-in energy (in kWh). Energy produced by your installation and fed back into the grid.
   - `PGE Settled Energy` (`sensor.pge_settled_energy`) – Settled energy (in kWh). The final amount of energy you were billed for after settling consumed vs feed-in energy.
   - `PGE Magazyn energii` (`sensor.pge_energy_storage`) – Energy Storage balance (in kWh) representing remaining energy. Attributes contain detailed monthly history and settlement factors.
   - `PGE Okres rozliczeniowy` (`sensor.pge_billing_period`) – Date range (e.g. 01.01.2026 - 30.06.2026) for which the latest invoice was issued.
   - `PGE Bieżąca płatność` (`sensor.pge_current_payment`) – The remaining amount (in PLN) to be paid specifically for the latest invoice (as opposed to the overall account balance).

### Troubleshooting
- Solve any two-factor prompts directly in the official portal before running the scraper.
- Empty sensors typically indicate that the eBOK layout changed; when your balance is zero the `PGE Balance` sensor reports `0` PLN and no due date is exposed.
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
