from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, Event
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Satellite Timer listener from a config entry."""
    satellite_entity = entry.data.get("satellite_entity")

    async def handle_timer_finished(event: Event) -> None:
        """Catch when any timer finishes and announce it on the satellite."""
        entity_id = event.data.get("entity_id")
        
        await hass.services.async_call(
            "assist_satellite",
            "announce",
            {
                "entity_id": satellite_entity,
                "message": "Your timer is finished!",
            },
            blocking=False,
        )

    entry.async_on_unload(
        hass.bus.async_listen("timer.finished", handle_timer_finished)
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
