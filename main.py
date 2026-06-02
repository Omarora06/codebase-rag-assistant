from app.ingestion.repo_loader import load_repository
from app.chunking.chunker import chunk_python_file
from app.embedding.embedder import create_embedding
from app.vectorstore.chroma_store import add_chunk

files = load_repository("./repos")

all_chunks = []

for file in files:
    all_chunks.extend(
        chunk_python_file(file)
    )

print(f"Total Chunks: {len(all_chunks)}")

for i, chunk in enumerate(all_chunks):

    embedding = create_embedding(
        chunk["content"]
    )

    add_chunk(
        str(i),
        chunk,
        embedding
    )

    if i % 100 == 0:
        print(f"Indexed {i}")

print("Indexing Complete")