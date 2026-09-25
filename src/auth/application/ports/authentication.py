from abc import ABC, abstractmethod

from auth.application.dtos.authenticated_user import AuthenticatedUserDTO


class AuthenticationPort(ABC):

    @abstractmethod
    async def authenticate(
        self,
        token: str,
    ) -> AuthenticatedUserDTO:
        ...