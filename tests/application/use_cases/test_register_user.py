from unittest.mock import AsyncMock

import pytest

from auth.application.dtos.register_user import RegisterUserCommand
from auth.application.dtos.user_output import UserOutputDTO
from auth.application.use_cases.register_user import RegisterUserUseCase


@pytest.mark.asyncio
async def test_register_user() -> None:
    identity_provider = AsyncMock()

    identity_provider.register.return_value = UserOutputDTO(
        user_id="auth0|123",
        email="test@example.com",
        full_name="Juan Test",
    )

    use_case = RegisterUserUseCase(identity_provider)

    command = RegisterUserCommand(
        email="test@example.com",
        password="Password123!",
        full_name="Juan Test",
    )

    result = await use_case.execute(command)

    assert result.user_id == "auth0|123"
    assert result.email == "test@example.com"
    assert result.full_name == "Juan Test"

    identity_provider.register.assert_awaited_once_with(command)