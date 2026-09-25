from typing import Annotated

from fastapi import APIRouter, Depends

from auth.adapters.inbound.http.dependencies.auth import (
    get_change_password_use_case,
    get_current_user,
    get_forgot_password_use_case,
    get_login_user_use_case,
    get_logout_use_case,
    get_refresh_token_use_case,
    get_register_user_use_case,
    get_update_document_use_case,
)
from auth.adapters.inbound.http.schemas.change_password import (
    ChangePasswordRequest,
)
from auth.adapters.inbound.http.schemas.forgot_password import (
    ForgotPasswordRequest,
)
from auth.adapters.inbound.http.schemas.login import LoginUserRequest
from auth.adapters.inbound.http.schemas.logout import LogoutRequest
from auth.adapters.inbound.http.schemas.refresh_token import (
    RefreshTokenRequest,
)
from auth.adapters.inbound.http.schemas.register import RegisterUserRequest
from auth.adapters.inbound.http.schemas.update_document import (
    UpdateDocumentRequest,
)
from auth.adapters.inbound.http.schemas.user import UserResponse
from auth.application.dtos.authenticated_user import AuthenticatedUserDTO
from auth.application.dtos.change_password import ChangePasswordCommand
from auth.application.dtos.forgot_password import ForgotPasswordCommand
from auth.application.dtos.login_user import LoginUserCommand
from auth.application.dtos.logout import LogoutCommand
from auth.application.dtos.refresh_token import RefreshTokenCommand
from auth.application.dtos.register_user import RegisterUserCommand
from auth.application.dtos.update_document import UpdateDocumentCommand
from auth.application.use_cases.change_password import ChangePasswordUseCase
from auth.application.use_cases.forgot_password import ForgotPasswordUseCase
from auth.application.use_cases.login_user import LoginUserUseCase
from auth.application.use_cases.logout import LogoutUseCase
from auth.application.use_cases.refresh_token import RefreshTokenUseCase
from auth.application.use_cases.register_user import RegisterUserUseCase
from auth.application.use_cases.update_document import UpdateDocumentUseCase

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
)
async def register(
    request: RegisterUserRequest,
    use_case: Annotated[
        RegisterUserUseCase,
        Depends(get_register_user_use_case),
    ],
) -> UserResponse:
    command = RegisterUserCommand(
        email=request.email,
        password=request.password,
        full_name=request.full_name,
    )

    result = await use_case.execute(command)

    return UserResponse(
        user_id=result.user_id,
        email=result.email,
        full_name=result.full_name,
    )

@router.patch(
    "/users/{user_id}/document",
)
async def update_document(
    user_id: str,
    request: UpdateDocumentRequest,
    use_case: Annotated[
        UpdateDocumentUseCase,
        Depends(get_update_document_use_case),
    ],
) -> dict[str, object]:
    command = UpdateDocumentCommand(
        user_id=user_id,
        tipo_documento=request.tipo_documento,
        numero_documento=request.numero_documento,
    )

    return await use_case.execute(command)

@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user: AuthenticatedUserDTO = Depends(get_current_user), # noqa: B008
) -> UserResponse:
    return UserResponse(
        user_id=current_user.user_id,
        email=current_user.email,
        full_name=current_user.full_name,
    )

@router.post(
    "/login",
)
async def login(
    request: LoginUserRequest,
    use_case: Annotated[
        LoginUserUseCase,
        Depends(get_login_user_use_case),
    ],
) -> dict[str, object]:
    command = LoginUserCommand(
        email=request.email,
        password=request.password,
    )

    result = await use_case.execute(command)

    return {
        "access_token": result.access_token,
        "token_type": result.token_type,
        "expires_in": result.expires_in,
        "refresh_token": result.refresh_token,
        "id_token": result.id_token,
    }

@router.post(
    "/refresh",
)
async def refresh_token(
    request: RefreshTokenRequest,
    use_case: Annotated[
        RefreshTokenUseCase,
        Depends(get_refresh_token_use_case),
    ],
) -> dict[str, object]:
    command = RefreshTokenCommand(
        refresh_token=request.refresh_token,
    )

    result = await use_case.execute(command)

    return {
        "access_token": result.access_token,
        "token_type": result.token_type,
        "expires_in": result.expires_in,
    }

@router.post(
    "/logout",
)
async def logout(
    request: LogoutRequest,
    use_case: Annotated[
        LogoutUseCase,
        Depends(get_logout_use_case),
    ],
) -> dict[str, str]:
    command = LogoutCommand(
        refresh_token=request.refresh_token,
    )

    await use_case.execute(command)

    return {
        "message": "Logout successful.",
    }

@router.post(
    "/password/forgot",
)
async def forgot_password(
    request: ForgotPasswordRequest,
    use_case: Annotated[
        ForgotPasswordUseCase,
        Depends(get_forgot_password_use_case),
    ],
) -> dict[str, str]:
    command = ForgotPasswordCommand(
        email=request.email,
    )

    result = await use_case.execute(command)

    return {
        "message": result.message,
    }

@router.post(
    "/password/change",
)
async def change_password(
    request: ChangePasswordRequest,
    current_user: AuthenticatedUserDTO = Depends(get_current_user),  # noqa: B008
    use_case: Annotated[
        ChangePasswordUseCase,
        Depends(get_change_password_use_case),
    ] = None,
) -> dict[str, str]:
    command = ChangePasswordCommand(
        user_id=current_user.user_id,
        email=current_user.email,
        current_password=request.current_password,
        new_password=request.new_password,
    )

    await use_case.execute(command)

    return {
        "message": "Password changed successfully.",
    }