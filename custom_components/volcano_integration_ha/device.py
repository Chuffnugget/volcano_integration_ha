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

    async def connect(self):
        """Connect to the Bluetooth device."""
        if not self.client.is_connected:
            await self.client.connect()
            _LOGGER.info(f"Connected to {self.address}")

    async def disconnect(self):
        """Disconnect from the Bluetooth device."""
        if self.client.is_connected:
            await self.client.disconnect()
            _LOGGER.info(f"Disconnected from {self.address}")

    async def fetch_data(self):
        """Fetch data from the Bluetooth device."""
        await self.connect()

        try:
            temperature = await self.read_characteristic(UUIDS["temperature"])
            return {
                "temperature": temperature,
                # Add more data mappings here...
            }
        except Exception as e:
            _LOGGER.error(f"Error fetching data: {e}")
            raise

    async def read_characteristic(self, uuid):
        """Read a characteristic from the Bluetooth device."""
        try:
            value = await self.client.read_gatt_char(uuid)
            _LOGGER.info(f"Read {uuid}: {value}")
            return value
        except Exception as e:
            _LOGGER.error(f"Error reading {uuid}: {e}")
            raise

    async def write_characteristic(self, uuid, value):
        """Write a characteristic to the Bluetooth device."""
        try:
            await self.client.write_gatt_char(uuid, value)
            _LOGGER.info(f"Wrote {uuid}: {value}")
        except Exception as e:
            _LOGGER.error(f"Error writing {uuid}: {e}")
            raise
