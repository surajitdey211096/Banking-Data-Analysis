
import json
from pathlib import Path

import faiss
import numpy as np


class VectorStore:
    def __init__(self, storage_dir: str = "data/rag_index"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.index_path = self.storage_dir / "banking.index"
        self.documents_path = self.storage_dir / "documents.json"

        self.index = None
        self.documents = []

        self.load()

    def add_documents(self, documents: list[dict], embeddings):
        """
        documents example:
        [{"id": "C101", "text": "Customer has an active loan"}]
        """
        if not documents:
            return

        vectors = np.asarray(embeddings, dtype=np.float32)

        if vectors.ndim != 2 or len(vectors) != len(documents):
            raise ValueError("Each document must have one embedding.")

        if not np.isfinite(vectors).all():
            raise ValueError("Embeddings contain invalid numbers.")

        faiss.normalize_L2(vectors)

        if self.index is None:
            dimension = vectors.shape[1]
            self.index = faiss.IndexFlatIP(dimension)
        elif self.index.d != vectors.shape[1]:
            raise ValueError("Embedding dimension does not match index.")

        self.index.add(vectors)
        self.documents.extend(documents)

        self.save()

    def search(self, query_embedding, top_k: int = 5):
        """Return the most similar documents and their scores."""
        if self.index is None or self.index.ntotal == 0:
            return []

        if top_k < 1:
            raise ValueError("top_k must be at least 1.")

        query = np.asarray(
            query_embedding, dtype=np.float32
        ).reshape(1, -1)

        if query.shape[1] != self.index.d:
            raise ValueError("Query embedding dimension mismatch.")

        if not np.isfinite(query).all():
            raise ValueError("Query embedding contains invalid numbers.")

        faiss.normalize_L2(query)

        scores, indices = self.index.search(
            query, min(top_k, self.index.ntotal)
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue

            results.append({
                "document": self.documents[int(idx)],
                "score": float(score),
            })

        return results

    def save(self):
        if self.index is None:
            return

        faiss.write_index(self.index, str(self.index_path))

        with self.documents_path.open("w", encoding="utf-8") as file:
            json.dump(
                self.documents,
                file,
                ensure_ascii=False,
                indent=2,
            )

    def load(self):
        if self.index_path.exists() and self.documents_path.exists():
            self.index = faiss.read_index(str(self.index_path))

            with self.documents_path.open(
                "r", encoding="utf-8"
            ) as file:
                self.documents = json.load(file)

            if self.index.ntotal != len(self.documents):
                raise ValueError(
                    "Saved FAISS index and documents do not match."
                )
