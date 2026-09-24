import asyncio

from auth.adapters.outbound.auth0.auth0_identity_provider import (
    Auth0IdentityProvider,
)
from auth.adapters.outbound.auth0.auth0_management_client import (
    Auth0ManagementClient,
)
from auth.application.dtos.update_document import UpdateDocumentCommand


async def main() -> None:
    client = Auth0ManagementClient()
    identity_provider = Auth0IdentityProvider(client)

    command = UpdateDocumentCommand(
        user_id="auth0|6ab5aa196c419f5d813808c5",
        tipo_documento="CC",
        numero_documento="1234567890",
    )

    result = await identity_provider.update_document_metadata(command)

    print("METADATA ACTUALIZADA")
    print(result)


asyncio.run(main())