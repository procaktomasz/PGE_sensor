"""DataUpdateCoordinator for the PGE Sensor integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import BalanceInfo, PgeScraper, PgeScraperError
from .const import DEFAULT_TIMEOUT

SCAN_INTERVAL = timedelta(hours=8)
RETRY_INTERVAL = timedelta(minutes=30)
_LOGGER = logging.getLogger(__name__)


class PgeEbokCoordinator(DataUpdateCoordinator[BalanceInfo]):
    """Coordinator responsible for fetching balance information."""

    def __init__(self, hass: HomeAssistant, username: str, password: str) -> None:
        self._api = PgeScraper(username, password, timeout=DEFAULT_TIMEOUT)
        self._username = username
        super().__init__(
            hass,
            _LOGGER,
                self._ensure_interval(SCAN_INTERVAL)

    async def _async_update_data(self) -> BalanceInfo:
                self._ensure_interval(RETRY_INTERVAL)
                raise UpdateFailed(str(err)) from err
            except Exception as err:  # pragma: no cover - defensive guard
                self._ensure_interval(RETRY_INTERVAL)
                raise UpdateFailed(f"Unexpected coordinator error: {err}") from err
            return data
        except PgeScraperError as err:
            # Tighten the retry window after a failure so we do not wait the full interval.
            if self.update_interval != RETRY_INTERVAL:

        def _ensure_interval(self, interval: timedelta) -> None:
            if self.update_interval != interval:
                self.update_interval = interval
                self.update_interval = RETRY_INTERVAL
            raise UpdateFailed(str(err)) from err

    @property
    def username(self) -> str:
        return self._username
