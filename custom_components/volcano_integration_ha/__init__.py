import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .coordinator import VolcanoCoordinator

DOMAIN = "volcano_integration_ha"
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Set up Volcano Integration HA."""
    address = config_entry.data["address"]
    coordinator = VolcanoCoordinator(hass, address)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    for platform in ["sensor", "switch", "number"]:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(config_entry, platform)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Unload Volcano Integration HA."""
    coordinator = hass.data[DOMAIN].pop(config_entry.entry_id)
    await coordinator.shutdown()

    unload_ok = all(
        await hass.config_entries.async_forward_entry_unload(config_entry, platform)
        for platform in ["sensor", "switch", "number"]
    )

    return unload_ok
