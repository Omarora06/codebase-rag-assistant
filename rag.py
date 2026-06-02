from app.embedding.embedder import create_embedding
from app.vectorstore.chroma_store import search
from app.llm.generator import generate_answer

question = input("Ask a question: ")

query_embedding = create_embedding(question)

results = search(
    query_embedding,
    n_results=5
)

context = "\n\n".join(
    results["documents"][0]
)

answer = generate_answer(
    question,
    context
)

print("\n")
print(answer)