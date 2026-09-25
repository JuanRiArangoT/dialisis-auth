from abc import ABC, abstractmethod

from auth.application.dtos.change_password import ChangePasswordCommand
from auth.application.dtos.change_password_output import (
    ChangePasswordOutputDTO,
)


class ChangePasswordProviderPort(ABC):

    @abstractmethod
    async def change_password(
        self,
        command: ChangePasswordCommand,
    ) -> ChangePasswordOutputDTO:
        ...