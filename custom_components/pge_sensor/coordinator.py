"""DataUpdateCoordinator for the PGE Sensor integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import BalanceInfo, PgeScraper, PgeScraperError
from .const import DEFAULT_TIMEOUT

SCAN_INTERVAL = timedelta(hours=12)
_LOGGER = logging.getLogger(__name__)


class PgeEbokCoordinator(DataUpdateCoordinator[BalanceInfo]):
    """Coordinator responsible for fetching balance information."""

    def __init__(self, hass: HomeAssistant, username: str, password: str) -> None:
        self._api = PgeScraper(username, password, timeout=DEFAULT_TIMEOUT)
        self._username = username
        super().__init__(
            hass,
            _LOGGER,
            name=f"PGE Sensor ({username})",
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> BalanceInfo:
        try:
            return await self.hass.async_add_executor_job(self._api.get_balance_details)
        except PgeScraperError as err:
            raise UpdateFailed(str(err)) from err

    @property
    def username(self) -> str:
        return self._username
