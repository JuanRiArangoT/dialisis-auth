from abc import ABC, abstractmethod
from ...domain.entities.user import UserRegistration, UserDocumentMetadata, AuthUser

class IAuthIdentityProvider(ABC):
    """Puerto de salida hacia el proveedor de identidad (Auth0)."""

    @abstractmethod
    def register_user(self, data: UserRegistration) -> AuthUser:
        """Crea el usuario registrando email, password y el campo estándar name."""
        pass

    @abstractmethod
    def update_document_metadata(self, data: UserDocumentMetadata) -> dict:
        """Actualiza el user_metadata con tipo y número de documento."""
        pass