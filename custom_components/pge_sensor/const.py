"""Constants for the PGE Sensor integration."""
from __future__ import annotations

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME

DOMAIN = "pge_sensor"
DEFAULT_TIMEOUT = 15

__all__ = ["DOMAIN", "CONF_USERNAME", "CONF_PASSWORD", "DEFAULT_TIMEOUT"]
