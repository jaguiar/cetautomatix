from pydantic import BaseModel


class DocumentSummaryRequest(BaseModel):
    document_url: str
    collections_to_use: list[str] | None = None
