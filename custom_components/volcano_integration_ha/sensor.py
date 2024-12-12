from homeassistant.components.sensor import SensorEntity

class VolcanoSensor(SensorEntity):
    def __init__(self, coordinator, name, data_key):
        self.coordinator = coordinator
        self._attr_name = name
        self.data_key = data_key

    @property
    def native_value(self):
        return self.coordinator.data[self.data_key]
