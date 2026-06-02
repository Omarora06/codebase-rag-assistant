import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="code_chunks"
)


def add_chunk(chunk_id, chunk, embedding):

    collection.add(
        ids=[chunk_id],

        documents=[
            chunk["content"]
        ],

        embeddings=[
            embedding.tolist()
        ],

        metadatas=[
            {
                "path": chunk["path"],
                "type": chunk["type"],
                "name": chunk["name"]
            }
        ]
    )


def search(query_embedding, n_results=5):

    return collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=n_results
    )