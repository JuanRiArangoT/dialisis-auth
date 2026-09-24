# src/auth/application/ports/authentication.py
from abc import ABC, abstractmethod
from typing import Any

from ..dtos import RegisterUserCommand, UpdateDocumentCommand, UserOutputDTO


class AuthenticationPort(ABC):
    @abstractmethod
    async def register(self, command: RegisterUserCommand) -> UserOutputDTO:
        """Crea el usuario en el proveedor de identidad asignando el nombre al campo 'name'."""

    @abstractmethod
    async def update_document_metadata(self, command: UpdateDocumentCommand) -> dict[str, Any]:
        """Actualiza la metadata del perfil en el proveedor de identidad."""
