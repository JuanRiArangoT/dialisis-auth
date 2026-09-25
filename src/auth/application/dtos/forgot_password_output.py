from dataclasses import dataclass


@dataclass(frozen=True)
class ForgotPasswordOutputDTO:
    message: str