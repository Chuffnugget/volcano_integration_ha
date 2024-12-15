import logging
from bleak import BleakClient

_LOGGER = logging.getLogger(__name__)

UUIDS = {
    "fan_on": "10110013-5354-4f52-5a26-4249434b454c",
    "fan_off": "10110014-5354-4f52-5a26-4249434b454c",
    "temperature": "10110001-5354-4f52-5a26-4249434b454c",
    # Add other UUIDs here...
}


class VolcanoDevice:
    """Representation of the Volcano Hybrid Bluetooth device."""

    def __init__(self, address):
        self.address = address
        self.client = BleakClient(address)
        self.is_connected = False
        self.status = None

    async def connect(self):
        """Connect to the Bluetooth device."""
        try:
            await self.client.connect()
            self.is_connected = True
            self.status = None
            _LOGGER.info(f"Connected to {self.address}")
        except Exception as e:
            self.status = f"Error connecting: {e}"
            self.is_connected = False
            _LOGGER.error(self.status)

    async def disconnect(self):
        """Disconnect from the Bluetooth device."""
        try:
            await self.client.disconnect()
            self.is_connected = False
            self.status = None
            _LOGGER.info(f"Disconnected from {self.address}")
        except Exception as e:
            self.status = f"Error disconnecting: {e}"
            _LOGGER.error(self.status)

    async def fetch_data(self):
        """Fetch data from the Bluetooth device."""
        if not self.is_connected:
            raise Exception("Device is not connected")
        try:
            temperature_raw = await self.read_characteristic(UUIDS["temperature"])
            temperature = int.from_bytes(temperature_raw, byteorder="little") / 100.0
            return {
                "temperature": temperature,
            }
        except Exception as e:
            _LOGGER.error(f"Error fetching data: {e}")
            raise

    async def read_characteristic(self, uuid):
        """Read a characteristic from the Bluetooth device."""
        try:
            value = await self.client.read_gatt_char(uuid)
            return value
        except Exception as e:
            _LOGGER.error(f"Error reading {uuid}: {e}")
            raise
