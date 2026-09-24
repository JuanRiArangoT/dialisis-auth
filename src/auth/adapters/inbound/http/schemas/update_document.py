from pydantic import BaseModel, Field


class UpdateDocumentRequest(BaseModel):
    tipo_documento: str = Field(min_length=1, max_length=30)
    numero_documento: str = Field(min_length=1, max_length=50)