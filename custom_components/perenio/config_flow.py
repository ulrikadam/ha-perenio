"""Config flow for Perenio integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN
from .perenio_api import PerenioAPI

_LOGGER = logging.getLogger(__name__)


class PerenioConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Perenio."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Tester la connexion
            api = PerenioAPI(
                user_input[CONF_EMAIL],
                user_input[CONF_PASSWORD]
            )

            try:
                await api.async_setup()
                
                if api.access_token:
                    await api.async_close()
                    
                    # Créer l'entrée de configuration
                    return self.async_create_entry(
                        title=f"Perenio ({user_input[CONF_EMAIL]})",
                        data=user_input
                    )
                else:
                    errors["base"] = "invalid_auth"
                    
            except Exception as e:
                _LOGGER.error(f"Error during authentication: {e}")
                errors["base"] = "cannot_connect"
            finally:
                await api.async_close()

        # Afficher le formulaire
        data_schema = vol.Schema({
            vol.Required(CONF_EMAIL): str,
            vol.Required(CONF_PASSWORD): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )
