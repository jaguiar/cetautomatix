from fastapi import APIRouter
from app.config.lifespan import clients

router = APIRouter(
    prefix="/cerfas",
    tags=["cerfas"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_cerfa_of_interest_from_albert():
    #c = await clients.albert.fetch_collections()
    #return {"cerfas": c}
    raise HTTPException(status_code=404, detail="Not implemented yet")