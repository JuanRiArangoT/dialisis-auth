from typing import Any

from auth.adapters.outbound.auth0.auth0_management_client import (
    Auth0ManagementClient,
)
from auth.application.dtos.register_user import RegisterUserCommand
from auth.application.dtos.update_document import UpdateDocumentCommand
from auth.application.dtos.user_output import UserOutputDTO
from auth.application.ports.identity_provider import IdentityProviderPort


class Auth0IdentityProvider(IdentityProviderPort):
    def __init__(
        self,
        client: Auth0ManagementClient,
    ) -> None:
        self._client = client

    async def register(
        self,
        command: RegisterUserCommand,
    ) -> UserOutputDTO:
        data = await self._client.create_user(
            email=command.email,
            password=command.password,
            full_name=command.full_name,
        )

        return UserOutputDTO(
            user_id=data["user_id"],
            email=data["email"],
            full_name=data.get("name", ""),
        )

    async def update_document_metadata(
        self,
        command: UpdateDocumentCommand,
    ) -> dict[str, object]:
        data: dict[str, Any] = await self._client.update_user_metadata(
            user_id=command.user_id,
            tipo_documento=command.tipo_documento,
            numero_documento=command.numero_documento,
        )

        return data

    async def get_user(
        self,
        user_id: str,
    ) -> UserOutputDTO:
        data = await self._client.get_user(user_id)

        return UserOutputDTO(
            user_id=data["user_id"],
            email=data.get("email", ""),
            full_name=data.get("name", ""),
        )