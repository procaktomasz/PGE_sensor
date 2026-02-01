"""Sensor platform for the PGE Sensor integration."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import DOMAIN
from .coordinator import PgeEbokCoordinator

MONETARY_UNIT = "PLN"


@dataclass
class PgeSensorDescription:
    name: str
    key: str


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: PgeEbokCoordinator = hass.data[DOMAIN][entry.entry_id]
    username = entry.data[CONF_USERNAME]
    slug = slugify(username)

    entities: list[SensorEntity] = [
        PgeBalanceSensor(coordinator, slug, username),
    ]

    if coordinator.data and coordinator.data.due_date:
        entities.append(PgeDueDateSensor(coordinator, slug, username))

    async_add_entities(entities)


class PgeBaseSensor(CoordinatorEntity[PgeEbokCoordinator], SensorEntity):
    def __init__(self, coordinator: PgeEbokCoordinator, slug: str, username: str) -> None:
        super().__init__(coordinator)
        self._slug = slug
        self._username = username

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._slug)},
            name="PGE Sensor",
            manufacturer="PGE",
        )

    @property
    def available(self) -> bool:
        if self._attr_available is False:
            return False
        return self.coordinator.data is not None


class PgeBalanceSensor(PgeBaseSensor):
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = MONETARY_UNIT
    _attr_name = "PGE Balance"

    @property
    def unique_id(self) -> str:
        return f"{self._slug}_balance"

    @property
    def native_value(self) -> float | None:
        if self.coordinator.data:
            return round(self.coordinator.data.amount, 2)
        return None

    @property
    def extra_state_attributes(self) -> dict[str, str] | None:
        if not self.coordinator.data:
            return None
        attributes = {}
        if self.coordinator.data.invoice_number:
            attributes["invoice_number"] = self.coordinator.data.invoice_number
        if self.coordinator.data.issue_date:
            attributes["issue_date"] = self.coordinator.data.issue_date.isoformat()
        return attributes or None


class PgeDueDateSensor(PgeBaseSensor):
    _attr_device_class = SensorDeviceClass.DATE
    _attr_name = "PGE Payment Due Date"

    @property
    def unique_id(self) -> str:
        return f"{self._slug}_due_date"

    @property
    def native_value(self) -> date | None:
        if self.coordinator.data:
            return self.coordinator.data.due_date
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        if self.coordinator.data and self.coordinator.data.due_date is None:
            self._attr_available = False
        else:
            self._attr_available = True
        super()._handle_coordinator_update()
