from auth.application.dtos.authenticated_user import AuthenticatedUserDTO
from auth.application.ports.authentication import AuthenticationPort


class AuthenticateUserUseCase:
    def __init__(
        self,
        authentication: AuthenticationPort,
    ) -> None:
        self._authentication = authentication

    async def execute(
        self,
        token: str,
    ) -> AuthenticatedUserDTO:
        return await self._authentication.authenticate(token)