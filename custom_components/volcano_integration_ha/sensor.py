import logging
from homeassistant.components.sensor import SensorEntity
from .coordinator import GATTDeviceCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Volcano Hybrid sensor entities."""
    address = hass.data["volcano_integration_ha"][config_entry.entry_id]["address"]

    coordinator = GATTDeviceCoordinator(hass, address, update_interval=0.5)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([
        GATTConnectionStatus(coordinator),
        GATTSerialNumber(coordinator),
        GATTTemperatureSensor(coordinator),
    ])


class GATTConnectionStatus(SensorEntity):
    """Entity to track Bluetooth connection status."""

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Volcano Connection Status"

    @property
    def native_value(self):
        return "Connected" if self.coordinator.connected else "Disconnected"


class GATTSerialNumber(SensorEntity):
    """Entity to show the serial number."""

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Volcano Serial Number"

    @property
    def native_value(self):
        return self.coordinator.data.get("serial_number")


class GATTTemperatureSensor(SensorEntity):
    """Entity to monitor the current temperature."""

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Volcano Current Temperature"

    @property
    def native_value(self):
        return self.coordinator.data.get("temperature")
