import streamlit as st

from app.embedding.embedder import create_embedding
from app.vectorstore.chroma_store import search
from app.llm.generator import generate_answer


st.set_page_config(
    page_title="Codebase RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------
# Session State
# ----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ----------------------------
# Sidebar
# ----------------------------

with st.sidebar:

    st.title("⚙️ System Info")

    st.success("System Ready")

    st.markdown("---")

    st.subheader("Project")

    st.write("**Vector DB:** ChromaDB")
    st.write("**LLM:** Gemini 2.5 Flash")
    st.write("**Embedding Model:** all-MiniLM-L6-v2")

    st.markdown("---")

    st.subheader("Conversation")

    st.metric(
        "Messages",
        len(st.session_state.messages)
    )

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ----------------------------
# Main Header
# ----------------------------

st.title("🤖 Codebase RAG Assistant")

st.write(
    "Ask questions about the indexed codebase using semantic search and Gemini."
)

st.markdown("---")


# ----------------------------
# Question Input
# ----------------------------

question = st.text_input(
    "Enter your question:",
    placeholder="Example: How are routes registered in Flask?"
)

ask = st.button(
    "🚀 Ask Question",
    use_container_width=True
)


# ----------------------------
# Generate Answer
# ----------------------------

if ask and question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.spinner(
        "🔍 Searching codebase and generating answer..."
    ):

        query_embedding = create_embedding(
            question
        )

        results = search(
            query_embedding,
            n_results=5
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        context = "\n\n".join(
            documents
        )

        answer = generate_answer(
            question,
            context
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "documents": documents,
            "metadatas": metadatas,
            "context": context
        }
    )

    st.rerun()


# ----------------------------
# Chat History
# ----------------------------

st.subheader("💬 Conversation")

for msg in st.session_state.messages:

    if msg["role"] == "user":

        with st.chat_message("user"):
            st.markdown(msg["content"])

    else:

        with st.chat_message("assistant"):

            st.markdown(
                msg["content"]
            )

            st.subheader(
                "📂 Retrieved Sources"
            )

            for i in range(
                len(msg["metadatas"])
            ):

                metadata = msg["metadatas"][i]

                with st.expander(
                    f"{i+1}. {metadata['path']}"
                ):

                    st.write(
                        f"**Type:** {metadata['type']}"
                    )

                    st.write(
                        f"**Name:** {metadata['name']}"
                    )

                    st.code(
                        msg["documents"][i],
                        language="python"
                    )

            st.subheader(
                "📊 Retrieval Statistics"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Retrieved Chunks",
                    len(msg["documents"])
                )

            with col2:

                st.metric(
                    "Unique Files",
                    len(
                        set(
                            metadata["path"]
                            for metadata in msg["metadatas"]
                        )
                    )
                )

            with col3:

                st.metric(
                    "Context Size",
                    f"{len(msg['context']):,}"
                )