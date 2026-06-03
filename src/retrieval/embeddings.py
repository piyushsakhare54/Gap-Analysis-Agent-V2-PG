from __future__ import annotations

import hashlib
import math
import re

import numpy as np


class EmbeddingProvider:
    def __init__(
        self,
        provider: str = "hashing",
        model_name: str = "BAAI/bge-m3",
        dimensions: int = 384,
        warnings: list[str] | None = None,
        allow_fallback: bool = True,
    ) -> None:
        self.provider = provider
        self.model_name = model_name
        self.dimensions = dimensions
        self._model = None
        self._active_provider = provider
        self._warnings = warnings if warnings is not None else []
        if provider == "sentence_transformers":
            self._load_sentence_transformer(allow_fallback)
        elif provider != "hashing":
            message = f"Unknown embedding provider '{provider}'."
            if not allow_fallback:
                raise ValueError(message)
            self._warnings.append(f"{message} Falling back to hashing embeddings.")
            self._active_provider = "hashing"

    @property
    def active_provider(self) -> str:
        return self._active_provider

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if self._active_provider == "sentence_transformers" and self._model is not None:
            vectors = self._model.encode(texts, normalize_embeddings=False)
            return np.asarray(vectors, dtype=float).tolist()
        return [self._hashing_embedding(text) for text in texts]

    def _load_sentence_transformer(self, allow_fallback: bool) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            if not allow_fallback:
                raise RuntimeError("sentence-transformers is not installed.") from exc
            self._warnings.append("sentence-transformers is not installed. Falling back to hashing embeddings.")
            self._active_provider = "hashing"
            return
        try:
            self._model = SentenceTransformer(self.model_name)
        except Exception as exc:
            if not allow_fallback:
                raise
            self._warnings.append(f"Could not load embedding model {self.model_name}: {exc}. Falling back to hashing embeddings.")
            self._active_provider = "hashing"

    def _hashing_embedding(self, text: str) -> list[float]:
        vector = np.zeros(self.dimensions, dtype=float)
        tokens = re.findall(r"[a-z0-9]+", text.lower())
        for token in tokens:
            digest = hashlib.md5(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "little") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign
        norm = math.sqrt(float(np.dot(vector, vector)))
        if norm:
            vector /= norm
        return vector.tolist()

