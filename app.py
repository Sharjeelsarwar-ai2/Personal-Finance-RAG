import streamlit as st
import time
from document_processor import DocumentProcessor
from rag_engine import RAGEngine
from ui_components import (
    inject_custom_css,
    render_header,
    render_metrics,
    render_file_item,
    render_chat_message,
    render_suggestion_chips,
    render_pipeline_status,
    render_upload_zone
)

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="FinanceRAG Analyzer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS
inject_custom_css()


# ===== SESSION STATE INITIALIZATION =====
def init_session_state():
    defaults = {
        "doc_processor": None,
        "rag_engine": None,
        "chat_history": [],
        "messages": [],
        "docs_processed": 0,
        "chunks_count": 0,
        "pipeline_status": "idle",
        "processed_files": [],
        "groq_api_key": "",
        "is_indexed": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# ===== SIDEBAR =====
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h2 style="color: rgba(255,255,255,0.9); font-weight: 700;">⚙️ Configuration</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # API Key
        st.markdown("""
        <h3 style="font-size: 0.9rem; color: rgba(255,255,255,0.6); 
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">
        🔑 Groq API Key</h3>
        """, unsafe_allow_html=True)

        api_key = st.text_input(
            "Enter API Key",
            type="password",
            value=st.session_state.groq_api_key,
            placeholder="gsk_...",
            label_visibility="collapsed"
        )

        if api_key != st.session_state.groq_api_key:
            st.session_state.groq_api_key = api_key
            st.session_state.rag_engine = None  # Reset engine on key change

        if api_key:
            st.markdown('<span class="status-badge badge-success">✓ Key Provided</span>',
                        unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-badge badge-error">✗ Key Required</span>',
                        unsafe_allow_html=True)
            st.markdown("""
            <div class="info-box">
                Get your free API key at <a href="https://console.groq.com" 
                target="_blank" style="color: #4facfe;">console.groq.com</a>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # Model Selection
        st.markdown("""
        <h3 style="font-size: 0.9rem; color: rgba(255,255,255,0.6); 
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">
        🧠 LLM Model</h3>
        """, unsafe_allow_html=True)

        model = st.selectbox(
            "Select Model",
            [
                "meta-llama/llama-4-scout-17b-16e-instruct",
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
                "mixtral-8x7b-32768",
                "gemma2-9b-it"
            ],
            index=0,
            label_visibility="collapsed"
        )

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # Processing Pipeline Status
        st.markdown("""
        <h3 style="font-size: 0.9rem; color: rgba(255,255,255,0.6); 
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">
        📊 Pipeline Status</h3>
        """, unsafe_allow_html=True)

        status = st.session_state.pipeline_status

        if status == "idle":
            steps = {
                "Upload Documents": "",
                "Extract Content": "",
                "Create Chunks": "",
                "Generate Embeddings": "",
                "Build FAISS Index": "",
                "Ready for Queries": ""
            }
        elif status == "processing":
            steps = {
                "Upload Documents": "done",
                "Extract Content": "active",
                "Create Chunks": "",
                "Generate Embeddings": "",
                "Build FAISS Index": "",
                "Ready for Queries": ""
            }
        elif status == "ready":
            steps = {
                "Upload Documents": "done",
                "Extract Content": "done",
                "Create Chunks": "done",
                "Generate Embeddings": "done",
                "Build FAISS Index": "done",
                "Ready for Queries": "done"
            }
        else:
            steps = {
                "Upload Documents": "done",
                "Extract Content": "done",
                "Create Chunks": "done",
                "Generate Embeddings": "done",
                "Build FAISS Index": "done",
                "Ready for Queries": "done"
            }

        render_pipeline_status(steps)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # Processed Files List
        if st.session_state.processed_files:
            st.markdown("""
            <h3 style="font-size: 0.9rem; color: rgba(255,255,255,0.6); 
            text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">
            📁 Processed Files</h3>
            """, unsafe_allow_html=True)

            for f in st.session_state.processed_files:
                render_file_item(f["filename"], f["file_size"], f["file_type"])

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # Reset Button
        if st.button("🔄 Reset Everything", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        # Footer
        st.markdown("""
        <div style="text-align: center; padding: 20px 0; margin-top: 30px;">
            <p style="color: rgba(255,255,255,0.2); font-size: 0.75rem;">
                FinanceRAG v1.0<br>
                Powered by Groq + FAISS<br>
                Open Source RAG Pipeline
            </p>
        </div>
        """, unsafe_allow_html=True)

    return model


# ===== DOCUMENT PROCESSING =====
def process_uploaded_files(uploaded_files, model: str):
    """Process uploaded files through the RAG pipeline"""

    if not st.session_state.groq_api_key:
        st.markdown("""
        <div class="warning-box">
            ⚠️ Please enter your Groq API key in the sidebar first.
        </div>
        """, unsafe_allow_html=True)
        return

    st.session_state.pipeline_status = "processing"

    # Initialize processor
    doc_processor = DocumentProcessor()

    # Progress display
    progress_container = st.empty()

    with progress_container.container():
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)

        # Stage 1: Extract documents
        st.markdown("#### 📥 Stage 1: Extracting Documents...")
        progress_bar = st.progress(0)
        processed_docs = []

        for i, file in enumerate(uploaded_files):
            result = doc_processor.process_file(file)
            processed_docs.append(result)
            progress_bar.progress((i + 1) / len(uploaded_files))

        st.markdown(f"""
        <div class="info-box">
            ✅ Extracted {len(processed_docs)} document(s) successfully
        </div>
        """, unsafe_allow_html=True)

        # Stage 2-4: RAG Pipeline
        st.markdown("#### 🔗 Stage 2: Building RAG Pipeline...")

        rag_engine = RAGEngine(
            groq_api_key=st.session_state.groq_api_key,
            model_name=model
        )

        # Prepare documents for RAG
        docs_for_rag = []
        for doc in doc_processor.processed_docs:
            if doc["text_content"].strip():
                docs_for_rag.append({
                    "filename": doc["filename"],
                    "text_content": doc["text_content"]
                })

        if not docs_for_rag:
            st.markdown("""
            <div class="warning-box">
                ⚠️ No extractable text found in uploaded documents. 
                Please check your files and try again.
            </div>
            """, unsafe_allow_html=True)
            return

        # Chunking
        st.markdown("**→ Creating chunks with overlap...**")
        chunks = rag_engine.chunk_documents(docs_for_rag)
        st.markdown(f"&nbsp;&nbsp;&nbsp;Created **{len(chunks)}** chunks")

        # Embedding
        st.markdown("**→ Generating embeddings (all-MiniLM-L6-v2)...**")
        embeddings = rag_engine.create_embeddings()
        st.markdown(f"&nbsp;&nbsp;&nbsp;Embedded **{embeddings.shape[0]}** vectors ({embeddings.shape[1]}D)")

        # FAISS Indexing
        st.markdown("**→ Building FAISS index...**")
        rag_engine.build_index()
        st.markdown(f"&nbsp;&nbsp;&nbsp;Index size: **{rag_engine.index.ntotal}** vectors")

        st.markdown("""
        <div class="info-box">
            ✅ RAG pipeline ready! You can now ask questions about your documents.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Update session state
    st.session_state.doc_processor = doc_processor
    st.session_state.rag_engine = rag_engine
    st.session_state.docs_processed = len(processed_docs)
    st.session_state.chunks_count = len(chunks)
    st.session_state.pipeline_status = "ready"
    st.session_state.is_indexed = True
    st.session_state.processed_files = doc_processor.get_doc_summaries()


# ===== MAIN APP =====
def main():
    # Render sidebar and get model selection
    model = render_sidebar()

    # Render header
    render_header()

    # Metrics row
    status_text = "Ready" if st.session_state.is_indexed else (
        "Processing" if st.session_state.pipeline_status == "processing" else "Waiting"
    )
    render_metrics(
        st.session_state.docs_processed,
        st.session_state.chunks_count,
        status_text
    )

    # ===== TWO COLUMN LAYOUT =====
    col_upload, col_chat = st.columns([2, 3], gap="large")

    # ----- LEFT COLUMN: Upload & Process -----
    with col_upload:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.markdown("""
        <h3 style="color: rgba(255,255,255,0.85); font-weight: 600; margin-bottom: 5px;">
            📁 Document Upload
        </h3>
        <p style="color: rgba(255,255,255,0.4); font-size: 0.85rem; margin-bottom: 15px;">
            Upload your financial documents to analyze
        </p>
        """, unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Upload documents",
            type=["pdf", "csv", "xlsx", "xls", "txt", "docx"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )

        if uploaded_files:
            st.markdown(f"""
            <div class="info-box">
                📎 {len(uploaded_files)} file(s) selected
            </div>
            """, unsafe_allow_html=True)

            if st.button("🚀 Process & Index Documents", use_container_width=True):
                process_uploaded_files(uploaded_files, model)
                st.rerun()
        else:
            render_upload_zone()

        st.markdown('</div>', unsafe_allow_html=True)

        # Suggestion Chips
        if st.session_state.is_indexed:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.markdown("""
            <h3 style="color: rgba(255,255,255,0.85); font-weight: 600; margin-bottom: 15px;">
                💡 Try Asking
            </h3>
            """, unsafe_allow_html=True)

            suggestions = render_suggestion_chips()

            # Create interactive buttons for suggestions
            suggestion_cols = st.columns(2)
            for i, suggestion in enumerate(suggestions):
                with suggestion_cols[i % 2]:
                    if st.button(
                        suggestion,
                        key=f"suggest_{i}",
                        use_container_width=True,
                    ):
                        st.session_state.pending_question = suggestion
                        st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

    # ----- RIGHT COLUMN: Chat Interface -----
    with col_chat:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.markdown("""
        <h3 style="color: rgba(255,255,255,0.85); font-weight: 600; margin-bottom: 5px;">
            💬 Ask Your Documents
        </h3>
        <p style="color: rgba(255,255,255,0.4); font-size: 0.85rem; margin-bottom: 15px;">
            All answers are strictly grounded in your uploaded data — zero hallucination
        </p>
        """, unsafe_allow_html=True)

        # Chat messages display
        chat_display = st.container()

        with chat_display:
            if not st.session_state.messages:
                st.markdown("""
                <div style="text-align: center; padding: 60px 20px;">
                    <div style="font-size: 3rem; margin-bottom: 15px;">📊</div>
                    <p style="color: rgba(255,255,255,0.4); font-size: 1rem;">
                        Upload documents and start asking questions
                    </p>
                    <p style="color: rgba(255,255,255,0.2); font-size: 0.85rem;">
                        Your financial data stays private — processed locally
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                for msg in st.session_state.messages:
                    render_chat_message(
                        msg["role"],
                        msg["content"],
                        msg.get("sources", None)
                    )

        st.markdown('</div>', unsafe_allow_html=True)

        # Chat input
        if st.session_state.is_indexed:
            # Check for pending question from suggestions
            pending = st.session_state.get("pending_question", None)

            query = st.chat_input(
                "Ask about your financial documents...",
                key="chat_input"
            )

            # Use pending question if exists
            if pending:
                query = pending
                st.session_state.pending_question = None

            if query:
                # Add user message
                st.session_state.messages.append({
                    "role": "user",
                    "content": query
                })

                # Build chat history for context
                chat_history = []
                for msg in st.session_state.messages[-6:]:
                    chat_history.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

                # Query RAG engine
                with st.spinner("🔍 Searching documents & generating answer..."):
                    answer, sources = st.session_state.rag_engine.query(
                        query,
                        chat_history=chat_history[:-1]  # Exclude current query
                    )

                # Add assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

                st.rerun()
        else:
            st.markdown("""
            <div class="warning-box">
                📤 Upload and process documents first to enable the chat.
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
