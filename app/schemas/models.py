from typing import Any, TypedDict

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=3)


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    plan: dict
    tool_calls: list[dict]
    review: dict


class AgentState(TypedDict):
    """État partagé entre les nœuds du graphe LangGraph."""
    question: str
    plan: dict
    messages: list[dict[str, Any]]
    evidence: list[str]
    sources: list[str]
    trace: list[dict]
    steps: int
    draft: str
    review: dict
    answer: str