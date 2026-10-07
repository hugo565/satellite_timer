import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from .const import DOMAIN

class SatelliteTimerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Satellite Timer."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step via UI."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(
                title=user_input["name"], 
                data=user_input
            )

        schema = vol.Schema({
            vol.Required("name", default="Voice Satellite Timer"): str,
            vol.Required("duration", default=300): int, # Default duration in seconds
        })

        return self.async_show_form(
            step_id="user", 
            data_schema=schema, 
            errors=errors
        )
