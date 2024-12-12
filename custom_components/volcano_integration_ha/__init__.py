async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the integration."""
    address = config_entry.data.get("address")

    if not address:
        _LOGGER.error("No Bluetooth address provided. Configuration is incomplete.")
        return False

    try:
        client = BleakClient(address)
        coordinator = GATTDeviceCoordinator(hass, client, update_interval)
        await coordinator.async_config_entry_first_refresh()

        device_info = DeviceInfo(
            identifiers={("volcano_integration_ha", address)},
            name="Volcano Device",
            manufacturer="Volcano",
            model="Volcano BT",
            entry_type=DeviceEntryType.SERVICE,
        )

        async_add_entities([
            GATTTemperatureSensor(coordinator, device_info),
            GATTFanSwitch(coordinator, device_info),
            GATTHeatSwitch(coordinator, device_info),
            GATTLCDBrightnessSensor(coordinator, device_info),
            GATTAutoShutoffSensor(coordinator, device_info),
        ])
        return True
    except Exception as e:
        _LOGGER.error(f"Error during setup of Bluetooth client: {e}")
        return False
