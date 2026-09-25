from auth.application.dtos.logout import LogoutCommand
from auth.application.ports.logout_provider import LogoutProviderPort


class LogoutUseCase:
    def __init__(
        self,
        logout_provider: LogoutProviderPort,
    ) -> None:
        self._logout_provider = logout_provider

    async def execute(
        self,
        command: LogoutCommand,
    ) -> None:
        await self._logout_provider.logout(command)