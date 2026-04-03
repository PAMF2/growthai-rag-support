"""
GrowthAI Knowledge Base Query
Semantic search across all indexed documentation.
Run: python query_knowledge.py "como configuro o webhook da z-api?"
"""

import os
import sys
import json
import chromadb
from chromadb.utils import embedding_functions

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")
COLLECTION_NAME = "growthai_knowledge"


def query(question: str, n_results: int = 5) -> list[dict]:
    """Query the knowledge base and return top results."""
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
    )

    results = collection.query(
        query_texts=[question],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    output = []
    for i in range(len(results["ids"][0])):
        output.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "header": results["metadatas"][0][i]["header"],
            "distance": round(results["distances"][0][i], 4),
        })

    return output


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if len(sys.argv) < 2:
        print("Usage: python query_knowledge.py \"sua pergunta aqui\"")
        print("\nExamples:")
        print('  python query_knowledge.py "como configuro o webhook da z-api?"')
        print('  python query_knowledge.py "redirect_uri_mismatch error"')
        print('  python query_knowledge.py "como instalo docker na vm?"')
        print('  python query_knowledge.py "bot nao responde no whatsapp"')
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    print(f"\nQuery: {question}")
    print("=" * 60)

    results = query(question)

    for i, r in enumerate(results):
        relevance = "HIGH" if r["distance"] < 0.8 else "MED" if r["distance"] < 1.2 else "LOW"
        print(f"\n--- Result {i+1} [{relevance}] (distance: {r['distance']}) ---")
        print(f"Source: {r['source']}")
        print(f"Section: {r['header']}")
        text_preview = r['text'][:500].encode('ascii', 'replace').decode('ascii')
        print(f"\n{text_preview}...")
        if len(r['text']) > 500:
            print(f"  [...{len(r['text'])-500} more chars]")


def query_json(question: str, n_results: int = 5) -> str:
    """Return results as JSON string (for programmatic use)."""
    results = query(question, n_results)
    return json.dumps(results, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
