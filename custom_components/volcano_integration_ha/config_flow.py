from homeassistant import config_entries
import voluptuous as vol

class VolcanoIntegrationConfigFlow(config_entries.ConfigFlow, domain="volcano_integration_ha"):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Volcano Integration HA", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("address"): str,
            }),
        )
