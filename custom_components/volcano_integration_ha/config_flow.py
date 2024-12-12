from homeassistant import config_entries
import voluptuous as vol
from bleak import BleakClient
import logging

_LOGGER = logging.getLogger(__name__)

class VolcanoIntegrationConfigFlow(config_entries.ConfigFlow, domain="volcano_integration_ha"):
    async def async_step_user(self, user_input=None):
        """Step for user to input the Bluetooth address."""
        if user_input is not None:
            address = user_input["address"]
            if not await self._validate_address(address):
                return self.async_show_form(
                    step_id="user",
                    data_schema=self._get_schema(),
                    errors={"base": "invalid_address"},
                )

            return self.async_create_entry(title="Volcano Device", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=self._get_schema(),
        )

    def _get_schema(self):
        """Return the schema for the configuration form."""
        return vol.Schema({
            vol.Required("address"): str,
        })

    async def _validate_address(self, address):
        """Validate the provided Bluetooth address."""
        try:
            async with BleakClient(address) as client:
                # Test reading a characteristic to validate the address
                await client.read_gatt_char("10110001-5354-4f52-5a26-4249434b454c")
                return True
        except Exception as e:
            _LOGGER.error(f"Validation failed for Bluetooth address {address}: {e}")
            return False
