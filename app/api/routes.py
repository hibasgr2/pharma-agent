import logging

from fastapi import APIRouter, HTTPException

from ..agent.graph import run_agent
from ..schemas.models import AskRequest, AskResponse

log = logging.getLogger("pharma")
router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    try:
        return run_agent(req.question)
    except Exception as e:
        log.exception("agent failure")
        raise HTTPException(status_code=500, detail=str(e))