from homeassistant.components.switch import SwitchEntity
from .device import VolcanoDevice


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Volcano Hybrid switch entities."""
    device = hass.data["volcano_integration_ha"][config_entry.entry_id]

    async_add_entities([
        GATTFanSwitch(device),
        GATTHeatSwitch(device),
    ])


class GATTFanSwitch(SwitchEntity):
    """Entity to control the fan."""

    def __init__(self, device):
        self.device = device
        self._attr_name = "Volcano Fan"

    @property
    def is_on(self):
        return self.device.data.get("fan_on")

    async def async_turn_on(self):
        await self.device.write_characteristic("10110013-5354-4f52-5a26-4249434b454c", bytearray([0x01]))

    async def async_turn_off(self):
        await self.device.write_characteristic("10110014-5354-4f52-5a26-4249434b454c", bytearray([0x00]))
