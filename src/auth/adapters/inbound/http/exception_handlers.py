from fastapi import Request
from fastapi.responses import JSONResponse

from auth.application.exceptions.authentication import (
    InvalidCredentialsError,
)
from auth.application.exceptions.email_verification import (
    EmailNotVerifiedError,
)
from auth.application.exceptions.identity_provider import (
    IdentityProviderAuthenticationError,
    IdentityProviderPermissionError,
    IdentityProviderRateLimitError,
    IdentityProviderUnavailableError,
    IdentityProviderUserAlreadyExistsError,
)


async def identity_provider_authentication_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, IdentityProviderAuthenticationError)

    return JSONResponse(
        status_code=502,
        content={
            "detail": "Identity provider authentication failed.",
        },
    )


async def identity_provider_permission_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, IdentityProviderPermissionError)

    return JSONResponse(
        status_code=502,
        content={
            "detail": "Identity provider denied the operation.",
        },
    )


async def identity_provider_rate_limit_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, IdentityProviderRateLimitError)

    return JSONResponse(
        status_code=503,
        content={
            "detail": "Identity provider rate limit exceeded.",
        },
    )


async def identity_provider_user_exists_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, IdentityProviderUserAlreadyExistsError)

    return JSONResponse(
        status_code=409,
        content={
            "detail": "User already exists.",
        },
    )

async def identity_provider_unavailable_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, IdentityProviderUnavailableError)

    return JSONResponse(
        status_code=503,
        content={
            "detail": "Identity provider is unavailable.",
        },
    )

async def invalid_credentials_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, InvalidCredentialsError)

    return JSONResponse(
        status_code=401,
        content={
            "detail": "Invalid credentials.",
        },
    )

async def email_not_verified_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, EmailNotVerifiedError)

    return JSONResponse(
        status_code=403,
        content={
            "detail": str(exc),
        },
    )