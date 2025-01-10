from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core import ClientsManager
from app.config.settings import settings
from app.config.logging import logger

clients = ClientsManager(settings=settings)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event to initialize clients (models API and external systems clients)."""

    logger.debug("Initializing clients...")
    clients.set()

    yield

    logger.debug("Shutdowning clients...")
    await clients.clear()