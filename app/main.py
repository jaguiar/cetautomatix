from fastapi import FastAPI, Request
from app.config.settings import settings
from app.config.lifespan import lifespan
from app.config.logging import logger
from app.routers import collections, admin, docsummary, models, cerfas
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse

app = FastAPI(
    title=settings.app_name,
    contact={"email": settings.creator_email},
    lifespan=lifespan,
    docs_url="/swagger",
)


@app.get("/")
async def read_root():
    return {"Ici": "Cétautomatix"}


# Debugging
app.include_router(router=admin.router)
# albert
app.include_router(router=collections.router)
app.include_router(router=models.router)
app.include_router(router=docsummary.router)
app.include_router(router=cerfas.router)


# handling exceptions with Json - should be put in a dedicated file
@app.exception_handler(StarletteHTTPException)
async def default_starlette_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"OMG! An error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(Exception)
async def default_all_exception_handler(request: Request, exc: Exception):
    logger.error(f"OMG! An error!: {repr(exc)}")
    return JSONResponse(
        status_code=500,
        content={"details": "Something terrible just happened"},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)
