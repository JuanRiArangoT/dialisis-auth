from dataclasses import dataclass


@dataclass(frozen=True)
class RefreshTokenOutputDTO:
    access_token: str
    token_type: str
    expires_in: int