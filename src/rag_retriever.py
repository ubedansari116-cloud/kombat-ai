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

        required_files = [
            config_path,
            embeddings_path,
            documents_path,
            metadata_path,
        ]

        missing = [str(path) for path in required_files if not path.exists()]

        if missing:
            raise FileNotFoundError(
                "Missing vector-store files:\n" + "\n".join(missing)
            )

        with config_path.open("r", encoding="utf-8") as file:
            self.config = json.load(file)

        self.embeddings = np.load(embeddings_path)

        with documents_path.open("r", encoding="utf-8") as file:
            self.documents = json.load(file)

        with metadata_path.open("r", encoding="utf-8") as file:
            self.metadata = json.load(file)

        if not (
            len(self.embeddings)
            == len(self.documents)
            == len(self.metadata)
        ):
            raise ValueError(
                "Vector-store files contain different numbers of records."
            )

        self.model = SentenceTransformer(self.config["model_name"])

        self.fighter_names = []
        self.name_to_index = {}

        for index, document in enumerate(self.documents):
            fighter_name = self.extract_fighter_name(document)

            if fighter_name:
                self.fighter_names.append(fighter_name)
                self.name_to_index[fighter_name.lower()] = index

    @staticmethod
    def extract_fighter_name(document):
        first_line = document.splitlines()[0]

        if first_line.startswith("Fighter Profile:"):
            return first_line.replace("Fighter Profile:", "").strip()

        return None

    def detect_fighter_names(self, query):
        normalized_query = query.lower()
        detected_names = []

        for fighter_name in self.fighter_names:
            pattern = rf"\b{re.escape(fighter_name.lower())}\b"

            if re.search(pattern, normalized_query):
                detected_names.append(fighter_name)

                detected_names.sort(
    key=lambda name: normalized_query.find(name.lower())
    )

        return detected_names

    def exact_search(self, fighter_names):
        results = []

        for rank, fighter_name in enumerate(fighter_names, start=1):
            index = self.name_to_index[fighter_name.lower()]

            results.append(
                {
                    "rank": rank,
                    "score": 1.0,
                    "retrieval_type": "exact_name",
                    "fighter_name": fighter_name,
                    "document": self.documents[index],
                    "metadata": self.metadata[index],
                }
            )

        return results

    def semantic_search(self, query, top_k=5):
        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True,
        )[0]

        scores = self.embeddings @ query_embedding

        top_k = min(top_k, len(scores))
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []

        for rank, index in enumerate(top_indices, start=1):
            fighter_name = self.extract_fighter_name(
                self.documents[index]
            )

            results.append(
                {
                    "rank": rank,
                    "score": float(scores[index]),
                    "retrieval_type": "semantic",
                    "fighter_name": fighter_name,
                    "document": self.documents[index],
                    "metadata": self.metadata[index],
                }
            )

        return results

    def search(self, query, top_k=5):
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        detected_names = self.detect_fighter_names(query)

        if detected_names:
            return self.exact_search(detected_names)

        return self.semantic_search(query, top_k=top_k)


def print_results(results):
    for result in results:
        print("=" * 80)
        print(
            f"Rank: {result['rank']} | "
            f"Score: {result['score']:.4f} | "
            f"Type: {result['retrieval_type']}"
        )
        print(f"Fighter: {result['fighter_name']}")
        print(f"Source: {result['metadata']['filename']}")
        print("-" * 80)
        print(result["document"])
        print()


def main():
    retriever = FighterRetriever()

    print("Kombat AI Fighter Retriever v2")
    print("Type 'exit' to stop.\n")

    while True:
        query = input("Ask a fighter question: ").strip()

        if query.lower() in {"exit", "quit"}:
            print("Retriever closed.")
            break

        try:
            results = retriever.search(query, top_k=3)
            print_results(results)
        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()