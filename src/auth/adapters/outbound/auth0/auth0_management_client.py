from typing import Any

import httpx

from auth.application.exceptions.identity_provider import (
    IdentityProviderAuthenticationError,
    IdentityProviderPermissionError,
    IdentityProviderRateLimitError,
    IdentityProviderUnavailableError,
    IdentityProviderUserAlreadyExistsError,
)
from auth.infrastructure.config.settings import settings


class Auth0ManagementClient:
    def __init__(self) -> None:
        self._domain = settings.auth0_domain
        self._client_id = settings.auth0_client_id
        self._client_secret = settings.auth0_client_secret
        self._audience = settings.auth0_audience
        self._connection = settings.auth0_db_connection

        self._base_url = f"https://{self._domain}"

    async def _get_management_token(self) -> str:
        url = f"{self._base_url}/oauth/token"

        payload = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "audience": self._audience,
            "grant_type": "client_credentials",
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=payload,
                    timeout=10.0,
                )
        except httpx.RequestError as exc:
            raise IdentityProviderUnavailableError(
                "Identity provider is unavailable."
            ) from exc

        if response.is_error:
            self._handle_error_response(response)

        data: dict[str, Any] = response.json()
        return data["access_token"]

    async def create_user(
        self,
        email: str,
        password: str,
        full_name: str,
    ) -> dict[str, Any]:
        token = await self._get_management_token()

        url = f"{self._base_url}/api/v2/users"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        payload = {
            "connection": self._connection,
            "email": email,
            "password": password,
            "name": full_name,
            "verify_email": False,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=10.0,
                )
        except httpx.RequestError as exc:
            raise IdentityProviderUnavailableError(
                "Identity provider is unavailable."
            ) from exc

        if response.is_error:
            self._handle_error_response(response)

        return response.json()
    
    async def update_user_metadata(
        self,
        user_id: str,
        tipo_documento: str,
        numero_documento: str,
    ) -> dict[str, Any]:
        token = await self._get_management_token()

        url = f"{self._base_url}/api/v2/users/{user_id}"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        payload = {
            "user_metadata": {
                "tipo_documento": tipo_documento,
                "numero_documento": numero_documento,
            }
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=10.0,
                )
        except httpx.RequestError as exc:
            raise IdentityProviderUnavailableError(
                "Identity provider is unavailable."
            ) from exc

        if response.is_error:
            self._handle_error_response(response)

        data: dict[str, Any] = response.json()

        return data.get("user_metadata", {})
    
    def _handle_error_response(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise IdentityProviderAuthenticationError(
                "Authentication with identity provider failed."
            )

        if response.status_code == 403:
            raise IdentityProviderPermissionError(
                "Identity provider denied the operation."
            )

        if response.status_code == 409:
            raise IdentityProviderUserAlreadyExistsError(
                "User already exists in identity provider."
            )

        if response.status_code == 429:
            raise IdentityProviderRateLimitError(
                "Identity provider rate limit exceeded."
            )

        response.raise_for_status()

    async def get_user(
        self,
        user_id: str,
    ) -> dict[str, Any]:
        token = await self._get_management_token()

        url = f"{self._base_url}/api/v2/users/{user_id}"

        headers = {
            "Authorization": f"Bearer {token}",
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers=headers,
                    timeout=10.0,
                )
        except httpx.RequestError as exc:
            raise IdentityProviderUnavailableError(
                "Identity provider is unavailable."
            ) from exc

        if response.is_error:
            self._handle_error_response(response)

        return response.json()


    async def update_user_password(
        self,
        user_id: str,
        password: str,
    ) -> None:
        token = await self._get_management_token()

        url = f"{self._base_url}/api/v2/users/{user_id}"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        payload = {
            "password": password,
            "connection": settings.auth0_db_connection,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=10.0,
                )
        except httpx.RequestError as exc:
            raise IdentityProviderUnavailableError(
                "Identity provider is unavailable."
            ) from exc

        if response.is_error:
            self._handle_error_response(response)