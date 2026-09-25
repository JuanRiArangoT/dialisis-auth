from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth.adapters.outbound.auth0.auth0_change_password_provider import (
    Auth0ChangePasswordProvider,
)
from auth.adapters.outbound.auth0.auth0_identity_provider import (
    Auth0IdentityProvider,
)
from auth.adapters.outbound.auth0.auth0_jwt_authenticator import (
    Auth0JWTAuthenticator,
)
from auth.adapters.outbound.auth0.auth0_login_provider import (
    Auth0LoginProvider,
)
from auth.adapters.outbound.auth0.auth0_logout_provider import (
    Auth0LogoutProvider,
)
from auth.adapters.outbound.auth0.auth0_management_client import (
    Auth0ManagementClient,
)
from auth.adapters.outbound.auth0.auth0_password_recovery_provider import (
    Auth0PasswordRecoveryProvider,
)
from auth.adapters.outbound.auth0.auth0_refresh_token_provider import (
    Auth0RefreshTokenProvider,
)
from auth.application.dtos.authenticated_user import AuthenticatedUserDTO
from auth.application.exceptions.authentication import AuthenticationError
from auth.application.use_cases.authenticate_user import (
    AuthenticateUserUseCase,
)
from auth.application.use_cases.change_password import (
    ChangePasswordUseCase,
)
from auth.application.use_cases.forgot_password import (
    ForgotPasswordUseCase,
)
from auth.application.use_cases.login_user import LoginUserUseCase
from auth.application.use_cases.logout import LogoutUseCase
from auth.application.use_cases.refresh_token import RefreshTokenUseCase
from auth.application.use_cases.register_user import RegisterUserUseCase
from auth.application.use_cases.update_document import UpdateDocumentUseCase

security = HTTPBearer()


def get_authentication_use_case() -> AuthenticateUserUseCase:
    authentication = Auth0JWTAuthenticator()

    client = Auth0ManagementClient()
    identity_provider = Auth0IdentityProvider(client)

    return AuthenticateUserUseCase(
        authentication,
        identity_provider,
    )


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

def get_login_user_use_case() -> LoginUserUseCase:
    login_provider = Auth0LoginProvider()

    return LoginUserUseCase(login_provider)

def get_refresh_token_use_case() -> RefreshTokenUseCase:
    refresh_token_provider = Auth0RefreshTokenProvider()

    return RefreshTokenUseCase(refresh_token_provider)

def get_logout_use_case() -> LogoutUseCase:
    logout_provider = Auth0LogoutProvider()

    return LogoutUseCase(logout_provider)

def get_forgot_password_use_case() -> ForgotPasswordUseCase:
    password_recovery_provider = Auth0PasswordRecoveryProvider()

    return ForgotPasswordUseCase(password_recovery_provider)

def get_change_password_use_case() -> ChangePasswordUseCase:
    management_client = Auth0ManagementClient()

    change_password_provider = Auth0ChangePasswordProvider(
        management_client,
    )

    return ChangePasswordUseCase(change_password_provider)