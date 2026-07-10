"""PGE Sensor API using mobile endpoints (mBOK PGE)."""
from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

import requests

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
    """Retrieves outstanding payment data from the mBOK PGE mobile API."""

    AUTH_URL = "https://mbok-services.gkpge.pl/authorization-service/api/auth/login"
    BILLING_ACCOUNTS_URL = "https://mbok-services.gkpge.pl/billing-service-v1/billingAccounts/filter"
    
    def __init__(self, username: str, password: str, *, timeout: int = 15) -> None:
        if not username or not password:
            raise ValueError("Username and password must be provided")
        self._username = username
        self._password = password
        self._timeout = timeout
        self._session = requests.Session()
        # Mocking an Android app request
        self._session.headers.update({
            "User-Agent": "okhttp/4.9.2",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        self._access_token: Optional[str] = None
        self._device_id = str(uuid.uuid4())

    def get_balance_details(self) -> BalanceInfo:
        """Return the outstanding payment along with its due date."""
        if not self._access_token:
            self._login()

        # Update headers with auth token
        self._session.headers.update({"Authorization": f"Bearer {self._access_token}"})

        account_id = self._get_billing_account_id()
        if not account_id:
            _LOGGER.warning("No billing accounts found for user %s", self._username)
            return BalanceInfo(amount=0.0)

        balance_data = self._get_balance(account_id)
        # Often totalAmount or requiredAmount stores the due value
        amount = balance_data.get("totalAmount", 0.0)

        # Get latest document/invoice to find due date
        documents = self._get_documents(account_id)
        
        # Filter for documents that actually need to be paid
        unpaid_docs = [
            doc for doc in documents 
            if doc.get("amountToPay", 0.0) > 0 or doc.get("paymentStatus") != "PAID"
        ]

        if not unpaid_docs:
            return BalanceInfo(amount=amount)

        # Sort by due date (closest first)
        def parse_date(date_str: str) -> datetime:
            try:
                # Format is usually "2026-02-24 00:00:00.000"
                return datetime.strptime(date_str.split(".")[0], "%Y-%m-%d %H:%M:%S")
            except Exception:
                return datetime.max

        unpaid_docs.sort(key=lambda d: parse_date(d.get("paymentDueDate", "9999-12-31 00:00:00")))
        
        target_doc = unpaid_docs[0]
        due_date = None
        if target_doc.get("paymentDueDate"):
            due_date = parse_date(target_doc["paymentDueDate"]).date()
            
        issue_date = None
        if target_doc.get("creationDate"):
            issue_date = parse_date(target_doc["creationDate"]).date()

        return BalanceInfo(
            amount=amount,
            due_date=due_date,
            invoice_number=target_doc.get("documentNumber"),
            issue_date=issue_date
        )

    def _login(self) -> None:
        payload = {
            "email": self._username,
            "password": self._password,
            "deviceId": self._device_id,
            "deviceName": "Home Assistant",
            "platform": "Android"
        }
        try:
            response = self._session.post(
                self.AUTH_URL,
                json=payload,
                timeout=self._timeout,
            )
            response.raise_for_status()
            data = response.json()
            if "accessToken" not in data:
                raise PgeScraperError("Login response missing accessToken")
            self._access_token = data["accessToken"]
        except requests.RequestException as exc:
            _LOGGER.debug("Login failed: %s", exc)
            if exc.response is not None and exc.response.status_code in (401, 403):
                raise PgeScraperError("Login failed: incorrect credentials") from exc
            raise PgeScraperError("Login request failed") from exc

    def _get_billing_account_id(self) -> Optional[int]:
        try:
            # First try to get the default account
            response = self._session.post(
                self.BILLING_ACCOUNTS_URL,
                json={"defaultAccount": True},
                timeout=self._timeout
            )
            response.raise_for_status()
            accounts = response.json().get("billingAccounts", [])
            
            if not accounts:
                # Fallback to any account if default is not set
                response = self._session.post(
                    self.BILLING_ACCOUNTS_URL,
                    json={},
                    timeout=self._timeout
                )
                response.raise_for_status()
                accounts = response.json().get("billingAccounts", [])

            if accounts:
                return accounts[0].get("id")
        except requests.RequestException as exc:
            raise PgeScraperError("Failed to fetch billing accounts") from exc
            
        return None

    def _get_balance(self, account_id: int) -> dict:
        url = f"https://mbok-services.gkpge.pl/billing-service-v1/billingAccounts/{account_id}/balance"
        try:
            response = self._session.get(url, timeout=self._timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            raise PgeScraperError(f"Failed to fetch balance for account {account_id}") from exc

    def _get_documents(self, account_id: int) -> list[dict]:
        url = f"https://mbok-services.gkpge.pl/mbok-service-v1/billingAccounts/{account_id}/documents/filter?pageNo=0&pageSize=15"
        try:
            response = self._session.post(url, json={}, timeout=self._timeout)
            response.raise_for_status()
            return response.json().get("documents", [])
        except requests.RequestException as exc:
            _LOGGER.warning("Failed to fetch documents: %s", exc)
            return []
