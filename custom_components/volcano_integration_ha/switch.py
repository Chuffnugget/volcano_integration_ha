from homeassistant.components.switch import SwitchEntity

class VolcanoSwitch(SwitchEntity):
    def __init__(self, coordinator, name, data_key, write_func):
        self.coordinator = coordinator
        self._attr_name = name
        self.data_key = data_key
        self.write_func = write_func

    @property
    def is_on(self):
        return self.coordinator.data[self.data_key]

    async def async_turn_on(self):
        await self.write_func(True)

    async def async_turn_off(self):
        await self.write_func(False)
