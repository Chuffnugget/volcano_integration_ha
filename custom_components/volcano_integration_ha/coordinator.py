import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .device import VolcanoDevice

_LOGGER = logging.getLogger(__name__)

class VolcanoCoordinator(DataUpdateCoordinator):
    """Coordinator for polling the Volcano Hybrid."""

    def __init__(self, hass, address):
        """Initialize the coordinator."""
        super().__init__(hass, _LOGGER, name="VolcanoCoordinator", update_interval=timedelta(seconds=0.5))
        self.device = VolcanoDevice(address)

    async def _async_update_data(self):
        """Fetch data from the Bluetooth device."""
        try:
            return await self.device.fetch_data()
        except Exception as e:
            _LOGGER.error(f"Error updating data: {e}")
            raise UpdateFailed(f"Error updating data: {e}")

    async def shutdown(self):
        """Shut down the Bluetooth connection."""
        await self.device.disconnect()
