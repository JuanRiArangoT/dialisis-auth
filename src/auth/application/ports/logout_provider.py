from abc import ABC, abstractmethod

from auth.application.dtos.logout import LogoutCommand


class LogoutProviderPort(ABC):

    @abstractmethod
    async def logout(
        self,
        command: LogoutCommand,
    ) -> None:
        ...