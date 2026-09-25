from auth.application.dtos.forgot_password import ForgotPasswordCommand
from auth.application.dtos.forgot_password_output import (
    ForgotPasswordOutputDTO,
)
from auth.application.ports.password_recovery_provider import (
    PasswordRecoveryProviderPort,
)


class ForgotPasswordUseCase:
    def __init__(
        self,
        password_recovery_provider: PasswordRecoveryProviderPort,
    ) -> None:
        self._password_recovery_provider = password_recovery_provider

    async def execute(
        self,
        command: ForgotPasswordCommand,
    ) -> ForgotPasswordOutputDTO:
        return await self._password_recovery_provider.forgot_password(command)