import logging
from datetime import timedelta
from bleak import BleakClient, BleakError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import asyncio

_LOGGER = logging.getLogger(__name__)

RECONNECT_DELAY = 5  # Delay between reconnection attempts, in seconds
MAX_RETRIES = 5      # Maximum reconnection attempts

class GATTDeviceCoordinator(DataUpdateCoordinator):
    """Manages updates for the Volcano Hybrid BLE device."""

    def __init__(self, hass, address, update_interval):
        """Initialize the coordinator."""
        super().__init__(hass, _LOGGER, name="Volcano Coordinator", update_interval=timedelta(seconds=update_interval))
        self.address = address
        self.connected = False
        self.client = None

    async def _async_update_data(self):
        """Fetch data from the Bluetooth device."""
        try:
            if not self.client or not self.connected:
                await self._connect()

            return {
                "Fan On": await self._read_characteristic("10110013-5354-4f52-5a26-4249434b454c"),
                "Fan Off": await self._read_characteristic("10110014-5354-4f52-5a26-4249434b454c"),
                "Heat On": await self._read_characteristic("1011000f-5354-4f52-5a26-4249434b454c"),
                "Heat Off": await self._read_characteristic("10110010-5354-4f52-5a26-4249434b454c"),
                "Temperature Read": await self._read_characteristic("10110001-5354-4f52-5a26-4249434b454c"),
                "BLE Firmware Version": await self._read_characteristic("10100004-5354-4f52-5a26-4249434b454c"),
                "Serial Number": await self._read_characteristic("10100008-5354-4f52-5a26-4249434b454c"),
                "Volcano Firmware Version": await self._read_characteristic("10100003-5354-4f52-5a26-4249434b454c"),
                "Auto Shutoff": await self._read_characteristic("1011000c-5354-4f52-5a26-4249434b454c"),
                "Auto Shutoff Setting": await self._read_characteristic("1011000d-5354-4f52-5a26-4249434b454c"),
                "LCD Brightness": await self._read_characteristic("10110005-5354-4f52-5a26-4249434b454c"),
                "Hours of Operation": await self._read_characteristic("10110015-5354-4f52-5a26-4249434b454c"),
                "Minutes of Operation": await self._read_characteristic("10110016-5354-4f52-5a26-4249434b454c"),
            }
        except BleakError as e:
            self.connected = False
            _LOGGER.error(f"Failed to fetch data from {self.address}: {e}")
            raise UpdateFailed(f"Failed to fetch data from {self.address}: {e}")

    async def _connect(self):
        """Ensure the client is connected to the Bluetooth device."""
        retries = 0
        while retries < MAX_RETRIES:
            try:
                self.client = BleakClient(self.address)
                await self.client.connect()
                self.connected = True
                _LOGGER.info(f"Connected to Bluetooth device at {self.address}")
                return
            except BleakError as e:
                retries += 1
                _LOGGER.warning(f"Connection attempt {retries}/{MAX_RETRIES} failed: {e}")
                await asyncio.sleep(RECONNECT_DELAY)

        _LOGGER.error(f"Unable to connect to Bluetooth device at {self.address} after {MAX_RETRIES} attempts")
        raise UpdateFailed(f"Unable to connect to Bluetooth device at {self.address}")

    async def _read_characteristic(self, uuid):
        """Read a characteristic value from the device."""
        try:
            value = await self.client.read_gatt_char(uuid)
            _LOGGER.info(f"Read characteristic {uuid}: {value}")
            return value.decode() if isinstance(value, bytes) else int.from_bytes(value, byteorder="little")
        except Exception as e:
            _LOGGER.error(f"Failed to read characteristic {uuid}: {e}")
            raise
