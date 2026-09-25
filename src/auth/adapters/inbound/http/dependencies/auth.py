from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth.adapters.outbound.auth0.auth0_identity_provider import (
    Auth0IdentityProvider,
)
from auth.adapters.outbound.auth0.auth0_jwt_authenticator import (
    Auth0JWTAuthenticator,
)
from auth.adapters.outbound.auth0.auth0_management_client import (
    Auth0ManagementClient,
)
from auth.application.dtos.authenticated_user import AuthenticatedUserDTO
from auth.application.exceptions.authentication import AuthenticationError
from auth.application.use_cases.authenticate_user import (
    AuthenticateUserUseCase,
)
from auth.application.use_cases.register_user import RegisterUserUseCase
from auth.application.use_cases.update_document import UpdateDocumentUseCase

security = HTTPBearer()


def get_authentication_use_case() -> AuthenticateUserUseCase:
    authentication = Auth0JWTAuthenticator()
    return AuthenticateUserUseCase(authentication)


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(security),
    ],
    use_case: Annotated[
        AuthenticateUserUseCase,
        Depends(get_authentication_use_case),
    ],
) -> AuthenticatedUserDTO:
    try:
        return await use_case.execute(credentials.credentials)
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
        ) from exc


def get_register_user_use_case() -> RegisterUserUseCase:
    client = Auth0ManagementClient()
    identity_provider = Auth0IdentityProvider(client)

    return RegisterUserUseCase(identity_provider)


def get_update_document_use_case() -> UpdateDocumentUseCase:
    client = Auth0ManagementClient()
    identity_provider = Auth0IdentityProvider(client)

    return UpdateDocumentUseCase(identity_provider)