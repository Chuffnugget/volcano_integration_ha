from homeassistant.components.sensor import SensorEntity
from .coordinator import VolcanoCoordinator

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Volcano Hybrid sensors."""
    coordinator = hass.data["volcano_integration_ha"][config_entry.entry_id]

    async_add_entities([
        VolcanoTemperatureSensor(coordinator),
    ])


class VolcanoTemperatureSensor(SensorEntity):
    """Sensor for monitoring the Volcano's temperature."""

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Volcano Temperature"

    @property
    def native_value(self):
        return self.coordinator.data.get("temperature")
