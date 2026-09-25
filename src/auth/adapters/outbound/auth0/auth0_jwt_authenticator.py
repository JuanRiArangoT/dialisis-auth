from typing import Any

import jwt
from jwt import PyJWKClient

from auth.application.dtos.authenticated_user import AuthenticatedUserDTO
from auth.application.exceptions.authentication import AuthenticationError
from auth.application.ports.authentication import AuthenticationPort
from auth.infrastructure.config.settings import settings


class Auth0JWTAuthenticator(AuthenticationPort):
    def __init__(self) -> None:
        self._issuer = f"https://{settings.auth0_domain}/"
        self._audience = settings.auth0_api_audience
        self._jwks_url = f"{self._issuer}.well-known/jwks.json"

        self._jwks_client = PyJWKClient(self._jwks_url)

    async def authenticate(
        self,
        token: str,
    ) -> AuthenticatedUserDTO:
        try:
            signing_key = self._jwks_client.get_signing_key_from_jwt(token)

            payload: dict[str, Any] = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self._audience,
                issuer=self._issuer,
            )
        except jwt.PyJWTError as exc:
            raise AuthenticationError(
                "Invalid authentication token."
            ) from exc

        return AuthenticatedUserDTO(
            user_id=payload["sub"],
            email=payload.get("email", ""),
            full_name=payload.get("name", ""),
        )