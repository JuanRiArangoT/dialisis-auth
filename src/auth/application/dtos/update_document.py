from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateDocumentCommand:
    user_id: str
    tipo_documento: str
    numero_documento: str