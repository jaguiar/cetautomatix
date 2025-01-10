from pydantic import BaseModel


### FIXME we should definitely validate fields to avoid "weird injections"
class DocumentSummaryRequest(BaseModel):
    document_url: str
    collections_to_use: list[str] = []
    topic_of_interest: str | None = None
