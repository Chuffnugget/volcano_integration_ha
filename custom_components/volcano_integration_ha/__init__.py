import logging
import asyncio

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry):
    """Set up the Volcano Hybrid integration."""
    hass.data.setdefault("volcano_integration_ha", {})
    hass.data["volcano_integration_ha"][config_entry.entry_id] = {
        "address": config_entry.data["address"]
    }

    # Forward the setup to each platform
    for platform in ["sensor", "switch", "number"]:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(config_entry, platform)
        )

    return True


async def async_unload_entry(hass, config_entry):
    """Unload the Volcano Hybrid integration."""
    unload_results = await asyncio.gather(
        *[
            hass.config_entries.async_forward_entry_unload(config_entry, platform)
            for platform in ["sensor", "switch", "number"]
        ]
    )

    if all(unload_results):
        hass.data["volcano_integration_ha"].pop(config_entry.entry_id)

    return all(unload_results)
