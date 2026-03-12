import chromadb
import time

client = chromadb.Client()
collection = client.get_or_create_collection("ideas")


def add_memory(text: str, entry_type: str = "idea") -> str:
    """Store a new memory. Returns the document ID."""
    doc_id = str(abs(hash(text + str(time.time()))))  # unique even for duplicate text
    collection.add(
        documents=[text],
        ids=[doc_id],
        metadatas=[{"type": entry_type, "timestamp": time.time()}],
    )
    return doc_id


def search_memory(query: str, n_results: int = 8) -> list[dict]:
    """Return the top-n most semantically related memories."""
    count = collection.count()
    if count == 0:
        return []

    n = min(n_results, count)
    results = collection.query(query_texts=[query], n_results=n)

    memories = []
    for doc, dist, meta in zip(
        results["documents"][0],
        results["distances"][0],
        results["metadatas"][0],
    ):
        memories.append({
            "text":     doc,
            "distance": round(dist, 4),
            "type":     (meta or {}).get("type", "idea"),
        })
    return memories


def get_all_memories() -> list[dict]:
    """Return every stored memory (most recent first)."""
    data = collection.get()
    if not data["documents"]:
        return []
    pairs = list(zip(data["documents"], data["metadatas"]))
    pairs.sort(key=lambda p: (p[1] or {}).get("timestamp", 0), reverse=True)
    return [
        {"text": doc, "type": (meta or {}).get("type", "idea")}
        for doc, meta in pairs
    ]


def memory_count() -> int:
    return collection.count()
