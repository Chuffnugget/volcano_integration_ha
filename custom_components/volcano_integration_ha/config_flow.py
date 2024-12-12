from homeassistant import config_entries
import voluptuous as vol
from bleak import BleakClient
import asyncio

class VolcanoIntegrationConfigFlow(config_entries.ConfigFlow, domain="volcano_integration_ha"):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            address = user_input["address"]
            # Validate Bluetooth address by trying to connect and read a characteristic
            if not await self._validate_address(address):
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema({
                        vol.Required("address"): str,
                    }),
                    errors={"base": "invalid_address"},
                )

            return self.async_create_entry(title="Volcano Integration HA", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("address"): str,
            }),
        )

    async def _validate_address(self, address):
        """Validate the provided Bluetooth address by connecting to the device."""
        try:
            async with BleakClient(address) as client:
                # Try reading a characteristic to validate connection
                await client.read_gatt_char("10110001-5354-4f52-5a26-4249434b454c")
                return True
        except Exception as e:
            self._log_error(address, e)
            return False

    def _log_error(self, address, error):
        """Log validation errors."""
        self.hass.helpers.logger.error(
            f"Failed to validate Bluetooth address {address}: {error}"
        )
