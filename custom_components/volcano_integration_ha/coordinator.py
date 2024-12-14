import logging
from datetime import timedelta
from bleak import BleakClient, BleakError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

class GATTDeviceCoordinator(DataUpdateCoordinator):
    """Manages updates for the Volcano Hybrid BLE device."""

    def __init__(self, hass, address, update_interval):
        """Initialize the coordinator."""
        super().__init__(hass, _LOGGER, name="Volcano Coordinator", update_interval=timedelta(seconds=update_interval))
        self.address = address
        self.connected = False

    async def _async_update_data(self):
        """Fetch data from the Bluetooth device."""
        try:
            async with BleakClient(self.address) as client:
                self.connected = True
                return {
                    "connection_status": "Connected",
                    "temperature": await self._read_characteristic(client, "10110001-5354-4f52-5a26-4249434b454c"),
                    "fan": await self._read_characteristic(client, "10110013-5354-4f52-5a26-4249434b454c"),
                    "heat": await self._read_characteristic(client, "1011000f-5354-4f52-5a26-4249434b454c"),
                    "lcd_brightness": await self._read_characteristic(client, "10110005-5354-4f52-5a26-4249434b454c"),
                    "auto_shutoff_setting": await self._read_characteristic(client, "1011000d-5354-4f52-5a26-4249434b454c"),
                    "serial_number": await self._read_characteristic(client, "10100008-5354-4f52-5a26-4249434b454c"),
                }
        except BleakError as e:
            self.connected = False
            _LOGGER.error(f"Failed to fetch data from {self.address}: {e}")
            raise UpdateFailed(f"Failed to fetch data from {self.address}: {e}")

    async def _read_characteristic(self, client, characteristic):
        """Read a characteristic from the device."""
        try:
            value = await client.read_gatt_char(characteristic)
            return value.decode() if isinstance(value, bytes) else int.from_bytes(value, byteorder="little")
        except Exception as e:
            _LOGGER.error(f"Failed to read characteristic {characteristic}: {e}")
            raise
