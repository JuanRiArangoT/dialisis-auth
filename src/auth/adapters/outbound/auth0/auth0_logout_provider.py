import httpx

from auth.application.dtos.logout import LogoutCommand
from auth.application.exceptions.authentication import InvalidCredentialsError
from auth.application.exceptions.identity_provider import (
    IdentityProviderUnavailableError,
)
from auth.application.ports.logout_provider import LogoutProviderPort
from auth.infrastructure.config.settings import settings


class Auth0LogoutProvider(LogoutProviderPort):
    async def logout(
        self,
        command: LogoutCommand,
    ) -> None:
        url = f"https://{settings.auth0_domain}/oauth/revoke"

        payload = {
            "client_id": settings.auth0_client_id,
            "client_secret": settings.auth0_client_secret,
            "token": command.refresh_token,
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

        if response.status_code in (400, 401, 403):
            raise InvalidCredentialsError(
                "Invalid refresh token."
            )

        if response.is_error:
            response.raise_for_status()