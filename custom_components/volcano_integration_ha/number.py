from homeassistant.components.number import NumberEntity
from .coordinator import GATTDeviceCoordinator

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Volcano Hybrid number entities."""
    address = hass.data["volcano_integration_ha"][config_entry.entry_id]["address"]

    coordinator = GATTDeviceCoordinator(hass, address, update_interval=0.5)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([
        GATTTargetTemperature(coordinator),
        GATTAutoShutoffSetting(coordinator),
    ])


class GATTTargetTemperature(NumberEntity):
    """Entity to set the target temperature."""

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Set Target Temperature"
        self._attr_min_value = 40
        self._attr_max_value = 230
        self._attr_step = 1

    @property
    def native_value(self):
        return self.coordinator.data.get("Temperature Read")

    async def async_set_native_value(self, value):
        await self.coordinator.client.write_gatt_char("10110003-5354-4f52-5a26-4249434b454c", int(value).to_bytes(2, "little"))


class GATTAutoShutoffSetting(NumberEntity):
    """Entity to set the auto shutoff setting."""

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Set Auto Shutoff (Minutes)"
        self._attr_min_value = 1
        self._attr_max_value = 120
        self._attr_step = 1

    @property
    def native_value(self):
        return self.coordinator.data.get("Auto Shutoff Setting")

    async def async_set_native_value(self, value):
        await self.coordinator.client.write_gatt_char("1011000d-5354-4f52-5a26-4249434b454c", int(value * 60).to_bytes(2, "little"))
