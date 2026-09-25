from typing import Any

import httpx

from auth.application.dtos.forgot_password import ForgotPasswordCommand
from auth.application.dtos.forgot_password_output import (
    ForgotPasswordOutputDTO,
)
from auth.application.exceptions.identity_provider import (
    IdentityProviderUnavailableError,
)
from auth.application.ports.password_recovery_provider import (
    PasswordRecoveryProviderPort,
)
from auth.infrastructure.config.settings import settings


class Auth0PasswordRecoveryProvider(PasswordRecoveryProviderPort):
    async def forgot_password(
        self,
        command: ForgotPasswordCommand,
    ) -> ForgotPasswordOutputDTO:
        url = f"https://{settings.auth0_domain}/dbconnections/change_password"

        payload: dict[str, Any] = {
            "client_id": settings.auth0_client_id,
            "email": command.email,
            "connection": settings.auth0_db_connection,
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
            response.raise_for_status()

        return ForgotPasswordOutputDTO(
            message="Password recovery email sent."
        )