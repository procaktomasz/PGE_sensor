"""Config flow for the PGE Sensor integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .api import PgeScraper, PgeScraperError
from .const import DOMAIN


async def _async_validate_credentials(hass: HomeAssistant, data: dict[str, str]) -> None:
    def _validate() -> None:
        scraper = PgeScraper(data[CONF_USERNAME], data[CONF_PASSWORD])
        scraper.get_balance_details()

    await hass.async_add_executor_job(_validate)


class PgeEbokConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for PGE Sensor."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, str] | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_USERNAME].lower())
            self._abort_if_unique_id_configured()
            try:
                await _async_validate_credentials(self.hass, user_input)
            except PgeScraperError:
                errors["base"] = "invalid_auth"
            except Exception:
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=user_input[CONF_USERNAME], data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
