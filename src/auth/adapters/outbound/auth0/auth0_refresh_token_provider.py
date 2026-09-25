from typing import Any

import httpx

from auth.application.dtos.refresh_token import RefreshTokenCommand
from auth.application.dtos.refresh_token_output import RefreshTokenOutputDTO
from auth.application.exceptions.authentication import InvalidCredentialsError
from auth.application.exceptions.identity_provider import (
    IdentityProviderUnavailableError,
)
from auth.application.ports.refresh_token_provider import (
    RefreshTokenProviderPort,
)
from auth.infrastructure.config.settings import settings


class Auth0RefreshTokenProvider(RefreshTokenProviderPort):
    async def refresh(
        self,
        command: RefreshTokenCommand,
    ) -> RefreshTokenOutputDTO:
        url = f"https://{settings.auth0_domain}/oauth/token"

        payload: dict[str, Any] = {
            "grant_type": "refresh_token",
            "client_id": settings.auth0_client_id,
            "client_secret": settings.auth0_client_secret,
            "refresh_token": command.refresh_token,
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

        if response.status_code in (401, 403):
            raise InvalidCredentialsError(
                "Invalid refresh token."
            )

        if response.is_error:
            response.raise_for_status()

        data: dict[str, Any] = response.json()

        return RefreshTokenOutputDTO(
            access_token=data["access_token"],
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in", 0),
        )