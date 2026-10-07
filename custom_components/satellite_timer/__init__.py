from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, Event, ServiceCall
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Satellite Timer listener and services."""
    satellite_entity = entry.data.get("satellite_entity")
    announcement_message = entry.data.get("announcement_message", "Your timer is finished!")

    async def handle_timer_finished(event: Event) -> None:
        """Catch when any timer finishes and announce it on the satellite if available."""
        if not satellite_entity or satellite_entity == "None":
            return
            
        await hass.services.async_call(
            "assist_satellite",
            "announce",
            {
                "entity_id": satellite_entity,
                "message": announcement_message,
            },
            blocking=False,
        )

    entry.async_on_unload(
        hass.bus.async_listen("timer.finished", handle_timer_finished)
    )

    async def async_set_timer(call: ServiceCall) -> None:
        entity_id = call.data.get("entity_id")
        hours = call.data.get("hours", 0)
        minutes = call.data.get("minutes", 0)
        seconds = call.data.get("seconds", 0)
        total_duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        
        await hass.services.async_call(
            "timer",
            "start",
            {"entity_id": entity_id, "duration": str(total_duration)},
            blocking=False,
        )

    async def async_pause_timer(call: ServiceCall) -> None:
        await hass.services.async_call(
            "timer",
            "pause",
            {"entity_id": call.data.get("entity_id")},
            blocking=False,
        )

    async def async_cancel_timer(call: ServiceCall) -> None:
        await hass.services.async_call(
            "timer",
            "cancel",
            {"entity_id": call.data.get("entity_id")},
            blocking=False,
        )

    hass.services.async_register(DOMAIN, "set", async_set_timer)
    hass.services.async_register(DOMAIN, "pause", async_pause_timer)
    hass.services.async_register(DOMAIN, "cancel", async_cancel_timer)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
