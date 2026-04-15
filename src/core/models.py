from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class UploadPayload:
    id: str
    file_bytes: bytes
    filename: str
    content_type: str
    filepath: str | None = None


class DeleteRequest(BaseModel):
    """Modelo para requisição de deleção de documentos."""

    ids: list[str]
