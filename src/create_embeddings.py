from pathlib import Path
import json

import numpy as np
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / "data" / "fighter_docs"
VECTOR_DIR = PROJECT_ROOT / "data" / "vectorstore"

MODEL_NAME = "all-MiniLM-L6-v2"


def load_documents():
    files = sorted(DOCS_DIR.glob("*.txt"))

    if not files:
        raise FileNotFoundError(
            f"No fighter documents found in: {DOCS_DIR}"
        )

    documents = []
    metadata = []

    for file_path in files:
        text = file_path.read_text(encoding="utf-8").strip()

        if not text:
            continue

        documents.append(text)
        metadata.append(
            {
                "filename": file_path.name,
                "path": str(file_path),
            }
        )

    return documents, metadata


def main():
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)

    documents, metadata = load_documents()

    print(f"Loaded {len(documents)} fighter documents.")
    print(f"Loading embedding model: {MODEL_NAME}")

    model = SentenceTransformer(MODEL_NAME)

    embeddings = model.encode(
        documents,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    embeddings = np.asarray(embeddings, dtype=np.float32)

    np.save(VECTOR_DIR / "fighter_embeddings.npy", embeddings)

    with open(
        VECTOR_DIR / "fighter_documents.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(documents, file, ensure_ascii=False, indent=2)

    with open(
        VECTOR_DIR / "fighter_metadata.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(metadata, file, ensure_ascii=False, indent=2)

    config = {
        "model_name": MODEL_NAME,
        "document_count": len(documents),
        "embedding_dimension": int(embeddings.shape[1]),
        "normalized": True,
    }

    with open(
        VECTOR_DIR / "config.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(config, file, indent=2)

    print("\nVector store created successfully.")
    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Saved to: {VECTOR_DIR}")


if __name__ == "__main__":
    main()