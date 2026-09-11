import streamlit as st
import time
from document_processor import DocumentProcessor
from rag_engine import RAGEngine
from ui_components import (
    inject_custom_css, 
    render_header, 
    render_file_item, 
    render_chat_message,
    render_chat_spacer,       # <--- Added spacer import
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
        "selected_model": "openai/gpt-oss-120b"
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()


# ===== TOP NAVIGATION WITH SETTINGS =====
def render_top_bar():
    render_top_nav(st.session_state.is_indexed, st.session_state.pipeline_status, bool(st.session_state.groq_api_key))
    col1, col2, col3 = st.columns([7, 1.5, 1.5])
    
    with col2:
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.show_settings = not st.session_state.show_settings
            
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def render_settings_panel():
    if not st.session_state.show_settings: 
        return
    
    st.markdown('<div class="settings-panel">', unsafe_allow_html=True)
    st.markdown('<div class="settings-title">⚙️ Configuration</div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.markdown('<div class="settings-label">🔑 Groq API Key</div>', unsafe_allow_html=True)
        api_key = st.text_input("api_key", type="password", value=st.session_state.groq_api_key, label_visibility="collapsed")
        
        if api_key != st.session_state.groq_api_key:
            st.session_state.groq_api_key = api_key
            st.session_state.rag_engine = None
            
        if not api_key: 
            st.markdown('<div style="color:#ff5252; font-size:0.8rem; margin-top:5px;">Required for AI features</div>', unsafe_allow_html=True)
            
    with col_b:
        st.markdown('<div class="settings-label">🧠 LLM Model</div>', unsafe_allow_html=True)
        model = st.selectbox(
            "model_select", 
            ["openai/gpt-oss-120b", "llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"], 
            index=0, 
            label_visibility="collapsed"
        )
        st.session_state.selected_model = model
    
    col_x, col_y, col_z = st.columns([4, 1, 4])
    with col_y:
        if st.button("✕ Close", use_container_width=True):
            st.session_state.show_settings = False
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)


# ===== DOCUMENT PROCESSING =====
def process_uploaded_files(uploaded_files, model: str):
    if not st.session_state.groq_api_key:
        st.error("⚠️ Please click ⚙️ Settings above and enter your Groq API key first.")
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
            processed_docs.append(doc_processor.process_file(file))
            progress_bar.progress((i + 1) / len(uploaded_files))

        st.markdown("#### 🔗 Stage 2: Building RAG Pipeline...")
        rag_engine = RAGEngine(st.session_state.groq_api_key, model_name=model)
        
        docs_for_rag = [{"filename": d["filename"], "text_content": d["text_content"]} for d in doc_processor.processed_docs if d["text_content"].strip()]
        
        chunks = rag_engine.chunk_documents(docs_for_rag)
        st.markdown(f"&nbsp;&nbsp;&nbsp;Created **{len(chunks)}** chunks")
        
        embeddings = rag_engine.create_embeddings()
        st.markdown(f"&nbsp;&nbsp;&nbsp;Embedded vectors")
        
        rag_engine.build_index()
        st.markdown("✅ RAG pipeline ready!")
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
    render_top_bar()
    render_settings_panel()
    render_header()

    # ==========================================
    # TABS FOR UI SEPARATION
    # ==========================================
    tab_chat, tab_data = st.tabs(["💬 Query Console", "🗄️ RAG Data Management"])

    # ----- TAB 1: USER CHAT QUERIES -----
    with tab_chat:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.markdown("""<h3 style="color: rgba(255,255,255,0.85); font-weight: 600; margin-bottom: 5px;">💬 Ask Your Documents</h3>""", unsafe_allow_html=True)

        # Chat display area
        if not st.session_state.messages:
            st.markdown("""
            <div style="text-align: center; padding: 60px 20px;">
                <div style="font-size: 3rem; margin-bottom: 15px;">📊</div>
                <p style="color: rgba(255,255,255,0.4); font-size: 1rem;">Upload documents in the 'RAG Data Management' tab to begin.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.messages:
                render_chat_message(msg["role"], msg["content"], msg.get("sources", None))

        st.markdown('</div>', unsafe_allow_html=True)

        # 🚀 SPACER: This pushes the last message up so it doesn't hide behind the floating input
        render_chat_spacer()

        # Chat Input (Floating at bottom because of the CSS in ui_components.py)
        if st.session_state.is_indexed:
            query = st.chat_input("Ask about your financial documents...", key="chat_input")
            if query:
                st.session_state.messages.append({"role": "user", "content": query})
                chat_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-6:]]
                
                with st.spinner("🔍 Searching documents & generating answer..."):
                    answer, sources = st.session_state.rag_engine.query(query, chat_history=chat_history[:-1])
                
                st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
                st.rerun()
        else:
            st.info("📤 Go to 'RAG Data Management' tab to upload documents first.")


    # ----- TAB 2: RAG MANAGEMENT -----
    with tab_data:
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.markdown("### 📁 Upload Data")
            uploaded_files = st.file_uploader(
                "Upload docs", 
                type=["pdf", "csv", "xlsx", "txt", "docx"], 
                accept_multiple_files=True, 
                label_visibility="collapsed"
            )
            
            if uploaded_files:
                if st.button("🚀 Process & Index Documents", use_container_width=True):
                    process_uploaded_files(uploaded_files, st.session_state.selected_model)
                    st.rerun()
            else:
                render_upload_zone()
                
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.markdown("### 📊 Pipeline Status")
            
            # Pipeline Visualizer
            s = st.session_state.pipeline_status
            steps = {
                "Upload": "done" if s in ["processing", "ready"] else "", 
                "Extract": "active" if s == "processing" else ("done" if s == "ready" else ""),
                "Chunk": "done" if s == "ready" else "", 
                "Embed": "done" if s == "ready" else "",
                "Index": "done" if s == "ready" else ""
            }
            render_pipeline_horizontal(steps)
            
            st.markdown("### 📚 Indexed Files")
            if st.session_state.processed_files:
                for f in st.session_state.processed_files:
                    render_file_item(f["filename"], f["file_size"], f["file_type"])
            else:
                st.markdown("<p style='color:gray;'>No files indexed yet.</p>", unsafe_allow_html=True)
                
            st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
