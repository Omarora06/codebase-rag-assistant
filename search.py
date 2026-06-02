from app.embedding.embedder import create_embedding
from app.vectorstore.chroma_store import search

query = input("Ask a question: ")

query_embedding = create_embedding(query)

results = search(
    query_embedding,
    n_results=5
)

documents = results["documents"][0]
metadatas = results["metadatas"][0]

for i in range(len(documents)):

    print("\n" + "=" * 80)

    print(
        f"File: {metadatas[i]['path']}"
    )

    print(
        f"Type: {metadatas[i]['type']}"
    )

    print(
        f"Name: {metadatas[i]['name']}"
    )

    print("-" * 80)

    print(documents[i])

    print("=" * 80)