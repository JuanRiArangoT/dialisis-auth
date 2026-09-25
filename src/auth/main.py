# src/auth/main.py
from fastapi import FastAPI

from auth.adapters.inbound.http.exception_handlers import (
    email_not_verified_handler,
    identity_provider_authentication_handler,
    identity_provider_permission_handler,
    identity_provider_rate_limit_handler,
    identity_provider_unavailable_handler,
    identity_provider_user_exists_handler,
    invalid_credentials_handler,
)
from auth.adapters.inbound.http.routes.auth import router as auth_router
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

app = FastAPI(
    title="Servicio de Autenticación - Diálisis",
    description="Microservicio de autenticación con Auth0 y Arquitectura Hexagonal",
    version="1.0.0"
)

# Conectar el adaptador de entrada HTTP
app.include_router(auth_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "auth-microservice"}

app.add_exception_handler(
    IdentityProviderAuthenticationError,
    identity_provider_authentication_handler,
)

app.add_exception_handler(
    IdentityProviderPermissionError,
    identity_provider_permission_handler,
)

app.add_exception_handler(
    IdentityProviderRateLimitError,
    identity_provider_rate_limit_handler,
)

app.add_exception_handler(
    IdentityProviderUserAlreadyExistsError,
    identity_provider_user_exists_handler,
)

app.add_exception_handler(
    IdentityProviderUnavailableError,
    identity_provider_unavailable_handler,
)

app.add_exception_handler(
    InvalidCredentialsError,
    invalid_credentials_handler,
)

app.add_exception_handler(
    EmailNotVerifiedError,
    email_not_verified_handler,
)