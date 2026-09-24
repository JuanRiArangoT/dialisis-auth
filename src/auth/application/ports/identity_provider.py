from abc import ABC, abstractmethod

from auth.application.dtos.register_user import RegisterUserCommand
from auth.application.dtos.update_document import UpdateDocumentCommand
from auth.application.dtos.user_output import UserOutputDTO


class IdentityProviderPort(ABC):

    @abstractmethod
    async def register(
        self,
        command: RegisterUserCommand,
    ) -> UserOutputDTO:
        ...

    @abstractmethod
    async def update_document_metadata(
        self,
        command: UpdateDocumentCommand,
    ) -> dict[str, object]:
        ...