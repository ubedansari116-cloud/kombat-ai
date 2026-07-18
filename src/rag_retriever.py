from pathlib import Path
import json
import re
import numpy as np
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VECTOR_DIR = PROJECT_ROOT / "data" / "vectorstore"


class FighterRetriever:
    def __init__(self):
        config_path = VECTOR_DIR / "config.json"
        embeddings_path = VECTOR_DIR / "fighter_embeddings.npy"
        documents_path = VECTOR_DIR / "fighter_documents.json"
        metadata_path = VECTOR_DIR / "fighter_metadata.json"

        for path in [config_path, embeddings_path, documents_path, metadata_path]:
            if not path.exists():
                raise FileNotFoundError(f"Missing vector-store file: {path}")

        with config_path.open("r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.embeddings = np.load(embeddings_path)
        with documents_path.open("r", encoding="utf-8") as f:
            self.documents = json.load(f)
        with metadata_path.open("r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        if not (len(self.embeddings) == len(self.documents) == len(self.metadata)):
            raise ValueError("Vector-store files have mismatched lengths.")

        self.model = SentenceTransformer(self.config["model_name"])

        # Build name index more robustly
        self.fighter_names = []
        self.name_to_index = {}
        self.name_variants = {}  # For fuzzy matching

        for idx, doc in enumerate(self.documents):
            name = self.extract_fighter_name(doc)
            if name:
                clean_name = name.strip()
                self.fighter_names.append(clean_name)
                lower_name = clean_name.lower()
                self.name_to_index[lower_name] = idx
                
                # Add variants for better matching
                self.name_variants[lower_name] = idx
                # Handle common cases like first + last name
                parts = lower_name.split()
                if len(parts) >= 2:
                    self.name_variants[parts[0]] = idx  # First name
                    self.name_variants[f"{parts[0]} {parts[-1]}"] = idx  # First + Last

    @staticmethod
    def extract_fighter_name(document: str):
        lines = document.splitlines()
        for line in lines[:3]:  # Check first few lines
            if line.startswith("Fighter Profile:"):
                return line.replace("Fighter Profile:", "").strip()
        return None

    def detect_fighter_names(self, query: str):
        """Improved name detection"""
        normalized = query.lower().strip()
        detected = set()

        # Try exact matches first (including variants)
        for name, idx in self.name_variants.items():
            if name in normalized:
                detected.add(self.fighter_names[idx])  # Get original casing

        # Fallback: semantic if nothing found
        if not detected:
            # You could add fuzzy matching here later (e.g., rapidfuzz)
            pass

        return sorted(list(detected), key=lambda x: normalized.find(x.lower()))

    def exact_search(self, fighter_names):
        results = []
        for rank, name in enumerate(fighter_names, start=1):
            idx = self.name_to_index.get(name.lower())
            if idx is not None:
                results.append({
                    "rank": rank,
                    "score": 1.0,
                    "retrieval_type": "exact_name",
                    "fighter_name": name,
                    "document": self.documents[idx],
                    "metadata": self.metadata[idx],
                })
        return results

    def semantic_search(self, query: str, top_k: int = 5):
        query_embedding = self.model.encode([query], normalize_embeddings=True)[0]
        scores = self.embeddings @ query_embedding
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for rank, idx in enumerate(top_indices, start=1):
            fighter_name = self.extract_fighter_name(self.documents[idx])
            results.append({
                "rank": rank,
                "score": float(scores[idx]),
                "retrieval_type": "semantic",
                "fighter_name": fighter_name or "Unknown",
                "document": self.documents[idx],
                "metadata": self.metadata[idx],
            })
        return results

    def search(self, query: str, top_k: int = 5):
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        detected_names = self.detect_fighter_names(query)

        if detected_names:
            return self.exact_search(detected_names)
        
        # Fallback
        return self.semantic_search(query, top_k=top_k)


# For testing
if __name__ == "__main__":
    retriever = FighterRetriever()
    print(f"Loaded {len(retriever.fighter_names)} fighters.")
    while True:
        q = input("\nQuery: ").strip()
        if q.lower() in ["exit", "quit"]:
            break
        results = retriever.search(q)
        for r in results:
            print(f"{r['fighter_name']} | {r['retrieval_type']} | Score: {r['score']:.3f}")