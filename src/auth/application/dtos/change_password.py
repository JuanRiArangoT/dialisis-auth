from dataclasses import dataclass


@dataclass(frozen=True)
class ChangePasswordCommand:
    user_id: str
    email: str
    current_password: str
    new_password: str