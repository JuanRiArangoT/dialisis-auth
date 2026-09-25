from auth.application.dtos.authenticated_user import AuthenticatedUserDTO
from auth.application.ports.authentication import AuthenticationPort
from auth.application.ports.identity_provider import IdentityProviderPort


class AuthenticateUserUseCase:
    def __init__(
        self,
        authentication: AuthenticationPort,
        identity_provider: IdentityProviderPort,
    ) -> None:
        self._authentication = authentication
        self._identity_provider = identity_provider

    async def execute(
        self,
        token: str,
    ) -> AuthenticatedUserDTO:
        authenticated_user = await self._authentication.authenticate(token)

        user = await self._identity_provider.get_user(
            authenticated_user.user_id,
        )

        return AuthenticatedUserDTO(
            user_id=user.user_id,
            email=user.email,
            full_name=user.full_name,
        )