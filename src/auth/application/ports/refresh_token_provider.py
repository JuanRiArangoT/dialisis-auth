from abc import ABC, abstractmethod

from auth.application.dtos.refresh_token import RefreshTokenCommand
from auth.application.dtos.refresh_token_output import RefreshTokenOutputDTO


class RefreshTokenProviderPort(ABC):

    @abstractmethod
    async def refresh(
        self,
        command: RefreshTokenCommand,
    ) -> RefreshTokenOutputDTO:
        ...