from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import logging

_LOGGER = logging.getLogger(__name__)


class VolcanoCoordinator(DataUpdateCoordinator):
    """Coordinator for polling the Volcano Hybrid."""

    def __init__(self, hass, address):
        """Initialize the coordinator."""
        super().__init__(hass, _LOGGER, name="VolcanoCoordinator", update_interval=None)
        self.device = None

    async def _async_update_data(self):
        """Fetch data from the Bluetooth device."""
        if not self.device or not self.device.is_connected:
            _LOGGER.warning("Device is not connected. Skipping update.")
            return {}

        try:
            return await self.device.fetch_data()
        except Exception as e:
            _LOGGER.error(f"Error updating data: {e}")
            raise UpdateFailed(f"Error updating data: {e}")
