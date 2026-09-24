from dataclasses import dataclass


@dataclass(frozen=True)
class UserOutputDTO:
    user_id: str
    email: str
    full_name: str