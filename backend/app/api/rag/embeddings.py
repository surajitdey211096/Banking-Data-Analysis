
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.model = SentenceTransformer(model_name)

    def create_embeddings(self, texts: list[str]):
        """Convert multiple text records into vectors."""
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embeddings

    def create_embedding(self, text: str):
        """Convert one question or record into a vector."""
        embeddings = self.create_embeddings([text])
        return embeddings[0]

    def get_embedding_dimension(self) -> int:
        """Return the size of each vector."""
        return self.model.get_sentence_embedding_dimension()
