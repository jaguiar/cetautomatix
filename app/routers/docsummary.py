from fastapi import APIRouter
from app.config.lifespan import clients
from app.routers.schemas.docsummary import DocumentSummaryRequest
from app.config.logging import logger

router = APIRouter(
    prefix="/summary",
    tags=["documents"],
    responses={500: {"description": "Internal server error"}},
)


@router.post("/")
async def sum_up_document(body: DocumentSummaryRequest):
    """
    Let a user get a summary of a document (for the moment referenced by url, an improvement would be to upload the file).
    One could also specify which collections to use to "enrich" the summary (in order to give some context?)
    and a topic to focus on
    """
    # logger should be put in a middleware probably
    logger.debug(f"Document summary request: {body}")
    answer = await clients.albert.ask_for_document_summary(body.document_url, body.collections_to_use, body.topic_of_interest)
    return {"answer": answer}
