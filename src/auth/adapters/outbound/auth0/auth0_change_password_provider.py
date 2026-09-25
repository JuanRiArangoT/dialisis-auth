from typing import Any

import httpx

from auth.adapters.outbound.auth0.auth0_management_client import (
    Auth0ManagementClient,
)
from auth.application.dtos.change_password import ChangePasswordCommand
from auth.application.dtos.change_password_output import (
    ChangePasswordOutputDTO,
)
from auth.application.exceptions.authentication import (
    InvalidCredentialsError,
)
from auth.application.exceptions.identity_provider import (
    IdentityProviderUnavailableError,
)
from auth.application.ports.change_password_provider import (
    ChangePasswordProviderPort,
)
from auth.infrastructure.config.settings import settings


class Auth0ChangePasswordProvider(ChangePasswordProviderPort):
    def __init__(
        self,
        management_client: Auth0ManagementClient,
    ) -> None:
        self._management_client = management_client

    async def change_password(
        self,
        command: ChangePasswordCommand,
    ) -> ChangePasswordOutputDTO:
        token_url = f"https://{settings.auth0_domain}/oauth/token"

        payload: dict[str, Any] = {
            "grant_type": (
                "http://auth0.com/oauth/grant-type/password-realm"
            ),
            "username": command.email,
            "password": command.current_password,
            "audience": settings.auth0_api_audience,
            "client_id": settings.auth0_client_id,
            "client_secret": settings.auth0_client_secret,
            "realm": settings.auth0_db_connection,
            "scope": "openid profile email",
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    token_url,
                    json=payload,
                    timeout=10.0,
                )
        except httpx.RequestError as exc:
            raise IdentityProviderUnavailableError(
                "Identity provider is unavailable."
            ) from exc

        if response.status_code in (400, 401):
            raise InvalidCredentialsError(
                "Invalid current password."
            )

        if response.is_error:
            response.raise_for_status()

        await self._management_client.update_user_password(
            user_id=command.user_id,
            password=command.new_password,
        )

        return ChangePasswordOutputDTO()