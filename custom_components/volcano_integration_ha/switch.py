from . import GATTDeviceCoordinator

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Volcano Hybrid switch entities."""
    address = hass.data["volcano_integration_ha"][config_entry.entry_id]["address"]

    coordinator = GATTDeviceCoordinator(hass, address, update_interval=0.5)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([
        GATTFanSwitch(coordinator),
        GATTHeatSwitch(coordinator),
    ])
