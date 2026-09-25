from typing import Annotated

from fastapi import APIRouter, Depends

from auth.adapters.inbound.http.dependencies.auth import (
    get_current_user,
    get_register_user_use_case,
    get_update_document_use_case,
)
from auth.adapters.inbound.http.schemas.register import RegisterUserRequest
from auth.adapters.inbound.http.schemas.update_document import (
    UpdateDocumentRequest,
)
from auth.adapters.inbound.http.schemas.user import UserResponse
from auth.application.dtos.authenticated_user import AuthenticatedUserDTO
from auth.application.dtos.register_user import RegisterUserCommand
from auth.application.dtos.update_document import UpdateDocumentCommand
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