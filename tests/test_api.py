from fastapi.testclient import TestClient

from app.main import app
from app.api import routes

client = TestClient(app)  # sans "with" : le warm-up des embeddings n'est pas lancé
# python -m pytest -q

def test_health():
    assert client.get("/health").status_code == 200


def test_ask_returns_200(monkeypatch):
    fake = {"answer": "ok", "sources": ["dailymed-warfarin.md"], "plan": {},
            "tool_calls": [], "review": {"grounded": True, "issues": []}}
    monkeypatch.setattr(routes, "run_agent", lambda q: fake)
    r = client.post("/ask", json={"question": "What are warfarin contraindications?"})
    assert r.status_code == 200
    assert r.json()["sources"] == ["dailymed-warfarin.md"]


def test_ask_rejects_empty_question():
    assert client.post("/ask", json={"question": ""}).status_code == 422