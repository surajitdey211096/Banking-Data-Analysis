import json
from pathlib import Path
from typing import Any

class MetadataStore:
def init(self, storage_dir: str | Path | None = None):
base_dir = Path(file).resolve().parents[1]
self.storage_dir = Path(
        storage_dir or base_dir / "rag" / "metadata"
    )
    self.storage_dir.mkdir(parents=True, exist_ok=True)

    self.file_path = self.storage_dir / "metadata.json"

def save_metadata(self, metadata: list[dict[str, Any]]) -> None:
    """Save metadata records."""
    with self.file_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4, ensure_ascii=False)

def load_metadata(self) -> list[dict[str, Any]]:
    """Load metadata records."""
    if not self.file_path.exists():
        return []

    with self.file_path.open("r", encoding="utf-8") as file:
        return json.load(file)

def add_metadata(self, item: dict[str, Any]) -> None:
    """Append one metadata record."""
    metadata = self.load_metadata()
    metadata.append(item)
    self.save_metadata(metadata)

def clear(self) -> None:
    """Remove all stored metadata."""
    if self.file_path.exists():
        self.file_path.unlink()