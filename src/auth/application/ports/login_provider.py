from abc import ABC, abstractmethod

from auth.application.dtos.login_user import LoginUserCommand
from auth.application.dtos.login_user_output import LoginUserOutputDTO


class LoginProviderPort(ABC):

    @abstractmethod
    async def login(
        self,
        command: LoginUserCommand,
    ) -> LoginUserOutputDTO:
        ...