"""
GrowthAI Knowledge Base Indexer
Indexes all .md files from the skill into ChromaDB for semantic search.
Run: python index_knowledge.py
"""

import os
import re
import chromadb
from chromadb.utils import embedding_functions

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")
COLLECTION_NAME = "growthai_knowledge"

# Also index the repo docs
REPO_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "growth-ai-agents")


def chunk_markdown(text: str, filepath: str, max_chunk: int = 800) -> list[dict]:
    """Split markdown into semantic chunks by headers."""
    chunks = []
    current_header = ""
    current_text = []

    for line in text.split("\n"):
        if line.startswith("#"):
            # Save previous chunk
            if current_text:
                content = "\n".join(current_text).strip()
                if len(content) > 50:  # Skip tiny chunks
                    chunks.append({
                        "text": f"{current_header}\n\n{content}" if current_header else content,
                        "header": current_header,
                        "source": filepath,
                    })
            current_header = line.strip()
            current_text = []
        else:
            current_text.append(line)

    # Last chunk
    if current_text:
        content = "\n".join(current_text).strip()
        if len(content) > 50:
            chunks.append({
                "text": f"{current_header}\n\n{content}" if current_header else content,
                "header": current_header,
                "source": filepath,
            })

    # Split oversized chunks
    final_chunks = []
    for chunk in chunks:
        text = chunk["text"]
        if len(text) > max_chunk:
            # Split by double newline or table rows
            parts = re.split(r"\n\n+", text)
            buffer = ""
            for part in parts:
                if len(buffer) + len(part) > max_chunk and buffer:
                    final_chunks.append({
                        "text": buffer.strip(),
                        "header": chunk["header"],
                        "source": chunk["source"],
                    })
                    buffer = part
                else:
                    buffer += "\n\n" + part if buffer else part
            if buffer.strip():
                final_chunks.append({
                    "text": buffer.strip(),
                    "header": chunk["header"],
                    "source": chunk["source"],
                })
        else:
            final_chunks.append(chunk)

    return final_chunks


def collect_files() -> list[str]:
    """Collect all .md files from skill dir and repo docs."""
    files = []

    # Skill files
    for root, _, filenames in os.walk(SKILL_DIR):
        for f in filenames:
            if f.endswith(".md"):
                files.append(os.path.join(root, f))

    # Repo docs and READMEs
    if os.path.exists(REPO_DIR):
        for f in os.listdir(REPO_DIR):
            if f.endswith(".md"):
                files.append(os.path.join(REPO_DIR, f))

        docs_dir = os.path.join(REPO_DIR, "docs")
        if os.path.exists(docs_dir):
            for root, _, filenames in os.walk(docs_dir):
                for f in filenames:
                    if f.endswith(".md"):
                        files.append(os.path.join(root, f))

        # Policies
        policies_dir = os.path.join(REPO_DIR, "policies")
        if os.path.exists(policies_dir):
            for f in os.listdir(policies_dir):
                if f.endswith((".yaml", ".yml")):
                    files.append(os.path.join(policies_dir, f))

        # .env.example
        env_example = os.path.join(REPO_DIR, ".env.example")
        if os.path.exists(env_example):
            files.append(env_example)

    return files


def main():
    print("GrowthAI Knowledge Base Indexer")
    print("=" * 50)

    # Setup ChromaDB
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    client = chromadb.PersistentClient(path=DB_DIR)

    # Delete existing collection if exists
    try:
        client.delete_collection(COLLECTION_NAME)
        print("Deleted existing collection.")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"description": "GrowthAI platform knowledge base for support"}
    )

    # Collect and index
    files = collect_files()
    print(f"\nFound {len(files)} files to index.")

    total_chunks = 0
    for filepath in files:
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            print(f"  SKIP {filepath}: {e}")
            continue

        relative = os.path.relpath(filepath, os.path.expanduser("~"))
        chunks = chunk_markdown(content, relative)

        if not chunks:
            continue

        ids = [f"{relative}::chunk_{i}" for i in range(len(chunks))]
        documents = [c["text"] for c in chunks]
        metadatas = [{"source": c["source"], "header": c["header"]} for c in chunks]

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
        )

        total_chunks += len(chunks)
        print(f"  [{len(chunks):3d} chunks] {relative}")

    print(f"\nDone! Indexed {total_chunks} chunks from {len(files)} files.")
    print(f"Database: {DB_DIR}")


if __name__ == "__main__":
    main()
