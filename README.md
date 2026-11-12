# PGE Sensor

Integracja Home Assistant oraz skrypt CLI do pobierania informacji o rozliczeniach i rachunkach z portalu PGE (eBOK).

## Funkcje

- **Integracja Home Assistant** - automatyczne tworzenie sensorów dla stanu konta, terminów płatności oraz parametrów zużycia energii.
- **Wielu punktów poboru** - obsługa wielu PPE na jednym koncie (każdy punkt tworzy osobne urządzenie w HA).
- **Szczegółowe dane** - m.in. energia pobrana, wprowadzona, zbilansowana, magazyn energii, okres rozliczeniowy.
- **Skrypt CLI** - opcjonalny skrypt `pge_scraper.py` dla szybkiej kontroli salda z poziomu konsoli.

## Wymagania

- Aktywne konto w serwisie https://ebok.gkpge.pl.
- Instancja Home Assistant (dla integracji) lub Python 3.10+ (dla skryptu CLI).

## Sensory

Integracja tworzy następujące sensory dla każdego skonfigurowanego konta rozliczeniowego.
Przy jednym koncie identyfikatory mają postać `sensor.pge_<sufiks>`, a przy kilku kontach `sensor.pge_<numer_konta>_<sufiks>`.
Identyfikatory istniejących encji nie są zmieniane podczas aktualizacji.

| Sufiks ID | Nazwa | Opis | Wartość |
|-----------|-------|------|---------|
| `saldo` | PGE Saldo | Kwota pozostała do zapłaty. W atrybutach m.in. data i status płatności, numer faktury. | PLN |
| `termin_platnosci` | PGE Termin płatności | Data, do której należy opłacić rachunek. | data |
| `kwota_faktury` | PGE Kwota ostatniego dokumentu płatności | Kwota najnowszego dokumentu płatności (faktury lub prognozy). | PLN |
| `biezaca_platnosc` | PGE Bieżąca płatność | Kwota do zapłaty wyłącznie za najnowszy dokument. | PLN |
| `actual_invoice_amount` | PGE Kwota rzeczywistej faktury rozliczeniowej | Kwota najnowszej faktury rzeczywistej (nie prognozy). | PLN |
| `energia_pobrana` | PGE Pobór w ostatnim rzeczywistym rozliczeniu | Energia pobrana z sieci w okresie ostatniej faktury rzeczywistej. | kWh |
| `energia_wprowadzona` | PGE Oddanie w ostatnim rzeczywistym rozliczeniu | Energia wprowadzona do sieci (prosumenci). | kWh |
| `forecast_energy` | PGE Prognozowany pobór — dokument płatności | Pobór przyjęty w fakturze prognozowanej. | kWh |
| `settlement_value_pln` | PGE Wartość rozliczenia energii (PLN) | Wartość energii z rzeczywistego rozliczenia (nie końcowa kwota faktury). | PLN |
| `magazyn_energii` | PGE Bank po opuście — ostatnie rozliczenie | Energia do odebrania z banku (suma S1/S2 po opuście), historia w atrybutach. | kWh |
| `energy_storage_1` / `energy_storage_2` | PGE Bank S1 / S2 po opuście | Saldo banku w strefie S1 / S2 po zastosowaniu współczynnika PGE. | kWh |
| `bank_date` | PGE Data potwierdzonego salda banku | Data, na którą obowiązuje saldo banku (koniec okresu faktury). | data |
| `okres_rozliczeniowy` | PGE Okres rozliczeniowy | Przedział dat ostatniej faktury rzeczywistej. | tekst |

Dane energii i banku pochodzą z faktur, więc opisują ostatni rozliczony okres, a nie bieżący stan licznika. Nie należy ich używać jako źródła w panelu Energia.
Szczegóły: [docs/settlement-sensors.md](docs/settlement-sensors.md).

Sensor „Zużycie po rozliczeniu” został wycofany w wersji 1.6.0 (pokazywał wartość w PLN jako kWh) i jest automatycznie wyłączany. Jego historia jest zachowana.

Koordynator aktualizuje dane co 8 godzin, a w przypadku błędu (np. przerwa techniczna eBOK) ponawia próby co 30 minut.

## Instalacja

### Opcja 1: HACS (Zalecana)

Kliknij poniższy przycisk, aby automatycznie dodać repozytorium do HACS:

[![Otwórz w HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=procaktomasz&repository=PGE_sensor&category=integration)

Lub ręcznie:

1. Otwórz HACS w Home Assistant.
2. Kliknij trzy kropki w prawym górnym rogu.
3. Wybierz **Custom repositories**.
4. W polu URL wpisz: `https://github.com/procaktomasz/PGE_sensor`
5. W polu Category wybierz: **Integration**.
6. Kliknij Add, a następnie wyszukaj "PGE Sensor" i zainstaluj komponent.
7. Zrestartuj Home Assistant.

### Opcja 2: Instalacja manualna

1. Skopiuj folder `custom_components/pge_sensor` do folderu `config/custom_components/` w konfiguracji HA.
2. Zrestartuj Home Assistant.

## Konfiguracja

1. Przejdź do: **Konfiguracja** > **Urządzenia i Usługi** > **Dodaj integrację**.
2. Wyszukaj **PGE Sensor**.
3. Podaj swoje dane logowania do serwisu eBOK.
4. Jeśli konto posiada wiele kont rozliczeniowych, instalator wyświetli je z adresem punktu poboru, numerem PPE i oznaczeniami (domyślne, prosument, ARCHIWALNE) i zapyta, czy dodać wszystkie naraz, czy tylko wybrane. Aby w przyszłości dodać kolejne, uruchom konfigurację ponownie z tymi samymi danymi.

## Rozwiązywanie problemów

- Jeśli logowanie kończy się błędem, sprawdź czy portal eBOK nie wymaga autoryzacji SMS/e-mail (zaloguj się ręcznie w przeglądarce i zaakceptuj żądanie).
- Zmiany na stronie eBOK mogą powodować tymczasowy brak danych w sensorach. 
- Aby włączyć logowanie dla integracji, dodaj w `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.pge_sensor: debug
```

## Nota prawna

Projekt licencjonowany na zasadach MIT. Jest to projekt prywatny, niepowiązany, niesponsorowany ani niewspierany przez PGE Polska Grupa Energetyczna S.A. Nazwy i znaki towarowe należą do ich właścicieli i służą wyłącznie do celów identyfikacyjnych.
Źródłem danych dla integracji jest https://ebok.gkpge.pl/.
