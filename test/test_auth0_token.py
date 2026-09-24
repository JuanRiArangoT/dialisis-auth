import asyncio

from auth.adapters.outbound.auth0.auth0_management_client import (
    Auth0ManagementClient,
)


async def main() -> None:
    client = Auth0ManagementClient()

    token = await client._get_management_token()

    print("TOKEN OBTENIDO:", bool(token))
    print("LONGITUD:", len(token))


asyncio.run(main())