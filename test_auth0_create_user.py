import asyncio

from auth.adapters.outbound.auth0.auth0_identity_provider import (
    Auth0IdentityProvider,
)
from auth.adapters.outbound.auth0.auth0_management_client import (
    Auth0ManagementClient,
)
from auth.application.dtos.register_user import RegisterUserCommand


async def main() -> None:
    client = Auth0ManagementClient()
    identity_provider = Auth0IdentityProvider(client)

    command = RegisterUserCommand(
        email="prueba.dialisis@example.com",
        password="TestPassword123!",
        full_name="Usuario Prueba Dialisis",
    )

    result = await identity_provider.register(command)

    print("USUARIO CREADO")
    print("USER ID:", result.user_id)
    print("EMAIL:", result.email)
    print("NOMBRE:", result.full_name)


asyncio.run(main())