from fastapi import APIRouter
from app.config.lifespan import clients
from app.routers.schemas.docsummary import DocumentSummaryRequest

router = APIRouter(
    prefix="/summary",
    tags=["documents"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def sum_up_document(body: DocumentSummaryRequest):
    """
    Let a user get a summary of a document (for the moment referenced by url, an improvement would be to upload the file).
    One could also specify which collections to use to "enrich" the summary (in order to give some context?)
    """
    answer = await clients.albert.ask_for_document_summary(body.document_url, body.collections_to_use)
    return {"answer": answer}