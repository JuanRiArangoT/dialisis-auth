from auth.adapters.outbound.auth0.auth0_identity_provider import (
    Auth0IdentityProvider,
)
from auth.adapters.outbound.auth0.auth0_management_client import (
    Auth0ManagementClient,
)
from auth.application.ports.identity_provider import IdentityProviderPort
from auth.application.use_cases.register_user import RegisterUserUseCase
from auth.application.use_cases.update_document import UpdateDocumentUseCase


def get_identity_provider() -> IdentityProviderPort:
    client = Auth0ManagementClient()

    return Auth0IdentityProvider(client)


def get_register_user_use_case() -> RegisterUserUseCase:
    identity_provider = get_identity_provider()

    return RegisterUserUseCase(identity_provider)


def get_update_document_use_case() -> UpdateDocumentUseCase:
    identity_provider = get_identity_provider()

    return UpdateDocumentUseCase(identity_provider)