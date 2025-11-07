"""Support for Perenio cameras."""
import logging
from typing import Optional

from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .perenio_api import PerenioAPI

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Perenio camera from a config entry."""
    api: PerenioAPI = hass.data[DOMAIN][entry.entry_id]

    # Récupérer la liste des caméras
    devices = await api.async_get_devices()

    cameras = []
    for device in devices:
        # Filtrer uniquement les caméras
        # Le type exact dépend de la structure des données de l'API
        if isinstance(device, dict):
            camera_id = device.get("id") or device.get("endpointId")
            camera_name = device.get("name") or device.get("deviceName") or f"Camera {camera_id}"
            
            if camera_id:
                _LOGGER.info(f"Adding Perenio camera: {camera_name} ({camera_id})")
                cameras.append(PerenioCamera(api, device, camera_id, camera_name))

    if cameras:
        async_add_entities(cameras)
    else:
        _LOGGER.warning("No cameras found in Perenio account")


class PerenioCamera(Camera):
    """Representation of a Perenio Camera."""

    def __init__(
        self,
        api: PerenioAPI,
        device: dict,
        camera_id: str,
        camera_name: str,
    ):
        """Initialize a Perenio camera."""
        super().__init__()
        
        self._api = api
        self._device = device
        self._camera_id = camera_id
        self._camera_name = camera_name
        
        # Attributs de l'entité
        self._attr_name = camera_name
        self._attr_unique_id = f"perenio_{camera_id}"
        self._attr_should_poll = True
        
        # Features supportées (ON_DEMAND disponible depuis HA 2023.8+)
        try:
            self._attr_supported_features = CameraEntityFeature.ON_DEMAND
        except AttributeError:
            # ON_DEMAND non disponible dans les anciennes versions
            self._attr_supported_features = 0

    @property
    def device_info(self):
        """Return device information about this camera."""
        return {
            "identifiers": {(DOMAIN, self._camera_id)},
            "name": self._camera_name,
            "manufacturer": "Perenio",
            "model": self._device.get("model", "PEIFC01"),
            "sw_version": self._device.get("firmwareVersion"),
        }

    @property
    def available(self) -> bool:
        """Return True if camera is available."""
        # Vérifier si l'API est connectée
        return self._api.access_token is not None

    async def async_camera_image(
        self, width: Optional[int] = None, height: Optional[int] = None
    ) -> Optional[bytes]:
        """Return a still image from the camera."""
        try:
            image = await self._api.async_get_camera_snapshot(self._camera_id)
            if image:
                _LOGGER.debug(f"Got snapshot for {self._camera_name}")
                return image
            else:
                _LOGGER.warning(f"No snapshot available for {self._camera_name}")
                return None
                
        except Exception as e:
            _LOGGER.error(f"Error getting snapshot for {self._camera_name}: {e}")
            return None

    async def stream_source(self) -> Optional[str]:
        """Return the stream source (for WebRTC)."""
        try:
            stream_info = await self._api.async_get_camera_stream_url(self._camera_id)
            if stream_info:
                _LOGGER.debug(f"Got stream info for {self._camera_name}: {stream_info}")
                # WebRTC necessiterait une implémentation plus complexe
                # Pour l'instant, retourner None
                return None
            else:
                _LOGGER.warning(f"No stream available for {self._camera_name}")
                return None
                
        except Exception as e:
            _LOGGER.error(f"Error getting stream for {self._camera_name}: {e}")
            return None

    @property
    def extra_state_attributes(self):
        """Return extra state attributes."""
        attrs = {
            "camera_id": self._camera_id,
        }
        
        # Ajouter d'autres attributs du device si disponibles
        if "status" in self._device:
            attrs["status"] = self._device["status"]
        
        if "online" in self._device:
            attrs["online"] = self._device["online"]
            
        return attrs

    async def async_update(self):
        """Update camera status."""
        try:
            # Rafraîchir le token si nécessaire
            await self._api.async_refresh_token_if_needed()
            
            # Optionnel: récupérer l'état à jour du device
            # devices = await self._api.async_get_devices()
            # for device in devices:
            #     if device.get("id") == self._camera_id:
            #         self._device = device
            #         break
            
        except Exception as e:
            _LOGGER.error(f"Error updating {self._camera_name}: {e}")
