import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .agent.retriever import get_index
from .api.routes import router
from .config import FRONTEND_DIR

log = logging.getLogger("pharma")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        get_index()  # préchauffe les embeddings
    except Exception as e:  # /health reste 200 ; l'index se reconstruira au 1er /ask
        log.warning("Index warm-up failed: %s", e)
    yield


app = FastAPI(title="Pharma Agent", lifespan=lifespan)
app.include_router(router)
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")