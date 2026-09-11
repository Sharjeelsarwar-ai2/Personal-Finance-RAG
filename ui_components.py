import streamlit as st
import base64
from datetime import datetime


def inject_custom_css():
    """Inject glassmorphic professional CSS styling"""
    st.markdown("""
    <style>
        /* ===== GLOBAL RESET & FONT ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        .stApp {
            background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3e 25%, #0d1b2a 50%, #1b2a4a 75%, #0a0a1a 100%);
            font-family: 'Inter', sans-serif;
            background-attachment: fixed;
        }

        /* Hide default streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}

        /* ===== GLASSMORPHIC CONTAINERS ===== */
        .glass-container {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }

        .glass-container:hover {
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 8px 40px rgba(79, 172, 254, 0.1);
        }

        /* ===== HEADER STYLING ===== */
        .main-header {
            text-align: center;
            padding: 40px 20px 20px 20px;
        }

        .main-header h1 {
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 50%, #a8edea 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
            letter-spacing: -1px;
        }

        .main-header p {
            color: rgba(255, 255, 255, 0.5);
            font-size: 1.05rem;
            font-weight: 300;
            letter-spacing: 0.5px;
        }

        /* ===== METRIC CARDS ===== */
        .metric-row {
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }

        .metric-card {
            flex: 1;
            min-width: 150px;
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-3px);
            border-color: rgba(79, 172, 254, 0.3);
            box-shadow: 0 10px 30px rgba(79, 172, 254, 0.1);
        }

        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #4facfe;
            margin-bottom: 4px;
        }

        .metric-label {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.4);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 500;
        }

        /* ===== UPLOAD ZONE ===== */
        .upload-zone {
            background: rgba(79, 172, 254, 0.03);
            border: 2px dashed rgba(79, 172, 254, 0.2);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            transition: all 0.3s ease;
            margin: 15px 0;
        }

        .upload-zone:hover {
            border-color: rgba(79, 172, 254, 0.5);
            background: rgba(79, 172, 254, 0.06);
        }

        .upload-icon {
            font-size: 3rem;
            margin-bottom: 10px;
        }

        .upload-text {
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.95rem;
        }

        .upload-formats {
            color: rgba(255, 255, 255, 0.3);
            font-size: 0.8rem;
            margin-top: 8px;
        }

        /* ===== CHAT STYLING ===== */
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
            padding: 10px;
            scrollbar-width: thin;
            scrollbar-color: rgba(79, 172, 254, 0.3) transparent;
        }

        .chat-container::-webkit-scrollbar {
            width: 6px;
        }

        .chat-container::-webkit-scrollbar-thumb {
            background: rgba(79, 172, 254, 0.3);
            border-radius: 3px;
        }

        .user-message {
            background: linear-gradient(135deg, rgba(79, 172, 254, 0.15), rgba(0, 242, 254, 0.08));
            border: 1px solid rgba(79, 172, 254, 0.2);
            border-radius: 18px 18px 4px 18px;
            padding: 16px 20px;
            margin: 10px 0;
            margin-left: 15%;
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.95rem;
            line-height: 1.6;
        }

        .assistant-message {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 18px 18px 18px 4px;
            padding: 16px 20px;
            margin: 10px 0;
            margin-right: 10%;
            color: rgba(255, 255, 255, 0.85);
            font-size: 0.95rem;
            line-height: 1.7;
        }

        .message-label {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .user-label { color: #4facfe; }
        .assistant-label { color: #a8edea; }

        /* ===== SOURCE BOX ===== */
        .source-box {
            background: rgba(168, 237, 234, 0.05);
            border: 1px solid rgba(168, 237, 234, 0.15);
            border-radius: 12px;
            padding: 12px 16px;
            margin-top: 10px;
            font-size: 0.8rem;
            color: rgba(168, 237, 234, 0.7);
        }

        .source-box strong {
            color: rgba(168, 237, 234, 0.9);
        }

        /* ===== SIDEBAR STYLING ===== */
        section[data-testid="stSidebar"] {
            background: rgba(10, 10, 26, 0.95) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        section[data-testid="stSidebar"] .stMarkdown h3 {
            color: rgba(255, 255, 255, 0.8);
            font-weight: 600;
        }

        /* ===== FILE LIST ===== */
        .file-item {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 12px 16px;
            margin: 8px 0;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.2s ease;
        }

        .file-item:hover {
            background: rgba(255, 255, 255, 0.07);
            border-color: rgba(79, 172, 254, 0.2);
        }

        .file-icon {
            font-size: 1.3rem;
        }

        .file-name {
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.85rem;
            font-weight: 500;
        }

        .file-size {
            color: rgba(255, 255, 255, 0.3);
            font-size: 0.75rem;
        }

        /* ===== STATUS BADGES ===== */
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .badge-success {
            background: rgba(0, 255, 136, 0.1);
            color: #00ff88;
            border: 1px solid rgba(0, 255, 136, 0.2);
        }

        .badge-processing {
            background: rgba(255, 193, 7, 0.1);
            color: #ffc107;
            border: 1px solid rgba(255, 193, 7, 0.2);
        }

        .badge-error {
            background: rgba(255, 82, 82, 0.1);
            color: #ff5252;
            border: 1px solid rgba(255, 82, 82, 0.2);
        }

        /* ===== SUGGESTION CHIPS ===== */
        .suggestion-chip {
            display: inline-block;
            background: rgba(79, 172, 254, 0.08);
            border: 1px solid rgba(79, 172, 254, 0.2);
            border-radius: 25px;
            padding: 8px 18px;
            margin: 5px;
            color: rgba(79, 172, 254, 0.9);
            font-size: 0.82rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .suggestion-chip:hover {
            background: rgba(79, 172, 254, 0.15);
            border-color: rgba(79, 172, 254, 0.4);
            transform: translateY(-1px);
        }

        /* ===== PIPELINE STEPS ===== */
        .pipeline-step {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 8px 0;
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.85rem;
        }

        .pipeline-step.active {
            color: rgba(79, 172, 254, 0.9);
        }

        .pipeline-step.done {
            color: rgba(0, 255, 136, 0.8);
        }

        .step-number {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: 700;
            border: 2px solid rgba(255, 255, 255, 0.15);
        }

        .step-number.active {
            border-color: #4facfe;
            color: #4facfe;
            box-shadow: 0 0 15px rgba(79, 172, 254, 0.3);
        }

        .step-number.done {
            border-color: #00ff88;
            color: #00ff88;
            background: rgba(0, 255, 136, 0.1);
        }

        /* ===== BUTTON OVERRIDES ===== */
        .stButton > button {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
            color: #0a0a1a !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 12px 30px !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            letter-spacing: 0.5px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3) !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 25px rgba(79, 172, 254, 0.5) !important;
        }

        /* ===== TEXT INPUT ===== */
        .stTextInput > div > div > input,
        .stChatInput > div > div > textarea {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 14px !important;
            color: white !important;
            font-family: 'Inter', sans-serif !important;
            padding: 14px 18px !important;
        }

        .stTextInput > div > div > input:focus,
        .stChatInput > div > div > textarea:focus {
            border-color: rgba(79, 172, 254, 0.5) !important;
            box-shadow: 0 0 20px rgba(79, 172, 254, 0.15) !important;
        }

        /* ===== FILE UPLOADER ===== */
        .stFileUploader {
            background: transparent !important;
        }

        .stFileUploader > div {
            background: rgba(79, 172, 254, 0.03) !important;
            border: 2px dashed rgba(79, 172, 254, 0.2) !important;
            border-radius: 16px !important;
            padding: 20px !important;
        }

        /* ===== EXPANDER ===== */
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.03) !important;
            border-radius: 12px !important;
            color: rgba(255, 255, 255, 0.8) !important;
        }

        /* ===== SPINNER ===== */
        .stSpinner > div {
            border-top-color: #4facfe !important;
        }

        /* ===== DIVIDER ===== */
        .custom-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(79, 172, 254, 0.3), transparent);
            margin: 25px 0;
            border: none;
        }

        /* ===== WARNING / INFO BOXES ===== */
        .info-box {
            background: rgba(79, 172, 254, 0.06);
            border-left: 3px solid #4facfe;
            border-radius: 0 12px 12px 0;
            padding: 14px 18px;
            margin: 10px 0;
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.88rem;
        }

        .warning-box {
            background: rgba(255, 193, 7, 0.06);
            border-left: 3px solid #ffc107;
            border-radius: 0 12px 12px 0;
            padding: 14px 18px;
            margin: 10px 0;
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.88rem;
        }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>💰 FinanceRAG Analyzer</h1>
        <p>Upload your financial documents • Ask questions • Get precise answers from YOUR data</p>
    </div>
    <div class="custom-divider"></div>
    """, unsafe_allow_html=True)


