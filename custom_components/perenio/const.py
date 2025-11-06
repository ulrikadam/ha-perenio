"""Constants for the Perenio integration."""

DOMAIN = "perenio"

# OAuth endpoints
OAUTH_BASE_URL = "https://oauth.perenio.com/auth/realms/aaa.kaa"
OAUTH_TOKEN_URL = f"{OAUTH_BASE_URL}/protocol/openid-connect/token"
OAUTH_USER_URL = f"{OAUTH_BASE_URL}/users/me"

# API endpoints
API_BASE_URL = "https://iot.perenio.com/apif/api/v1"

# Configuration
CONF_EMAIL = "email"
CONF_PASSWORD = "password"

# Default values
DEFAULT_TENANT_ID = "perenio"
DEFAULT_CLIENT_ID = "perenio-app"
DEFAULT_CLIENT_SECRET = "ecbea13f-a1cd-47ff-a01e-60082fb8b999"
DEFAULT_SCAN_INTERVAL = 30

# Token expiry (in seconds) - 10 days
TOKEN_EXPIRY = 864000
