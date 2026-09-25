from unittest.mock import AsyncMock

import pytest

from auth.application.dtos.update_document import UpdateDocumentCommand
from auth.application.use_cases.update_document import UpdateDocumentUseCase


@pytest.mark.asyncio
async def test_update_document() -> None:
    identity_provider = AsyncMock()

    identity_provider.update_document_metadata.return_value = {
        "tipo_documento": "CC",
        "numero_documento": "1234567890",
    }

    use_case = UpdateDocumentUseCase(identity_provider)

    command = UpdateDocumentCommand(
        user_id="auth0|123",
        tipo_documento="CC",
        numero_documento="1234567890",
    )

    result = await use_case.execute(command)

    assert result == {
        "tipo_documento": "CC",
        "numero_documento": "1234567890",
    }

    identity_provider.update_document_metadata.assert_awaited_once_with(
        command
    )