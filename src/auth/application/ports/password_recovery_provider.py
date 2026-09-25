from abc import ABC, abstractmethod

from auth.application.dtos.forgot_password import ForgotPasswordCommand
from auth.application.dtos.forgot_password_output import (
    ForgotPasswordOutputDTO,
)


class PasswordRecoveryProviderPort(ABC):

    @abstractmethod
    async def forgot_password(
        self,
        command: ForgotPasswordCommand,
    ) -> ForgotPasswordOutputDTO:
        ...