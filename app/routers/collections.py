from fastapi import APIRouter
from app.config.lifespan import clients

router = APIRouter(
    prefix="/collections",
    tags=["collections"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_albert_collections():
    c = await clients.albert.fetch_collections()
    return {"collections": c}