from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticatedUserDTO:
    user_id: str
    email: str
    full_name: str