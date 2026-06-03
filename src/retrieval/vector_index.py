from __future__ import annotations

import numpy as np

from src.schemas import Solution


class VectorIndex:
    def __init__(self) -> None:
        self._items: list[Solution] = []
        self._matrix: np.ndarray | None = None

    def add(self, items: list[Solution], vectors: list[list[float]]) -> None:
        if len(items) != len(vectors):
            raise ValueError("items and vectors must have the same length.")
        self._items = list(items)
        if not vectors:
            self._matrix = np.zeros((0, 0), dtype=float)
            return
        matrix = np.asarray(vectors, dtype=float)
        self._matrix = _normalize_rows(matrix)

    def search(self, query_vector: list[float], top_k: int) -> list[tuple[Solution, float]]:
        if top_k <= 0:
            return []
        if self._matrix is None or self._matrix.size == 0:
            return []
        query = _normalize_rows(np.asarray([query_vector], dtype=float))[0]
        scores = self._matrix @ query
        order = np.argsort(scores)[::-1][:top_k]
        return [(self._items[int(index)], float(scores[int(index)])) for index in order]


def _normalize_rows(matrix: np.ndarray) -> np.ndarray:
    if matrix.size == 0:
        return matrix
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return matrix / norms

