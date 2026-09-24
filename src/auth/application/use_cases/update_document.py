from auth.application.dtos.update_document import UpdateDocumentCommand
from auth.application.ports.identity_provider import IdentityProviderPort


class UpdateDocumentUseCase:
    def __init__(self, identity_provider: IdentityProviderPort) -> None:
        self._identity_provider = identity_provider

    async def execute(
        self,
        command: UpdateDocumentCommand,
    ) -> dict[str, object]:
        return await self._identity_provider.update_document_metadata(command)