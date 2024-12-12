async def async_setup_entry(hass, config_entry):
    hass.data.setdefault("volcano_integration_ha", {})
    hass.data["volcano_integration_ha"][config_entry.entry_id] = config_entry.data
    return True
