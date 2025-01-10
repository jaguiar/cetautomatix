from typing import Union
from fastapi import FastAPI
from app.config.settings import settings
from app.config.lifespan import lifespan
from app.routers import collections, admin, docsummary, models

app = FastAPI(
    title=settings.app_name,
    contact={"email": settings.creator_email},
    lifespan=lifespan,
    docs_url="/swagger",
)


@app.get("/")
async def read_root():
    return {"Ici": "Cétautomatix"}


@app.get("/cerfas/{cerfa_id}")
async def read_cerfa(cerfa_id: int, q: Union[str, None] = None):
    return {"cerfa_id": cerfa_id, "q": q}


# Debugging
app.include_router(router=admin.router)
# albert
app.include_router(router=collections.router)
app.include_router(router=models.router)
app.include_router(router=docsummary.router)
