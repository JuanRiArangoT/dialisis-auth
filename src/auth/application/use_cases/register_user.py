from auth.application.dtos.register_user import RegisterUserCommand
from auth.application.dtos.user_output import UserOutputDTO
from auth.application.ports.identity_provider import IdentityProviderPort


class RegisterUserUseCase:
    def __init__(self, identity_provider: IdentityProviderPort) -> None:
        self._identity_provider = identity_provider

    async def execute(
        self,
        command: RegisterUserCommand,
    ) -> UserOutputDTO:
        return await self._identity_provider.register(command)