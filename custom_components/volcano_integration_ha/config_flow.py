from homeassistant import config_entries
import voluptuous as vol
import logging

_LOGGER = logging.getLogger(__name__)

class VolcanoIntegrationConfigFlow(config_entries.ConfigFlow, domain="volcano_integration_ha"):
    """Handle a config flow for Volcano Hybrid Integration."""

    async def async_step_user(self, user_input=None):
        """Step where the user provides the Bluetooth address."""
        if user_input is not None:
            return self.async_create_entry(title="Volcano Hybrid", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("address"): str,
            }),
        )
