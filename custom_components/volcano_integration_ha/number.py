from homeassistant.components.number import NumberEntity

class GATTSetTargetTemperature(NumberEntity):
    """Entity to set the target temperature."""

    def __init__(self, coordinator, device_info):
        self.coordinator = coordinator
        self._attr_name = "Set Target Temperature"
        self._attr_device_info = device_info
        self._attr_min_value = 40
        self._attr_max_value = 230
        self._attr_step = 1

    @property
    def native_value(self):
        return self.coordinator.data.get("temperature")

    async def async_set_native_value(self, value):
        async with BleakClient(self.coordinator.address) as client:
            await client.write_gatt_char("10110003-5354-4f52-5a26-4249434b454c", int(value).to_bytes(2, "little"))
