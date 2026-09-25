from typing import Any

import httpx

from auth.application.dtos.login_user import LoginUserCommand
from auth.application.dtos.login_user_output import LoginUserOutputDTO
from auth.application.exceptions.authentication import (
    InvalidCredentialsError,
)
from auth.application.exceptions.email_verification import (
    EmailNotVerifiedError,
)
from auth.application.exceptions.identity_provider import (
    IdentityProviderUnavailableError,
)
from auth.application.ports.login_provider import LoginProviderPort
from auth.infrastructure.config.settings import settings


class Auth0LoginProvider(LoginProviderPort):
    async def login(
        self,
        command: LoginUserCommand,
    ) -> LoginUserOutputDTO:
        url = f"https://{settings.auth0_domain}/oauth/token"

        payload: dict[str, Any] = {
            "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
            "username": command.email,
            "password": command.password,
            "audience": settings.auth0_api_audience,
            "client_id": settings.auth0_client_id,
            "client_secret": settings.auth0_client_secret,
            "realm": settings.auth0_db_connection,
            "scope": "openid profile email offline_access",
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
                "Invalid credentials."
            )

        if response.status_code == 500:
            data: dict[str, Any] = response.json()

            if data.get("error") == "access_denied":
                raise EmailNotVerifiedError(
                    data.get(
                        "error_description",
                        "Access denied.",
                    )
                )

        if response.is_error:
            response.raise_for_status()

        data: dict[str, Any] = response.json()

        return LoginUserOutputDTO(
            access_token=data["access_token"],
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in", 0),
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
        )