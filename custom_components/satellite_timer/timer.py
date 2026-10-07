from datetime import timedelta
from homeassistant.components.timer import TimerEntity, TimerEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the satellite timer platform from a config entry."""
    async_add_entities([SatelliteTimerEntity(entry)])

class SatelliteTimerEntity(TimerEntity):
    """Representation of a Voice Satellite Timer Entity."""

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the timer entity."""
        self._attr_name = entry.data.get("name", "Voice Timer")
        self._attr_unique_id = entry.entry_id
        self._attr_icon = "mdi:timer-outline"
        
        # Configure supported timer features (Start, Pause, Cancel, Finish)
        self._attr_supported_features = (
            TimerEntityFeature.START
            | TimerEntityFeature.PAUSE
            | TimerEntityFeature.CANCEL
            | TimerEntityFeature.FINISH
        )
        
        # Default starting duration configuration (e.g., 5 minutes)
        default_duration_sec = entry.data.get("duration", 300)
        self._attr_duration = timedelta(seconds=default_duration_sec)
        self._attr_remaining = timedelta(seconds=0)
        self._attr_state = "idle"
