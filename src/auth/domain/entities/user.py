from dataclasses import dataclass
from typing import Optional

@dataclass
class UserRegistration:
    email: str
    password: str
    full_name: str

@dataclass
class UserDocumentMetadata:
    user_id: str          # Identificador auth0_id / sub (ej. "auth0|123456")
    tipo_documento: str   # CC, TI, CE, Pasaporte
    numero_documento: str

@dataclass
class AuthUser:
    user_id: str
    email: str
    name: str
    user_metadata: Optional[dict] = None