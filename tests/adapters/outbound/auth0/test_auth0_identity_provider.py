from unittest.mock import AsyncMock

import pytest

from auth.adapters.outbound.auth0.auth0_identity_provider import (
    Auth0IdentityProvider,
)
from auth.application.dtos.register_user import RegisterUserCommand
from auth.application.dtos.update_document import UpdateDocumentCommand
from auth.application.dtos.user_output import UserOutputDTO


@pytest.mark.asyncio
async def test_register() -> None:
    client = AsyncMock()

    client.create_user.return_value = {
        "user_id": "auth0|123",
        "email": "test@example.com",
        "name": "Juan Test",
    }

    identity_provider = Auth0IdentityProvider(client)

    command = RegisterUserCommand(
        email="test@example.com",
        password="Password123!",
        full_name="Juan Test",
    )

    result = await identity_provider.register(command)

    assert result.user_id == "auth0|123"
    assert result.email == "test@example.com"
    assert result.full_name == "Juan Test"

    client.create_user.assert_awaited_once_with(
        email="test@example.com",
        password="Password123!",
        full_name="Juan Test",
    )


@pytest.mark.asyncio
async def test_update_document_metadata() -> None:
    client = AsyncMock()

    client.update_user_metadata.return_value = {
        "tipo_documento": "CC",
        "numero_documento": "1234567890",
    }

    identity_provider = Auth0IdentityProvider(client)

    command = UpdateDocumentCommand(
        user_id="auth0|123",
        tipo_documento="CC",
        numero_documento="1234567890",
    )

    result = await identity_provider.update_document_metadata(command)

    assert result == {
        "tipo_documento": "CC",
        "numero_documento": "1234567890",
    }

    client.update_user_metadata.assert_awaited_once_with(
        user_id="auth0|123",
        tipo_documento="CC",
        numero_documento="1234567890",
    )

async def get_user(
    self,
    user_id: str,
) -> UserOutputDTO:
    data = await self._management_client.get_user(user_id)

    return UserOutputDTO(
        user_id=data["user_id"],
        email=data.get("email", ""),
        full_name=data.get("name", ""),
    )