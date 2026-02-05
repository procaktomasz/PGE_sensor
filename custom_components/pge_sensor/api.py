"""PGE Sensor scraping helpers."""
from __future__ import annotations

import logging
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup

_LOGGER = logging.getLogger(__name__)


class PgeScraperError(RuntimeError):
    """Domain-specific exception raised by PgeScraper."""


@dataclass
class BalanceInfo:
    """Represents a single outstanding payment entry."""

    amount: float
    due_date: Optional[date] = None
    invoice_number: Optional[str] = None
    issue_date: Optional[date] = None


class PgeScraper:
    """Scrapes outstanding payment data from the PGE Sensor portal."""

    LOGIN_URL = "https://ebok.gkpge.pl/ebok/profil/logowanie.xhtml"
    DASHBOARD_URL = "https://ebok.gkpge.pl/ebok/"
    INDEX_URL = "https://ebok.gkpge.pl/ebok/index.xhtml"
    FINANCE_URL = "https://ebok.gkpge.pl/ebok/finanse.xhtml"
    FINANCE_FALLBACK_URLS = (
        "https://ebok.gkpge.pl/ebok/finanse.xhtml",
        "https://ebok.gkpge.pl/ebok/finanse/finanse.xhtml",
    )
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    )
    _AMOUNT_REGEX = re.compile(
        r"(?:\d{1,3}(?:[\s\xa0]\d{3})*(?:[\.,]\d{2})|\d+[\.,]\d{2})"
    )
    _NO_OUTSTANDING_HINTS = (
        "brak nale\u017cno\u015bci",
        "brak zaleg\u0142o\u015bci",
        "brak dokument\u00f3w do zap\u0142aty",
        "brak faktur do zap\u0142aty",
        "brak rachunk\u00f3w do zap\u0142aty",
        "brak p\u0142atno\u015bci do realizacji",
        "wszystkie p\u0142atno\u015bci zosta\u0142y uregulowane",
        "nie masz \u017cadnych zaleg\u0142o\u015bci",
    )
    _ZERO_BALANCE_REGEX = re.compile(
        r"(saldo|do zap(?:\u0142|l)aty|kwota do zap(?:\u0142|l)aty)[^0-9]{0,80}(0[,\.]00)"
    )

    def __init__(self, username: str, password: str, *, timeout: int = 15) -> None:
        if not username or not password:
            raise ValueError("Username and password must be provided")
        self._username = username
        self._password = password
        self._timeout = timeout
        self._session = requests.Session()
        default_headers = {
            "User-Agent": self.USER_AGENT,
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,*/*;q=0.8"
            ),
            "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        for header, value in default_headers.items():
            self._session.headers.setdefault(header, value)
        self._authenticated = False

    def get_balance_details(self) -> BalanceInfo:
        """Return the highest outstanding payment along with its due date."""
        if not self._authenticated:
            self._login()
        payload = self._fetch_finance_payload()
        balances = self._extract_balance_info(payload)
        if not balances:
            if self._has_no_outstanding_hint(payload):
                _LOGGER.debug("No outstanding payments detected for %s", self._username)
                return BalanceInfo(amount=0.0)
            raise PgeScraperError("Could not find any outstanding payments in response")
        return max(balances, key=lambda item: item.amount)

    # ---------------------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------------------

    def _login(self) -> None:
        view_state = self._fetch_view_state()
        payload = {
            "hiddenLoginForm": "hiddenLoginForm",
            "hiddenLoginForm:hiddenLogin": self._username,
            "hiddenLoginForm:hiddenPassword": self._password,
            "hiddenLoginForm:loginButton": "Zaloguj",
            "javax.faces.ViewState": view_state,
        }
        try:
            response = self._session.post(
                self.LOGIN_URL,
                data=payload,
                headers={"Referer": self.LOGIN_URL},
                timeout=self._timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise PgeScraperError("Login request failed") from exc
        if self._is_login_response(response):
            raise PgeScraperError(
                "Login failed: incorrect credentials or additional verification required"
            )
        if "weryfikacja" in (response.url or "").lower():
            raise PgeScraperError(
                "Portal requires additional verification. Complete it in the browser first."
            )
        self._post_login_warmup()
        self._authenticated = True

    def _fetch_view_state(self) -> str:
        try:
            response = self._session.get(self.LOGIN_URL, timeout=self._timeout)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise PgeScraperError("Unable to load login form") from exc
        soup = BeautifulSoup(response.text, "html.parser")
        view_state = soup.find("input", attrs={"name": "javax.faces.ViewState"})
        if not view_state or not view_state.get("value"):
            raise PgeScraperError("Missing javax.faces.ViewState token on login page")
        return view_state["value"]

    @staticmethod
    def _is_login_response(response: requests.Response) -> bool:
        url = (response.url or "").lower()
        if "logowanie" in url:
            return True
        return "hiddenLoginForm:hiddenLogin" in response.text

    def _post_login_warmup(self) -> None:
        for url in (self.DASHBOARD_URL, self.INDEX_URL):
            try:
                resp = self._session.get(url, timeout=self._timeout)
                _LOGGER.debug("Warmup GET %s -> %s", url, resp.status_code)
            except requests.RequestException as exc:
                _LOGGER.debug("Warmup GET %s failed: %s", url, exc)

    def _fetch_finance_payload(self) -> str:
        errors: list[str] = []
        headers = {"Referer": self.INDEX_URL}
        for url in self.FINANCE_FALLBACK_URLS:
            try:
                response = self._session.get(url, timeout=self._timeout, headers=headers)
                response.raise_for_status()
                if url != self.FINANCE_URL:
                    _LOGGER.debug("Using fallback finance endpoint %s", url)
                return response.text
            except requests.HTTPError as exc:
                status = exc.response.status_code if exc.response else "?"
                snippet = exc.response.text[:160].strip() if exc.response else ""
                errors.append(f"{url} -> {status}: {snippet}")
            except requests.RequestException as exc:
                errors.append(f"{url} -> network error: {exc}")
        raise PgeScraperError(
            "Unable to retrieve finance data: " + "; ".join(errors)
        )

    # ------------------------------------------------------------------
    # Parsing helpers
    # ------------------------------------------------------------------

    @classmethod
    def _extract_balance_info(cls, raw_payload: str) -> list[BalanceInfo]:
        snapshot = raw_payload.lstrip()
        balances: list[BalanceInfo] = []
        if snapshot.startswith("<?xml") or "<partial-response" in snapshot[:200]:
            try:
                balances.extend(cls._extract_from_partial(snapshot))
            except PgeScraperError as err:
                _LOGGER.debug(
                    "Partial-response parsing failed, falling back to HTML: %s", err
                )
        if not balances:
            balances.extend(cls._extract_from_html(raw_payload))
        return balances

    @classmethod
    def _has_no_outstanding_hint(cls, raw_payload: str) -> bool:
        simplified = raw_payload.lower()
        if any(marker in simplified for marker in cls._NO_OUTSTANDING_HINTS):
            return True
        if "0,00" not in simplified and "0.00" not in simplified:
            return False
        return bool(cls._ZERO_BALANCE_REGEX.search(simplified))

    @classmethod
    def _extract_from_partial(cls, partial_xml: str) -> list[BalanceInfo]:
        try:
            root = ET.fromstring(partial_xml)
        except ET.ParseError as exc:
            raise PgeScraperError("Finance response is not valid XML") from exc
        balances: list[BalanceInfo] = []
        for update_node in root.findall(".//update"):
            html_fragment = update_node.text or ""
            balances.extend(cls._extract_from_html(html_fragment))
        return balances

    @classmethod
    def _extract_from_html(cls, html_payload: str) -> list[BalanceInfo]:
        soup = BeautifulSoup(html_payload, "html.parser")
        balances = cls._extract_from_invoice_tables(soup)
        if not balances:
            for label in soup.select(
                '[id*="amountToPay" i], .amount-to-pay, .do-zaplaty-label'
            ):
                amount = cls._extract_amount_from_text(label.get_text(" ", strip=True))
                if amount is not None:
                    balances.append(BalanceInfo(amount=amount))
        return balances

    @classmethod
    def _extract_from_invoice_tables(cls, soup: BeautifulSoup) -> list[BalanceInfo]:
        balances: list[BalanceInfo] = []
        tables = []
        for thead in soup.select("thead[id*='fakturaDoZaplaty']"):
            table = thead.find_parent("table")
            if table:
                tables.append(table)
        if not tables:
            tables = [
                table
                for table in soup.find_all("table")
                if table.find("thead")
                and "Termin" in table.find("thead").get_text(" ", strip=True)
            ]
        for table in tables:
            header = table.find("thead")
            if header and "Termin" not in header.get_text(" ", strip=True):
                continue
            for row in table.select("tbody tr"):
                cells = row.find_all("td")
                if len(cells) < 4:
                    continue
                invoice_number = cells[0].get_text(" ", strip=True) or None
                issue_date = cls._parse_date(cells[1].get_text(" ", strip=True))
                due_date = cls._parse_date(cells[2].get_text(" ", strip=True))
                amount = cls._extract_amount_from_text(
                    cells[3].get_text(" ", strip=True)
                )
                if amount is None:
                    continue
                balances.append(
                    BalanceInfo(
                        amount=amount,
                        due_date=due_date,
                        invoice_number=invoice_number,
                        issue_date=issue_date,
                    )
                )
        return balances

    @staticmethod
    def _parse_date(value: str) -> Optional[date]:
        if not value:
            return None
        try:
            return datetime.strptime(value.strip(), "%d.%m.%Y").date()
        except ValueError:
            return None

    @classmethod
    def _extract_amount_from_text(cls, text: str) -> Optional[float]:
        if not text:
            return None
        cleaned_text = text.replace("PLN", "").replace("zł", "")
        matches = cls._AMOUNT_REGEX.findall(cleaned_text)
        if not matches:
            return None
        numeric = matches[-1]
        cleaned = (
            numeric.replace("\xa0", "")
            .replace(" ", "")
            .replace(",", ".")
        )
        try:
            return float(cleaned)
        except ValueError:
            return None
