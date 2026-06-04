import streamlit as st

from app.embedding.embedder import create_embedding
from app.vectorstore.chroma_store import search
from app.llm.generator import generate_answer


# ----------------------------
# Page Config
# ----------------------------

st.set_page_config(
    page_title="Codebase RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------
# Custom Theme
# ----------------------------

st.markdown("""
<style>

/* Main App */
.stApp {
    background-color: #0B1220;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(
        135deg,
        #10B981,
        #34D399
    );
    color: white;
    border: none;
    border-radius: 12px;
    height: 3rem;
    font-weight: bold;
}

/* Metric Cards */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.15);
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}

/* Input Box */
.stTextInput input {
    border-radius: 12px;
}

/* Code Blocks */
pre {
    border-radius: 12px !important;
}

/* Hero Banner Typography */
h2, h4 {
    margin: 0;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Session State
# ----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------
# Sidebar
# ----------------------------

with st.sidebar:

    st.title("⚙️ AI Control Center")

    st.success("🟢 System Ready")

    st.markdown("---")

    st.subheader("📦 Project")

    st.write("**Vector DB:** ChromaDB")
    st.write("**LLM:** Gemini 2.5 Flash")
    st.write("**Embedding Model:** all-MiniLM-L6-v2")

    st.markdown("---")

    st.subheader("💬 Conversation")

    st.metric(
        "Messages",
        len(st.session_state.messages)
    )

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ----------------------------
# Hero Banner
# ----------------------------

st.markdown(
    """
    <div style="
        background: linear-gradient(
            135deg,
            #10B981,
            #34D399
        );
        padding: 18px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    ">
        <h2>🤖 Codebase RAG Assistant</h2>
        <h4>Semantic Search • ChromaDB • Gemini</h4>
        <p style="margin: 5px 0 0 0;">Understand Any Codebase Using AI</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Dashboard Metrics
# ----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Messages",
        len(st.session_state.messages)
    )

with col2:
    st.metric(
        "Vector DB",
        "ChromaDB"
    )

with col3:
    st.metric(
        "Status",
        "Online"
    )

# ----------------------------
# Architecture Panel
# ----------------------------

st.markdown("### ⚡ Architecture")

st.markdown("""
<div style="
    background: rgba(255,255,255,0.05);
    padding:18px;
    border-radius:15px;
    border:1px solid rgba(255,255,255,0.1);
    text-align:center;
    font-size:18px;
    margin-bottom:20px;
">
    📁 Repository → 🧠 Embeddings → 🗄️ ChromaDB →
    🔎 Retriever → 🤖 Gemini → ✅ Answer
</div>
""", unsafe_allow_html=True)

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
        "🔍 Searching codebase..."
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

    with st.spinner(
        "🧠 Generating answer..."
    ):

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
# Conversation
# ----------------------------

st.markdown("## 💬 Conversation")

if len(st.session_state.messages) == 0:
    st.info(
        "Ask a question to start chatting with your codebase."
    )

for msg in st.session_state.messages:

    if msg["role"] == "user":

        with st.chat_message("user"):
            st.markdown(
                msg["content"]
            )

    else:

        with st.chat_message("assistant"):

            st.markdown(
                msg["content"]
            )

            st.markdown("### 📂 Retrieved Sources")

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

            st.markdown("### 📊 Retrieval Statistics")

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