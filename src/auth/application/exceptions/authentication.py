class AuthenticationError(Exception):
    """Raised when authentication fails."""

class InvalidCredentialsError(AuthenticationError):
    """Raised when the provided credentials are invalid."""