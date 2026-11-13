import numpy as np

from ..config import EMBEDDING_MODEL
from .llm import get_client


def embed(texts: list[str], batch_size: int = 64) -> np.ndarray:
    """Retourne une matrice (n, d) de vecteurs normalisés (cosinus = produit scalaire)."""
    vectors: list[list[float]] = []
    for i in range(0, len(texts), batch_size):
        resp = get_client().embeddings.create(
            model=EMBEDDING_MODEL, input=texts[i:i + batch_size]
        )
        vectors += [d.embedding for d in resp.data]
    arr = np.array(vectors, dtype=np.float32)
    return arr / np.linalg.norm(arr, axis=1, keepdims=True)