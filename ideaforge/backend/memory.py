import chromadb
import time

client = chromadb.Client()
collection = client.get_or_create_collection("ideas")


def add_memory(text, entry_type="idea"):
    """Store a new memory with metadata."""
    doc_id = str(abs(hash(text)))
    collection.add(
        documents=[text],
        ids=[doc_id],
        metadatas=[{"type": entry_type, "timestamp": time.time()}],
    )
    return doc_id


def search_memory(query, n_results=5):
    """Return related memories with similarity distances."""
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
            "text": doc,
            "distance": round(dist, 4),
            "type": meta.get("type", "idea"),
        })
    return memories


def get_all_memories():
    """Return every stored memory."""
    data = collection.get()
    if not data["documents"]:
        return []
    return [
        {"text": doc, "type": (meta or {}).get("type", "idea")}
        for doc, meta in zip(data["documents"], data["metadatas"])
    ]


def memory_count():
    return collection.count()
