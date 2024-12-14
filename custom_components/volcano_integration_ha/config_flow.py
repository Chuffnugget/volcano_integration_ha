from homeassistant import config_entries
import voluptuous as vol
import logging

_LOGGER = logging.getLogger(__name__)

class VolcanoIntegrationConfigFlow(config_entries.ConfigFlow, domain="volcano_integration_ha"):
    """Handle a config flow for Volcano Hybrid Integration."""

    async def async_step_user(self, user_input=None):
        """Step where the user provides the Bluetooth address."""
        if user_input is not None:
            address = user_input.get("address")
            if not self._validate_address(address):
                return self.async_show_form(
                    step_id="user",
                    data_schema=self._schema(),
                    errors={"address": "invalid_address"},
                )
            return self.async_create_entry(title="Volcano Hybrid", data=user_input)

        return self.async_show_form(step_id="user", data_schema=self._schema())

    def _schema(self):
        """Return the data schema for user input."""
        return vol.Schema({
            vol.Required("address"): str,
        })

    def _validate_address(self, address):
        """Validate the provided Bluetooth address."""
        if not isinstance(address, str) or len(address.split(":")) != 6:
            _LOGGER.error(f"Invalid Bluetooth address provided: {address}")
            return False
        return True
