import json
from pathlib import Path
from typing import Any

class DocumentStore:
def init(self, storage_dir: str | Path | None = None):
base_dir = Path(file).resolve().parents[1]
self.storage_dir = Path(
        storage_dir or base_dir / "rag" / "documents"
    )
    self.storage_dir.mkdir(parents=True, exist_ok=True)

    self.file_path = self.storage_dir / "documents.jsonl"

def save_documents(self, documents: list[dict[str, Any]]) -> None:
    """Save documents as JSON Lines."""
    with self.file_path.open("w", encoding="utf-8") as file:
        for document in documents:
            file.write(
                json.dumps(document, ensure_ascii=False) + "\n"
            )

def load_documents(self) -> list[dict[str, Any]]:
    """Load all saved documents."""
    if not self.file_path.exists():
        return []

    documents = []

    with self.file_path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                documents.append(json.loads(line))

    return documents

def add_document(self, document: dict[str, Any]) -> None:
    """Append one document."""
    with self.file_path.open("a", encoding="utf-8") as file:
        file.write(
            json.dumps(document, ensure_ascii=False) + "\n"
        )

def clear(self) -> None:
    """Remove all stored document records."""
    if self.file_path.exists():
        self.file_path.unlink()