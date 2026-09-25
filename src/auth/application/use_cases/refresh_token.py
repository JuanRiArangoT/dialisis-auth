from auth.application.dtos.refresh_token import RefreshTokenCommand
from auth.application.dtos.refresh_token_output import RefreshTokenOutputDTO
from auth.application.ports.refresh_token_provider import (
    RefreshTokenProviderPort,
)


class RefreshTokenUseCase:
    def __init__(
        self,
        refresh_token_provider: RefreshTokenProviderPort,
    ) -> None:
        self._refresh_token_provider = refresh_token_provider

    async def execute(
        self,
        command: RefreshTokenCommand,
    ) -> RefreshTokenOutputDTO:
        return await self._refresh_token_provider.refresh(command)