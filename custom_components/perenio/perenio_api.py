"""Perenio API Client."""
import logging
import aiohttp
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

from .const import (
    OAUTH_TOKEN_URL,
    OAUTH_USER_URL,
    API_BASE_URL,
    DEFAULT_TENANT_ID,
    DEFAULT_CLIENT_ID,
    DEFAULT_CLIENT_SECRET,
    TOKEN_EXPIRY,
)

_LOGGER = logging.getLogger(__name__)


class PerenioAPI:
    """Client pour l'API Perenio Cloud."""

    def __init__(self, email: str, password: str):
        """Initialize the Perenio API client."""
        self.email = email
        self.password = password
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        self.session: Optional[aiohttp.ClientSession] = None
        self.user_info: Optional[Dict[str, Any]] = None

    async def async_setup(self):
        """Set up the API client."""
        self.session = aiohttp.ClientSession()
        await self.async_authenticate()

    async def async_close(self):
        """Close the API client."""
        if self.session:
            await self.session.close()

    async def async_authenticate(self) -> bool:
        """Authenticate with Perenio OAuth2."""
        if not self.session:
            self.session = aiohttp.ClientSession()

        # Préparer les données de login OAuth2
        # Format: application/x-www-form-urlencoded
        data = {
            "grant_type": "password",
            "client_id": DEFAULT_CLIENT_ID,
            "client_secret": DEFAULT_CLIENT_SECRET,
            "username": self.email,
            "password": self.password,
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "tenantId": DEFAULT_TENANT_ID,
            "Accept": "application/json",
        }

        try:
            async with self.session.post(
                OAUTH_TOKEN_URL, 
                data=data, 
                headers=headers
            ) as resp:
                if resp.status == 200:
                    token_data = await resp.json()
                    
                    self.access_token = token_data.get("access_token")
                    self.refresh_token = token_data.get("refresh_token")
                    expires_in = token_data.get("expires_in", TOKEN_EXPIRY)
                    
                    # Calculer la date d'expiration
                    self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                    
                    _LOGGER.info("Successfully authenticated with Perenio")
                    
                    # Récupérer les infos utilisateur
                    await self.async_get_user_info()
                    
                    return True
                else:
                    error_text = await resp.text()
                    _LOGGER.error(f"Authentication failed: {resp.status} - {error_text}")
                    return False
                    
        except Exception as e:
            _LOGGER.error(f"Authentication error: {e}")
            return False

    async def async_refresh_token_if_needed(self):
        """Refresh token if it's about to expire."""
        if not self.token_expires_at or not self.refresh_token:
            return await self.async_authenticate()

        # Rafraîchir 5 minutes avant l'expiration
        if datetime.now() >= self.token_expires_at - timedelta(minutes=5):
            _LOGGER.debug("Token expiring soon, refreshing...")
            
            data = {
                "grant_type": "refresh_token",
                "client_id": DEFAULT_CLIENT_ID,
                "client_secret": DEFAULT_CLIENT_SECRET,
                "refresh_token": self.refresh_token,
            }

            headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                "tenantId": DEFAULT_TENANT_ID,
            }

            try:
                async with self.session.post(
                    OAUTH_TOKEN_URL, 
                    data=data, 
                    headers=headers
                ) as resp:
                    if resp.status == 200:
                        token_data = await resp.json()
                        self.access_token = token_data.get("access_token")
                        self.refresh_token = token_data.get("refresh_token")
                        expires_in = token_data.get("expires_in", TOKEN_EXPIRY)
                        self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                        _LOGGER.info("Token refreshed successfully")
                        return True
                    else:
                        _LOGGER.warning("Token refresh failed, re-authenticating...")
                        return await self.async_authenticate()
                        
            except Exception as e:
                _LOGGER.error(f"Token refresh error: {e}")
                return await self.async_authenticate()

        return True

    async def async_get_user_info(self) -> Optional[Dict[str, Any]]:
        """Get user information."""
        headers = self._get_headers()
        
        try:
            async with self.session.get(OAUTH_USER_URL, headers=headers) as resp:
                if resp.status == 200:
                    self.user_info = await resp.json()
                    _LOGGER.debug(f"User info: {self.user_info}")
                    return self.user_info
                else:
                    _LOGGER.error(f"Failed to get user info: {resp.status}")
                    return None
                    
        except Exception as e:
            _LOGGER.error(f"Error getting user info: {e}")
            return None

    def _get_headers(self) -> Dict[str, str]:
        """Get standard API headers."""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "tenantId": DEFAULT_TENANT_ID,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def async_get_devices(self) -> List[Dict[str, Any]]:
        """Get list of devices (cameras)."""
        await self.async_refresh_token_if_needed()
        
        headers = self._get_headers()
        
        # Essayer différents endpoints
        endpoints_to_try = [
            f"{API_BASE_URL}/endpoints",
            f"{API_BASE_URL}/devices",
            f"{API_BASE_URL}/cameras",
        ]
        
        for endpoint in endpoints_to_try:
            try:
                async with self.session.get(endpoint, headers=headers) as resp:
                    if resp.status == 200:
                        devices = await resp.json()
                        _LOGGER.info(f"Successfully got devices from {endpoint}")
                        return devices if isinstance(devices, list) else []
                    elif resp.status != 404:
                        _LOGGER.warning(f"Endpoint {endpoint} returned {resp.status}")
                        
            except Exception as e:
                _LOGGER.error(f"Error getting devices from {endpoint}: {e}")
        
        _LOGGER.warning("Could not find devices endpoint")
        return []

    async def async_get_camera_snapshot(self, camera_id: str) -> Optional[bytes]:
        """Get snapshot from camera."""
        await self.async_refresh_token_if_needed()
        
        headers = self._get_headers()
        
        # Essayer différentes méthodes pour obtenir un snapshot
        urls_to_try = [
            f"{API_BASE_URL}/file/{camera_id}/snapshot",
            f"{API_BASE_URL}/endpoints/{camera_id}/snapshot",
        ]
        
        # Essayer aussi via commandes
        command_url = f"{API_BASE_URL}/commands"
        params = {
            "endpointId": camera_id,
            "commandType": "GET_SNAPSHOT"
        }
        
        try:
            async with self.session.post(
                command_url, 
                headers=headers, 
                params=params,
                json={}
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    # Le résultat peut contenir une URL vers le snapshot
                    if isinstance(result, dict) and "url" in result:
                        async with self.session.get(result["url"]) as img_resp:
                            if img_resp.status == 200:
                                return await img_resp.read()
                                
        except Exception as e:
            _LOGGER.debug(f"Snapshot command failed: {e}")
        
        # Essayer les URLs directes
        for url in urls_to_try:
            try:
                async with self.session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        return await resp.read()
                        
            except Exception as e:
                _LOGGER.debug(f"Snapshot URL {url} failed: {e}")
        
        return None

    async def async_get_camera_stream_url(self, camera_id: str) -> Optional[str]:
        """Get stream URL for camera (WebRTC)."""
        await self.async_refresh_token_if_needed()
        
        headers = self._get_headers()
        
        # L'app utilise WebRTC avec /mediastream/{camera_id}/offer
        url = f"{API_BASE_URL}/mediastream/{camera_id}/offer"
        
        try:
            async with self.session.post(url, headers=headers, json={}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    _LOGGER.debug(f"Stream offer response: {data}")
                    # WebRTC SDP offer
                    return data
                else:
                    _LOGGER.warning(f"Stream offer failed: {resp.status}")
                    
        except Exception as e:
            _LOGGER.error(f"Error getting stream URL: {e}")
        
        return None

    async def async_get_camera_files(
        self, camera_id: str, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get recorded video files from camera."""
        await self.async_refresh_token_if_needed()
        
        headers = self._get_headers()
        url = f"{API_BASE_URL}/file/{camera_id}/files"
        
        params = {
            "endpointId": camera_id,
            "limit": limit,
            "mimeTypeMask": "video/*",
            "offset": 0,
            "parameters[sort]": "DESC"
        }
        
        try:
            async with self.session.get(url, headers=headers, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data if isinstance(data, list) else []
                else:
                    _LOGGER.warning(f"Get files failed: {resp.status}")
                    
        except Exception as e:
            _LOGGER.error(f"Error getting camera files: {e}")
        
        return []
