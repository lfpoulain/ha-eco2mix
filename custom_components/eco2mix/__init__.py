"""The éCO2mix integration."""

import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.const import UnitOfTime

from .coordinator import Eco2mixDataUpdateCoordinator
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

type Eco2mixConfigEntry = ConfigEntry[Eco2mixDataUpdateCoordinator]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the éCO2mix component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up éCO2mix from a config entry."""
    coordinator = Eco2mixDataUpdateCoordinator(hass, DEFAULT_SCAN_INTERVAL)

    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception:
        _LOGGER.error("Error fetching initial data")
        return False

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
