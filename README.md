# Codebase RAG Assistant

An AI-powered Retrieval-Augmented Generation (RAG) system for understanding source code repositories.

## Features

- Loads Python repositories
- Parses code using Python AST
- Extracts functions and classes
- Generates embeddings using Sentence Transformers
- Stores vectors in ChromaDB
- Retrieves relevant code chunks
- Uses Gemini for intelligent codebase Q&A

## Tech Stack

- Python
- AST
- Sentence Transformers
- ChromaDB
- Google Gemini

## Project Structure

app/
+-- ingestion/
+-- chunking/
+-- embedding/
+-- vectorstore/
+-- llm/

main.py
rag.py
search.py

## Example Questions

- How does Flask register routes?
- How does Flask handle request contexts?
- How are errors handled in Flask?
- Explain the Flask application lifecycle.

## Workflow

1. Load repository
2. Parse code with AST
3. Generate embeddings
4. Store vectors in ChromaDB
5. Retrieve relevant chunks
6. Generate answers using Gemini

