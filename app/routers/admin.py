# This router should probably be secured somehow since it as endpoints for debugging purposes and maybe sensitive information
from fastapi import APIRouter
from app.config.settings import settings
from app.config.lifespan import clients

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}, 404: {"description": "Not found"}},
)

@router.get("/settings")
async def read_settings():
    return settings

@router.get("/clients")
async def read_clients():
    clients_list = clients.get_clients_list()
    return {"collections": clients_list}