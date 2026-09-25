from unittest.mock import MagicMock

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from auth.adapters.outbound.auth0.auth0_jwt_authenticator import (
    Auth0JWTAuthenticator,
)
from auth.application.exceptions.authentication import AuthenticationError


@pytest.fixture
def rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    return private_key, private_key.public_key()


@pytest.mark.asyncio
async def test_authenticate_rejects_invalid_token() -> None:
    authenticator = Auth0JWTAuthenticator()

    with pytest.raises(AuthenticationError):
        await authenticator.authenticate("invalid-token")


@pytest.mark.asyncio
async def test_authenticate_valid_token(rsa_key_pair) -> None:
    private_key, public_key = rsa_key_pair

    authenticator = Auth0JWTAuthenticator()

    signing_key = MagicMock()
    signing_key.key = public_key

    authenticator._jwks_client.get_signing_key_from_jwt = MagicMock(
        return_value=signing_key,
    )

    token = jwt.encode(
        {
            "sub": "auth0|123",
            "email": "test@example.com",
            "name": "Juan Test",
            "iss": authenticator._issuer,
            "aud": authenticator._audience,
        },
        private_key,
        algorithm="RS256",
    )

    result = await authenticator.authenticate(token)

    assert result.user_id == "auth0|123"
    assert result.email == "test@example.com"
    assert result.full_name == "Juan Test"