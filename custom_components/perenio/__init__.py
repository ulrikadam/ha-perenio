"""The Perenio integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .perenio_api import PerenioAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.CAMERA]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Perenio from a config entry."""
    email = entry.data[CONF_EMAIL]
    password = entry.data[CONF_PASSWORD]

    # Créer le client API
    api = PerenioAPI(email, password)

    try:
        await api.async_setup()
    except Exception as e:
        _LOGGER.error(f"Failed to set up Perenio: {e}")
        raise ConfigEntryNotReady from e

    if not api.access_token:
        _LOGGER.error("Failed to authenticate with Perenio")
        raise ConfigEntryNotReady("Authentication failed")

    # Stocker l'API dans hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = api

    # Charger les plateformes
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Décharger les plateformes
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        # Fermer l'API
        api = hass.data[DOMAIN].pop(entry.entry_id)
        await api.async_close()

    return unload_ok
