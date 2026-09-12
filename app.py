import streamlit as st

from document_processor import DocumentProcessor
from rag_engine import RAGEngine
try:
    import ui_components as ui
except ImportError as exc:
    raise ImportError(
        "FinanceRAG could not load ui_components.py. Make sure ui_components.py "
        "is uploaded to the same project directory as app.py and that it imports "
        "without errors. Original error: " + str(exc)
    ) from exc


# -----------------------------------------------------------------------------
# Page configuration and theme
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="FinanceRAG | Document Intelligence",
    page_icon="⌁",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ui.inject_custom_css()


# -----------------------------------------------------------------------------
# Session state
# -----------------------------------------------------------------------------

def init_session_state() -> None:
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
        "selected_model": "openai/gpt-oss-120b",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# -----------------------------------------------------------------------------
# App controls
# -----------------------------------------------------------------------------

def _status_badge(dot_color: str, label: str) -> str:
    return f"""
    <span style="display:inline-flex;align-items:center;gap:7px;padding:7px 10px;border-radius:999px;
        color:#aeb9cb;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);
        font-size:.63rem;font-weight:700;letter-spacing:.03em;white-space:nowrap;">
        <span style="width:6px;height:6px;border-radius:50%;background:{dot_color};box-shadow:0 0 9px {dot_color};"></span>{label}
    </span>
    """


