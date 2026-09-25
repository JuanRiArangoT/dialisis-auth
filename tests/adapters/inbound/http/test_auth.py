from fastapi.testclient import TestClient

from auth.adapters.inbound.http.dependencies.auth import get_current_user
from auth.application.dtos.authenticated_user import AuthenticatedUserDTO
from auth.main import app


def override_get_current_user() -> AuthenticatedUserDTO:
    return AuthenticatedUserDTO(
        user_id="auth0|123",
        email="test@example.com",
        full_name="Juan Test",
    )


app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


def test_get_me() -> None:
    response = client.get("/auth/me")

    assert response.status_code == 200
    assert response.json() == {
        "user_id": "auth0|123",
        "email": "test@example.com",
        "full_name": "Juan Test",
    }