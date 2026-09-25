class IdentityProviderError(Exception):
    """Base exception for identity provider errors."""


class IdentityProviderAuthenticationError(IdentityProviderError):
    """Raised when authentication with the identity provider fails."""


class IdentityProviderPermissionError(IdentityProviderError):
    """Raised when the identity provider denies an operation."""


class IdentityProviderRateLimitError(IdentityProviderError):
    """Raised when the identity provider rate-limits a request."""


class IdentityProviderUserAlreadyExistsError(IdentityProviderError):
    """Raised when trying to create an existing user."""

class IdentityProviderUnavailableError(IdentityProviderError):
    """Raised when the identity provider is unavailable."""