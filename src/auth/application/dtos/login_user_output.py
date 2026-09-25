from dataclasses import dataclass


@dataclass(frozen=True)
class LoginUserOutputDTO:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str | None = None
    id_token: str | None = None