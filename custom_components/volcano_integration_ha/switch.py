from homeassistant.components.switch import SwitchEntity
from .coordinator import GATTDeviceCoordinator

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Volcano Hybrid switch entities."""
    address = hass.data["volcano_integration_ha"][config_entry.entry_id]["address"]

    coordinator = GATTDeviceCoordinator(hass, address, update_interval=0.5)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([
        GATTFanSwitch(coordinator),
        GATTHeatSwitch(coordinator),
    ])


class GATTFanSwitch(SwitchEntity):
    """Entity to control the fan."""

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Volcano Fan"

    @property
    def is_on(self):
        return self.coordinator.data.get("Fan On")

    async def async_turn_on(self):
        await self.coordinator.client.write_gatt_char("10110013-5354-4f52-5a26-4249434b454c", bytearray([0x01]))

    async def async_turn_off(self):
        await self.coordinator.client.write_gatt_char("10110014-5354-4f52-5a26-4249434b454c", bytearray([0x00]))


class GATTHeatSwitch(SwitchEntity):
    """Entity to control the heat."""

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Volcano Heat"

    @property
    def is_on(self):
        return self.coordinator.data.get("Heat On")

    async def async_turn_on(self):
        await self.coordinator.client.write_gatt_char("1011000f-5354-4f52-5a26-4249434b454c", bytearray([0x01]))

    async def async_turn_off(self):
        await self.coordinator.client.write_gatt_char("10110010-5354-4f52-5a26-4249434b454c", bytearray([0x00]))
