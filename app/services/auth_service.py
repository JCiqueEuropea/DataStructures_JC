from fastapi import Security
from fastapi.security import APIKeyHeader

from app.errors import AuthenticationError
from app.settings import get_settings

settings = get_settings()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_api_key(header: str = Security(api_key_header)):
    if header == settings.api_key_secret:
        return header

    raise AuthenticationError(message="Invalid or missing API Key credentials")
