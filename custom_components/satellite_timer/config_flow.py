import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import entity_registry as er
from .const import DOMAIN

class SatelliteTimerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Satellite Timer."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step via UI."""
        errors = {}
        
        entity_registry = er.async_get(self.hass)
        satellites = [
            entry.entity_id 
            for entry in entity_registry.entities.values() 
            if entry.domain == "assist_satellite"
        ]

        if user_input is not None:
            if not satellites and not user_input.get("satellite_entity"):
                errors["base"] = "no_satellites_found"
            else:
                return self.async_create_entry(
                    title="Voice Satellite Timer Handler", 
                    data=user_input
                )

        if satellites:
            schema = vol.Schema({
                vol.Required("satellite_entity", default=satellites[0]): vol.In(satellites),
                vol.Optional("announcement_message", default="Your timer is finished!"): str,
            })
        else:
            schema = vol.Schema({
                vol.Optional("satellite_entity", default="None"): str,
                vol.Required("announcement_message", default="No satellite entities found. Please configure a satellite first."): str,
            })
            errors["base"] = "no_satellites_found"

        return self.async_show_form(
            step_id="user", 
            data_schema=schema, 
            errors=errors
        )