def render_metrics(docs_count: int, chunks_count: int, status: str):
    """Render metric cards"""
    status_color = "#00ff88" if status == "Ready" else "#ffc107" if status == "Processing" else "#ff5252"
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-value">{docs_count}</div>
            <div class="metric-label">Documents</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{chunks_count}</div>
            <div class="metric-label">Chunks Indexed</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" style="color: {status_color};">●</div>
            <div class="metric-label">{status}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_file_item(filename: str, file_size: float, file_type: str):
    """Render a single file item"""
    icons = {
        "pdf": "📄",
        "csv": "📊",
        "xlsx": "📈",
        "xls": "📈",
        "txt": "📝",
        "docx": "📋"
    }
    icon = icons.get(file_type.lower(), "📎")
    size_str = f"{file_size:.1f} KB" if file_size < 1024 else f"{file_size/1024:.1f} MB"

    st.markdown(f"""
    <div class="file-item">
        <span class="file-icon">{icon}</span>
        <div>
            <div class="file-name">{filename}</div>
            <div class="file-size">{size_str} • {file_type.upper()}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_chat_message(role: str, content: str, sources: list = None):
    """Render a chat message with optional sources"""
    if role == "user":
        st.markdown(f"""
        <div class="user-message">
            <div class="message-label user-label">🧑 You</div>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        source_html = ""
        if sources and len(sources) > 0:
            source_items = "".join([f"<br>• {s}" for s in sources[:3]])
            source_html = f"""
            <div class="source-box">
                <strong>📎 Sources Referenced:</strong>{source_items}
            </div>
            """
        st.markdown(f"""
        <div class="assistant-message">
            <div class="message-label assistant-label">🤖 FinanceRAG</div>
            {content}
            {source_html}
        </div>
        """, unsafe_allow_html=True)


def render_suggestion_chips():
    """Render suggestion query chips"""
    suggestions = [
        "What is my total income?",
        "Summarize my expenses by category",
        "What deductions can I claim?",
        "What are my largest transactions?",
        "Show my monthly spending trend",
        "Any recurring payments found?"
    ]
    return suggestions


def render_pipeline_status(steps: dict):
    """Render processing pipeline steps"""
    html = ""
    for step_name, status in steps.items():
        if status == "done":
            cls = "done"
            num_cls = "done"
            icon = "✓"
        elif status == "active":
            cls = "active"
            num_cls = "active"
            icon = "⟳"
        else:
            cls = ""
            num_cls = ""
            icon = "○"

        html += f"""
        <div class="pipeline-step {cls}">
            <div class="step-number {num_cls}">{icon}</div>
            <span>{step_name}</span>
        </div>
        """

    st.markdown(html, unsafe_allow_html=True)


def render_upload_zone():
    """Render upload zone description"""
    st.markdown("""
    <div class="upload-zone">
        <div class="upload-icon">📁</div>
        <div class="upload-text">Drop your financial documents here</div>
        <div class="upload-formats">PDF • CSV • XLSX • TXT • DOCX</div>
    </div>
    """, unsafe_allow_html=True)
