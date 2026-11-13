from functools import lru_cache

import numpy as np

from ..config import CORPUS_DIR
from ..services.embeddings import embed

CHUNK_SIZE, OVERLAP = 1500, 200


def _sections(text: str) -> list[tuple[str, str]]:
    """Découpe un fichier markdown par titres (#, ##, ###)."""
    title, buf, out = "intro", [], []
    for line in text.splitlines():
        if line.startswith("#"):
            if buf:
                out.append((title, "\n".join(buf).strip()))
                buf = []
            title = line.lstrip("# ").strip()
        else:
            buf.append(line)
    if buf:
        out.append((title, "\n".join(buf).strip()))
    return [(t, b) for t, b in out if b]


def _windows(text: str) -> list[str]:
    if len(text) <= CHUNK_SIZE:
        return [text]
    step = CHUNK_SIZE - OVERLAP
    return [text[i:i + CHUNK_SIZE] for i in range(0, len(text), step)]


class Index:
    def __init__(self) -> None:
        self.chunks: list[dict] = []
        for path in sorted(CORPUS_DIR.glob("*")):
            if path.suffix not in {".md", ".txt"}:
                continue
            for section, body in _sections(path.read_text(encoding="utf-8")):
                for piece in _windows(body):
                    self.chunks.append(
                        {"source": path.name, "section": section, "text": piece}
                    )
        self.matrix = embed(
            [f"{c['source']} | {c['section']}\n{c['text']}" for c in self.chunks]
        )

    def search(self, query: str, k: int = 5, drug: str | None = None) -> list[dict]:
        q = embed([query])[0]
        scores = self.matrix @ q
        if drug:
            mask = np.array([drug.lower() in c["source"].lower() for c in self.chunks])
            scores = np.where(mask, scores, -1.0)
        top = np.argsort(-scores)[:k]
        return [{**self.chunks[i], "score": round(float(scores[i]), 3)}
                for i in top if scores[i] > 0]


@lru_cache(maxsize=1)
def get_index() -> Index:
    return Index()