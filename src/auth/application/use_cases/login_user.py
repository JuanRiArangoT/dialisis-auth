from auth.application.dtos.login_user import LoginUserCommand
from auth.application.dtos.login_user_output import LoginUserOutputDTO
from auth.application.ports.login_provider import LoginProviderPort


class LoginUserUseCase:
    def __init__(self, login_provider: LoginProviderPort) -> None:
        self._login_provider = login_provider

    async def execute(
        self,
        command: LoginUserCommand,
    ) -> LoginUserOutputDTO:
        return await self._login_provider.login(command)