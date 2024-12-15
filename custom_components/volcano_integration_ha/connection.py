from homeassistant.components.switch import SwitchEntity
from homeassistant.components.sensor import SensorEntity


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Volcano Hybrid connection entities."""
    device = hass.data["volcano_integration_ha"][config_entry.entry_id].device

    async_add_entities([
        ConnectBluetoothSwitch(device),
        DisconnectBluetoothSwitch(device),
        BluetoothStatusSensor(device),
    ])


class ConnectBluetoothSwitch(SwitchEntity):
    """Entity to initiate Bluetooth connection."""

    def __init__(self, device):
        self.device = device
        self._attr_name = "Connect Bluetooth"

    @property
    def is_on(self):
        return self.device.is_connected

    async def async_turn_on(self):
        await self.device.connect()

    async def async_turn_off(self):
        """Do nothing; this switch only connects."""


class DisconnectBluetoothSwitch(SwitchEntity):
    """Entity to disconnect Bluetooth connection."""

    def __init__(self, device):
        self.device = device
        self._attr_name = "Disconnect Bluetooth"

    @property
    def is_on(self):
        return not self.device.is_connected

    async def async_turn_on(self):
        await self.device.disconnect()

    async def async_turn_off(self):
        """Do nothing; this switch only disconnects."""


class BluetoothStatusSensor(SensorEntity):
    """Entity to represent Bluetooth connection status."""

    def __init__(self, device):
        self.device = device
        self._attr_name = "Bluetooth Connection Status"

    @property
    def native_value(self):
        return self.device.status or "Disconnected"
