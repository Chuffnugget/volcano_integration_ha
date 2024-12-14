from homeassistant.components.sensor import SensorEntity

class GATTConnectionStatus(SensorEntity):
    """Entity to track Bluetooth connection status."""

    def __init__(self, coordinator, device_info):
        self.coordinator = coordinator
        self._attr_name = "Volcano Connection Status"
        self._attr_device_info = device_info

    @property
    def native_value(self):
        return "Connected" if self.coordinator.connected else "Disconnected"


class GATTSerialNumber(SensorEntity):
    """Entity to show the serial number."""

    def __init__(self, coordinator, device_info):
        self.coordinator = coordinator
        self._attr_name = "Volcano Serial Number"
        self._attr_device_info = device_info

    @property
    def native_value(self):
        return self.coordinator.data.get("serial_number")


class GATTTemperatureSensor(SensorEntity):
    """Entity to monitor the current temperature."""

    def __init__(self, coordinator, device_info):
        self.coordinator = coordinator
        self._attr_name = "Volcano Current Temperature"
        self._attr_device_info = device_info

    @property
    def native_value(self):
        return self.coordinator.data.get("temperature")
