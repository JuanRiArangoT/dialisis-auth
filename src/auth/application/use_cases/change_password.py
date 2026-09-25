from auth.application.dtos.change_password import ChangePasswordCommand
from auth.application.dtos.change_password_output import (
    ChangePasswordOutputDTO,
)
from auth.application.ports.change_password_provider import (
    ChangePasswordProviderPort,
)


class ChangePasswordUseCase:
    def __init__(
        self,
        change_password_provider: ChangePasswordProviderPort,
    ) -> None:
        self._change_password_provider = change_password_provider

    async def execute(
        self,
        command: ChangePasswordCommand,
    ) -> ChangePasswordOutputDTO:
        return await self._change_password_provider.change_password(command)