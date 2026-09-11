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
    render_pipeline_horizontal,
    render_upload_zone,
    render_top_nav
)

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="FinanceRAG Analyzer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
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
        "is_indexed": False,
        "show_settings": False,
        "selected_model": "llama-3.3-70b-versatile"
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# ===== TOP NAVIGATION WITH SETTINGS =====
def render_top_bar():
    """Render top nav with Settings toggle button"""
    
    # Top nav status bar
    render_top_nav(
        is_indexed=st.session_state.is_indexed,
        pipeline_status=st.session_state.pipeline_status,
        has_api_key=bool(st.session_state.groq_api_key)
    )
    
    # Action buttons row
    col1, col2, col3, col4 = st.columns([6, 1.5, 1.5, 1.5])
    
    with col2:
        if st.button("⚙️ Settings", use_container_width=True, key="btn_settings"):
            st.session_state.show_settings = not st.session_state.show_settings
    
    with col3:
        if st.button("📊 Pipeline", use_container_width=True, key="btn_pipeline"):
            st.session_state.show_pipeline = not st.session_state.get("show_pipeline", False)
    
    with col4:
        if st.button("🔄 Reset", use_container_width=True, key="btn_reset"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ===== SETTINGS PANEL =====
def render_settings_panel():
    """Render the collapsible settings panel"""
    if not st.session_state.show_settings:
        return
    
    st.markdown('<div class="settings-panel">', unsafe_allow_html=True)
    st.markdown("""
    <div class="settings-title">⚙️ Configuration</div>
    <div class="settings-subtitle">Configure your API key and LLM model settings</div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.markdown('<div class="settings-label">🔑 Groq API Key</div>', unsafe_allow_html=True)
        api_key = st.text_input(
            "api_key_input",
            type="password",
            value=st.session_state.groq_api_key,
            placeholder="gsk_...",
            label_visibility="collapsed",
            key="settings_api_key"
        )
        
        if api_key != st.session_state.groq_api_key:
            st.session_state.groq_api_key = api_key
            st.session_state.rag_engine = None
        
        if not api_key:
            st.markdown("""
            <div class="info-box" style="margin-top: 8px;">
                Get free API key at <a href="https://console.groq.com" target="_blank" 
                style="color: #4facfe;">console.groq.com</a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <span class="status-badge badge-success" style="margin-top: 8px;">
                ✓ API Key Provided
            </span>
            """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown('<div class="settings-label">🧠 LLM Model</div>', unsafe_allow_html=True)
        model = st.selectbox(
            "model_select",
            [
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
                "meta-llama/llama-4-scout-17b-16e-instruct",
                "gemma2-9b-it",
                "mixtral-8x7b-32768"
            ],
            index=0,
            label_visibility="collapsed",
            key="settings_model"
        )
        st.session_state.selected_model = model
        
        st.markdown(f"""
        <div class="info-box" style="margin-top: 8px;">
            Model: <strong>{model.split('/')[-1]}</strong><br>
            Temperature: <strong>0.1</strong> (factual)
        </div>
        """, unsafe_allow_html=True)
    
    # Close button
    col_x, col_y, col_z = st.columns([4, 1, 4])
    with col_y:
        if st.button("✕ Close", key="close_settings", use_container_width=True):
            st.session_state.show_settings = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


# ===== PIPELINE STATUS PANEL =====
def render_pipeline_status_panel():
    """Show the pipeline stages status"""
    if not st.session_state.get("show_pipeline", False):
        return
    
    st.markdown('<div class="settings-panel">', unsafe_allow_html=True)
    st.markdown("""
    <div class="settings-title">📊 RAG Pipeline Status</div>
    <div class="settings-subtitle">Multi-stage document processing workflow</div>
    """, unsafe_allow_html=True)
    
    status = st.session_state.pipeline_status
    
    if status == "idle":
        steps = {"Upload": "", "Extract": "", "Chunk": "", "Embed": "", "Index": "", "Ready": ""}
    elif status == "processing":
        steps = {"Upload": "done", "Extract": "active", "Chunk": "", "Embed": "", "Index": "", "Ready": ""}
    elif status == "ready":
        steps = {"Upload": "done", "Extract": "done", "Chunk": "done", "Embed": "done", "Index": "done", "Ready": "done"}
    else:
        steps = {"Upload": "done", "Extract": "done", "Chunk": "done", "Embed": "done", "Index": "done", "Ready": "done"}
    
    render_pipeline_horizontal(steps)
    
    # Close button
    col_x, col_y, col_z = st.columns([4, 1, 4])
    with col_y:
        if st.button("✕ Close", key="close_pipeline", use_container_width=True):
            st.session_state.show_pipeline = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


# ===== DOCUMENT PROCESSING =====
def process_uploaded_files(uploaded_files, model: str):
    """Process uploaded files through the RAG pipeline"""
    if not st.session_state.groq_api_key:
        st.markdown("""
        <div class="warning-box">
            ⚠️ Please click <strong>⚙️ Settings</strong> above and enter your Groq API key first.
        </div>
        """, unsafe_allow_html=True)
        return

    st.session_state.pipeline_status = "processing"
    doc_processor = DocumentProcessor()

    progress_container = st.empty()

    with progress_container.container():
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
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

        st.markdown("#### 🔗 Stage 2: Building RAG Pipeline...")

        rag_engine = RAGEngine(
            groq_api_key=st.session_state.groq_api_key,
            model_name=model
        )

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
            </div>
            """, unsafe_allow_html=True)
            return

        st.markdown("**→ Creating chunks with overlap...**")
        chunks = rag_engine.chunk_documents(docs_for_rag)
        st.markdown(f"&nbsp;&nbsp;&nbsp;Created **{len(chunks)}** chunks")

        st.markdown("**→ Generating embeddings (all-MiniLM-L6-v2)...**")
        embeddings = rag_engine.create_embeddings()
        st.markdown(f"&nbsp;&nbsp;&nbsp;Embedded **{embeddings.shape[0]}** vectors ({embeddings.shape[1]}D)")

        st.markdown("**→ Building FAISS index...**")
        rag_engine.build_index()
        st.markdown(f"&nbsp;&nbsp;&nbsp;Index size: **{rag_engine.index.ntotal}** vectors")

        st.markdown("""
        <div class="info-box">
            ✅ RAG pipeline ready! You can now ask questions about your documents.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.session_state.doc_processor = doc_processor
    st.session_state.rag_engine = rag_engine
    st.session_state.docs_processed = len(processed_docs)
    st.session_state.chunks_count = len(chunks)
    st.session_state.pipeline_status = "ready"
    st.session_state.is_indexed = True
    st.session_state.processed_files = doc_processor.get_doc_summaries()


# ===== MAIN APP =====
def main():
    # Top navigation bar
    render_top_bar()
    
    # Conditional panels
    render_settings_panel()
    render_pipeline_status_panel()
    
    # Main header
    render_header()

    # Metrics
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

    # ----- LEFT COLUMN: Upload & Files -----
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
                process_uploaded_files(uploaded_files, st.session_state.selected_model)
                st.rerun()
        else:
            render_upload_zone()

        st.markdown('</div>', unsafe_allow_html=True)

        # Show processed files
        if st.session_state.processed_files:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.markdown("""
            <h3 style="color: rgba(255,255,255,0.85); font-weight: 600; margin-bottom: 15px;">
                📚 Indexed Documents
            </h3>
            """, unsafe_allow_html=True)
            
            for f in st.session_state.processed_files:
                render_file_item(f["filename"], f["file_size"], f["file_type"])
            
            st.markdown('</div>', unsafe_allow_html=True)

        # Suggestions
        if st.session_state.is_indexed:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.markdown("""
            <h3 style="color: rgba(255,255,255,0.85); font-weight: 600; margin-bottom: 15px;">
                💡 Try Asking
            </h3>
            """, unsafe_allow_html=True)

            suggestions = render_suggestion_chips()
            suggestion_cols = st.columns(2)
            for i, suggestion in enumerate(suggestions):
                with suggestion_cols[i % 2]:
                    if st.button(suggestion, key=f"suggest_{i}", use_container_width=True):
                        st.session_state.pending_question = suggestion
                        st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

    # ----- RIGHT COLUMN: Chat -----
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
                        Your financial data stays private
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                for msg in st.session_state.messages:
                    render_chat_message(msg["role"], msg["content"], msg.get("sources", None))

        st.markdown('</div>', unsafe_allow_html=True)

        # Chat input
        if st.session_state.is_indexed:
            pending = st.session_state.get("pending_question", None)
            query = st.chat_input("Ask about your financial documents...", key="chat_input")

            if pending:
                query = pending
                st.session_state.pending_question = None

            if query:
                st.session_state.messages.append({"role": "user", "content": query})

                chat_history = []
                for msg in st.session_state.messages[-6:]:
                    chat_history.append({"role": msg["role"], "content": msg["content"]})

                with st.spinner("🔍 Searching documents & generating answer..."):
                    answer, sources = st.session_state.rag_engine.query(
                        query, chat_history=chat_history[:-1]
                    )

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
