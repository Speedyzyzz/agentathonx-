import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection("ideas")


def add_memory(text):
    collection.add(
        documents=[text],
        ids=[str(hash(text))],
    )


def search_memory(query):
    results = collection.query(
        query_texts=[query],
        n_results=5,
    )

    return results["documents"][0]
