from homeassistant.components.switch import SwitchEntity

class GATTFanSwitch(SwitchEntity):
    """Entity to control the fan."""

    def __init__(self, coordinator, device_info):
        self.coordinator = coordinator
        self._attr_name = "Volcano Fan"
        self._attr_device_info = device_info

    @property
    def is_on(self):
        return self.coordinator.data.get("fan")

    async def async_turn_on(self):
        async with BleakClient(self.coordinator.address) as client:
            await client.write_gatt_char("10110013-5354-4f52-5a26-4249434b454c", bytearray([0x01]))

    async def async_turn_off(self):
        async with BleakClient(self.coordinator.address) as client:
            await client.write_gatt_char("10110013-5354-4f52-5a26-4249434b454c", bytearray([0x00]))


class GATTHeatSwitch(SwitchEntity):
    """Entity to control the heat."""

    def __init__(self, coordinator, device_info):
        self.coordinator = coordinator
        self._attr_name = "Volcano Heat"
        self._attr_device_info = device_info

    @property
    def is_on(self):
        return self.coordinator.data.get("heat")

    async def async_turn_on(self):
        async with BleakClient(self.coordinator.address) as client:
            await client.write_gatt_char("1011000f-5354-4f52-5a26-4249434b454c", bytearray([0x01]))

    async def async_turn_off(self):
        async with BleakClient(self.coordinator.address) as client:
            await client.write_gatt_char("1011000f-5354-4f52-5a26-4249434b454c", bytearray([0x00]))
