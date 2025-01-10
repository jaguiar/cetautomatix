from fastapi import APIRouter
from app.config.lifespan import clients

router = APIRouter(
    prefix="/models",
    tags=["models"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_albert_available_models():
    models = await clients.albert.fetch_available_models()
    return {"available_models": models}