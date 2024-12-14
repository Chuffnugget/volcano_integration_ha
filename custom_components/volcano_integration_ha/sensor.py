from homeassistant.components.sensor import SensorEntity
from .coordinator import GATTDeviceCoordinator

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Volcano Hybrid sensor entities."""
    address = hass.data["volcano_integration_ha"][config_entry.entry_id]["address"]

    coordinator = GATTDeviceCoordinator(hass, address, update_interval=0.5)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([
        GATTTemperatureSensor(coordinator),
        GATTSerialNumber(coordinator),
        GATTBLEFirmwareVersion(coordinator),
        GATTHoursOfOperation(coordinator),
        GATTMinutesOfOperation(coordinator),
    ])


class GATTTemperatureSensor(SensorEntity):
    """Entity to monitor the current temperature."""

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Volcano Temperature"

    @property
    def native_value(self):
        return self.coordinator.data.get("Temperature Read")


class GATTSerialNumber(SensorEntity):
    """Entity to show the serial number."""

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Volcano Serial Number"

    @property
    def native_value(self):
        return self.coordinator.data.get("Serial Number")


class GATTBLEFirmwareVersion(SensorEntity):
    """Entity to show the BLE firmware version."""

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "BLE Firmware Version"

    @property
    def native_value(self):
        return self.coordinator.data.get("BLE Firmware Version")


class GATTHoursOfOperation(SensorEntity):
    """Entity to monitor the hours of operation."""

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Hours of Operation"

    @property
    def native_value(self):
        return self.coordinator.data.get("Hours of Operation")


class GATTMinutesOfOperation(SensorEntity):
    """Entity to monitor the minutes of operation."""

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Minutes of Operation"

    @property
    def native_value(self):
        return self.coordinator.data.get("Minutes of Operation")
