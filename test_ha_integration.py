import sys
import asyncio
import os
import importlib.util

# Bezpośrednie załadowanie pliku api.py za pomocą importlib.
# Zapobiega to wykonaniu pliku __init__.py w custom_components/pge_sensor/,
# który wymagałby całego środowiska Home Assistant.
api_path = os.path.join(os.path.dirname(__file__), "custom_components", "pge_sensor", "api.py")
spec = importlib.util.spec_from_file_location("pge_sensor_api", api_path)
pge_sensor_api = importlib.util.module_from_spec(spec)
sys.modules["pge_sensor_api"] = pge_sensor_api
spec.loader.exec_module(pge_sensor_api)

PgeScraper = pge_sensor_api.PgeScraper
PgeScraperError = pge_sensor_api.PgeScraperError

async def test_integration(username, password):
    print(f"Rozpoczynam test modułu API dla użytkownika: {username}")
    
    # Bezpośrednie uruchomienie serca komponentu - klasy PgeScraper
    # Dzięki temu omijamy zależność od zewnętrznego modułu 'homeassistant'
    scraper = PgeScraper(username, password, timeout=15)
    print("Zainicjalizowano rdzeń komunikacyjny PgeScraper.")
    
    try:
        print("Trwa próba logowania i pobierania danych (może to zająć chwilę)...")
        # W środowisku asynchronicznym (jak HA) używane byłoby asyncio.to_thread / run_in_executor
        # Tutaj wywołamy to bezpośrednio w sposób blokujący na potrzeby testu.
        data = scraper.get_balance_details()
        
        print("\n=== SUKCES ===")
        print("Logowanie przebiegło pomyślnie, a komponent przetworzył dane:")
        print(f" Kwota do zapłaty: {data.amount:.2f} PLN")
        if data.due_date:
            print(f" Termin płatności: {data.due_date.strftime('%d.%m.%Y')}")
        else:
            print(" Termin płatności: (brak / nie dotyczy)")
            
        if data.invoice_number:
            print(f" Numer faktury:    {data.invoice_number}")
            
        print("\nTest przepływu komponentu zakończony pomyślnie!")
        
    except PgeScraperError as err:
        print("\n=== BŁĄD LOGOWANIA / SCRAPOWANIA ===")
        print(f"Wystąpił problem związany z kontem lub portalem eBOK: {err}")
    except Exception as err:
        print("\n=== NIEOCZEKIWANY BŁĄD ===")
        print(f"Napotkano niespodziewany wyjątek: {err}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("BŁĄD: Złe użycie skryptu.")
        print("Poprawne wywołanie: python test_ha_integration.py <użytkownik_pge> <hasło_pge>")
        sys.exit(1)
        
    test_user = sys.argv[1]
    test_pass = sys.argv[2]
    
    # Uruchomienie testu asynchronicznego
    asyncio.run(test_integration(test_user, test_pass))
