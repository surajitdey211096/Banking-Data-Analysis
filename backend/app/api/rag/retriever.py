
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore


class BankingRetriever:
    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
        vector_store: VectorStore | None = None,
    ):
        self.embedding_service = (
            embedding_service or EmbeddingService()
        )
        self.vector_store = vector_store or VectorStore()

    def index_documents(self, documents: list[dict]):
        """
        Index documents containing at least:
        {"id": "TXN101", "text": "Transaction amount was 2500"}
        """
        texts = [doc["text"] for doc in documents]

        embeddings = self.embedding_service.create_embeddings(texts)

        self.vector_store.add_documents(documents, embeddings)

    def retrieve(self, question: str, top_k: int = 5):
        """Find records relevant to the user's question."""
        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        query_embedding = self.embedding_service.create_embedding(
            question.strip()
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        return results