def render_top_bar() -> None:
    """Render compact state badges and utility actions beneath the product header."""
    is_indexed = st.session_state.is_indexed
    status = st.session_state.pipeline_status
    has_api = bool(st.session_state.groq_api_key)

    if is_indexed:
        index_color, index_text = "#68e6bd", "Index ready"
    elif status == "processing":
        index_color, index_text = "#ffd166", "Processing"
    else:
        index_color, index_text = "#ff8296", "Awaiting documents"

    api_color, api_text = ("#68e6bd", "API connected") if has_api else ("#ff8296", "API not configured")

    left, center, settings_col, reset_col = st.columns([2.4, 3.8, 1.25, 1.0], vertical_alignment="center")
    with left:
        st.markdown(
            f'<div style="display:flex;gap:7px;align-items:center;">{_status_badge(index_color, index_text)}{_status_badge(api_color, api_text)}</div>',
            unsafe_allow_html=True,
        )
    with center:
        if st.session_state.docs_processed or st.session_state.chunks_count:
            st.markdown(
                f'<div style="color:#78849a;font-family:DM Mono,monospace;font-size:.64rem;text-align:center;letter-spacing:.03em;">'
                f'{st.session_state.docs_processed} DOCUMENTS &nbsp;·&nbsp; {st.session_state.chunks_count} RETRIEVAL CHUNKS</div>',
                unsafe_allow_html=True,
            )
    with settings_col:
        if st.button("Settings", type="secondary", use_container_width=True):
            st.session_state.show_settings = not st.session_state.show_settings
    with reset_col:
        if st.button("Reset", type="secondary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def render_settings_panel() -> None:
    if not st.session_state.show_settings:
        return

    st.markdown('<div class="glass-card" style="padding:22px 24px;margin:20px 0 24px;">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">Workspace configuration</div><div class="section-title">Connect your intelligence layer</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([1.35, 1.35, .7], gap="large", vertical_alignment="bottom")
    with col_a:
        api_key = st.text_input(
            "Groq API key",
            type="password",
            value=st.session_state.groq_api_key,
            placeholder="Paste your API key",
            help="Required to process documents and answer questions.",
        )
        if api_key != st.session_state.groq_api_key:
            st.session_state.groq_api_key = api_key
            st.session_state.rag_engine = None
    with col_b:
        models = [
            "openai/gpt-oss-120b",
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
        ]
        current_index = models.index(st.session_state.selected_model) if st.session_state.selected_model in models else 0
        st.session_state.selected_model = st.selectbox("Language model", models, index=current_index)
    with col_c:
        if st.button("Close", type="secondary", use_container_width=True):
            st.session_state.show_settings = False
            st.rerun()

    if not api_key:
        st.markdown('<div style="color:#ff9aaa;font-size:.7rem;margin-top:3px;">An API key is required before indexing.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Document processing
# -----------------------------------------------------------------------------

def process_uploaded_files(uploaded_files, model: str) -> None:
    if not st.session_state.groq_api_key:
        st.error("Open Settings and add your Groq API key before processing documents.")
        return

    st.session_state.pipeline_status = "processing"
    doc_processor = DocumentProcessor()
    progress_container = st.empty()

    with progress_container.container():
        st.markdown('<div class="glass-card" style="padding:22px 24px;margin:20px 0;">', unsafe_allow_html=True)
        st.markdown('<div class="section-kicker">Live ingestion</div><div class="section-title">Preparing your document intelligence layer</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        progress_bar = st.progress(0, text="Extracting document content…")

        processed_docs = []
        total_files = len(uploaded_files)
        for index, file in enumerate(uploaded_files):
            processed_docs.append(doc_processor.process_file(file))
            progress_bar.progress((index + 1) / total_files, text=f"Extracted {index + 1} of {total_files} documents")

        progress_bar.progress(1.0, text="Building retrieval index…")
        rag_engine = RAGEngine(st.session_state.groq_api_key, model_name=model)
        docs_for_rag = [
            {"filename": doc["filename"], "text_content": doc["text_content"]}
            for doc in doc_processor.processed_docs
            if doc["text_content"].strip()
        ]

        chunks = rag_engine.chunk_documents(docs_for_rag)
        rag_engine.create_embeddings()
        rag_engine.build_index()
        st.markdown(
            f'<div style="color:#68e6bd;font-family:DM Mono,monospace;font-size:.68rem;margin-top:10px;">✓ INDEX READY &nbsp;·&nbsp; {len(chunks)} CHUNKS EMBEDDED</div>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.session_state.doc_processor = doc_processor
    st.session_state.rag_engine = rag_engine
    st.session_state.docs_processed = len(processed_docs)
    st.session_state.chunks_count = len(chunks)
    st.session_state.pipeline_status = "ready"
    st.session_state.is_indexed = True
    st.session_state.processed_files = doc_processor.get_doc_summaries()


# -----------------------------------------------------------------------------
# Main views
# -----------------------------------------------------------------------------

def render_data_tab() -> None:
    upload_col, status_col = st.columns([1.05, .95], gap="large")

    with upload_col:
        st.markdown('<div class="glass-card" style="padding:22px 24px;min-height:390px;">', unsafe_allow_html=True)
        st.markdown('<div class="section-kicker">01 / Source library</div><div class="section-title">Add financial documents</div>', unsafe_allow_html=True)
        ui.render_upload_zone()
        uploaded_files = st.file_uploader(
            "Choose documents",
            type=["pdf", "csv", "xlsx", "txt", "docx"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )
        if uploaded_files:
            st.markdown(f'<div style="color:#9aa7bb;font-size:.72rem;margin:10px 0;">{len(uploaded_files)} document(s) selected and ready to index.</div>', unsafe_allow_html=True)
            if st.button("Process & index documents", type="primary", use_container_width=True):
                process_uploaded_files(uploaded_files, st.session_state.selected_model)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with status_col:
        st.markdown('<div class="glass-card" style="padding:22px 24px;min-height:390px;">', unsafe_allow_html=True)
        st.markdown('<div class="section-kicker">02 / Retrieval pipeline</div><div class="section-title">Knowledge base status</div>', unsafe_allow_html=True)
        current_status = st.session_state.pipeline_status
        steps = {
            "Upload": "done" if current_status in ["processing", "ready"] else "",
            "Extract": "active" if current_status == "processing" else ("done" if current_status == "ready" else ""),
            "Chunk": "done" if current_status == "ready" else "",
            "Embed": "done" if current_status == "ready" else "",
            "Index": "done" if current_status == "ready" else "",
            "Ready": "done" if current_status == "ready" else "",
        }
        ui.render_pipeline_horizontal(steps)
        st.markdown('<div class="section-kicker" style="margin-top:18px;">Indexed files</div>', unsafe_allow_html=True)
        if st.session_state.processed_files:
            for file_summary in st.session_state.processed_files:
                ui.render_file_item(file_summary["filename"], file_summary["file_size"], file_summary["file_type"])
        else:
            st.markdown('<div style="color:#68748a;font-size:.78rem;padding:24px 0;text-align:center;">Your indexed files will appear here.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def render_chat_tab() -> None:
    st.markdown('<div class="glass-card" style="padding:22px 24px;">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">Conversation layer</div><div class="section-title">Ask your documents</div>', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown(
            '<div style="text-align:center;padding:65px 20px 72px;"><div style="font-size:2.2rem;color:#58d5ff;margin-bottom:15px;">⌁</div><div style="color:#dce6f4;font-size:.9rem;font-weight:700;">Your document conversation starts here</div><div style="color:#78849a;font-size:.76rem;line-height:1.7;margin:8px auto 0;max-width:390px;">Index a report, statement, or spreadsheet to ask contextual questions with source-backed answers.</div></div>',
            unsafe_allow_html=True,
        )
    else:
        for message in st.session_state.messages:
            ui.render_chat_message(message["role"], message["content"], message.get("sources"))

    st.markdown('</div>', unsafe_allow_html=True)
    ui.render_chat_spacer()

    if st.session_state.is_indexed:
        query = st.chat_input("Ask about your financial documents…", key="chat_input")
        if query:
            st.session_state.messages.append({"role": "user", "content": query})
            chat_history = [{"role": message["role"], "content": message["content"]} for message in st.session_state.messages[-6:]]
            with st.spinner("Searching your knowledge base…"):
                answer, sources = st.session_state.rag_engine.query(query, chat_history=chat_history[:-1])
            st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
            st.rerun()
    else:
        st.info("Index documents in the Source library before starting a conversation.")


def main() -> None:
    ui.render_header()
    render_top_bar()
    render_settings_panel()

    data_tab, chat_tab = st.tabs(["Source library", "Query console"])
    with data_tab:
        render_data_tab()
    with chat_tab:
        render_chat_tab()


if __name__ == "__main__":
    main()
