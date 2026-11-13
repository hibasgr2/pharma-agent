import json
import re
from functools import lru_cache

from openai import OpenAI

from ..config import CHAT_MODEL


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    """Client créé à la demande : lit OPENAI_API_KEY / OPENAI_BASE_URL."""
    return OpenAI()


def chat(messages: list[dict], **kwargs):
    return get_client().chat.completions.create(
        model=CHAT_MODEL, messages=messages, **kwargs
    )


def parse_json(text: str | None) -> dict:
    """Extrait un objet JSON d'une réponse LLM (tolère les ```json)."""
    m = re.search(r"\{.*\}", text or "", re.S)
    try:
        return json.loads(m.group(0)) if m else {}
    except json.JSONDecodeError:
        return {}