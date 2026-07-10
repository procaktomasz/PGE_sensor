"""Utility for retrieving outstanding payments from PGE Sensor (mobile API)."""
from __future__ import annotations

import argparse
import logging
import sys
import os
import importlib.util

# Bezpośrednie załadowanie pliku api.py za pomocą importlib.
api_path = os.path.join(os.path.dirname(__file__), "custom_components", "pge_sensor", "api.py")
spec = importlib.util.spec_from_file_location("pge_sensor_api", api_path)
pge_sensor_api = importlib.util.module_from_spec(spec)
sys.modules["pge_sensor_api"] = pge_sensor_api
spec.loader.exec_module(pge_sensor_api)

PgeScraper = pge_sensor_api.PgeScraper
PgeScraperError = pge_sensor_api.PgeScraperError

_LOGGER = logging.getLogger(__name__)

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch outstanding balance from PGE mobile API")
    parser.add_argument("username", help="Login (email) used on ekob/mobile portal")
    parser.add_argument("password", help="Password used on ekob/mobile portal")
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="Request timeout in seconds (default: 15)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable verbose debug logging",
    )
    return parser.parse_args()

def main() -> int:
    args = _parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )
    scraper = PgeScraper(args.username, args.password, timeout=args.timeout)
    try:
        balance = scraper.get_balance_details()
    except PgeScraperError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    if balance.due_date:
        due_text = balance.due_date.strftime("%d.%m.%Y")
        print(f"Outstanding amount: {balance.amount:.2f} PLN (due {due_text})")
    else:
        print(f"Outstanding amount: {balance.amount:.2f} PLN (due date unavailable)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
