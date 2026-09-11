import streamlit as st

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
        
        /* Hide sidebar completely */
        section[data-testid="stSidebar"] {display: none !important;}
        div[data-testid="collapsedControl"] {display: none !important;}

        /* Adjust main content to full width */
        .main .block-container {
            padding-top: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 100%;
        }

        /* ===== TABS STYLING (For UI Separation) ===== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: rgba(255, 255, 255, 0.02);
            padding: 15px 15px 0 15px;
            border-radius: 20px 20px 0 0;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-bottom: none;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 255, 255, 0.03);
            border-radius: 12px 12px 0 0;
            color: rgba(255, 255, 255, 0.6);
            padding: 10px 24px;
            border: 1px solid transparent;
            transition: all 0.3s ease;
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(79, 172, 254, 0.1) !important;
            color: #4facfe !important;
            border: 1px solid rgba(79, 172, 254, 0.3);
            border-bottom: none;
        }

        /* ===== TOP NAVIGATION BAR ===== */
        .top-nav {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 14px 24px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }

        .nav-brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .nav-logo { font-size: 1.6rem; }

        .nav-title {
            font-size: 1.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .nav-status {
            display: flex;
            align-items: center;
            gap: 20px;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 500;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: rgba(255, 255, 255, 0.7);
        }

        .status-pill .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }

        .dot-green { background: #00ff88; box-shadow: 0 0 8px #00ff88; }
        .dot-yellow { background: #ffc107; box-shadow: 0 0 8px #ffc107; }
        .dot-red { background: #ff5252; box-shadow: 0 0 8px #ff5252; }

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

        /* ===== SETTINGS PANEL ===== */
        .settings-panel {
            background: rgba(15, 15, 35, 0.7);
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            border: 1px solid rgba(79, 172, 254, 0.2);
            border-radius: 20px;
            padding: 25px 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(79, 172, 254, 0.15);
        }

        .settings-title {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 5px;
        }

        .settings-label {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.6);
            text-transform: uppercase;
            font-weight: 600;
            margin-bottom: 8px;
        }

        /* ===== HEADER STYLING ===== */
        .main-header {
            text-align: center;
            padding: 20px 20px 15px 20px;
        }

        .main-header h1 {
            font-size: 2.4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 50%, #a8edea 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        .main-header p {
            color: rgba(255, 255, 255, 0.5);
            font-size: 1rem;
            font-weight: 300;
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
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
        }

        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #4facfe;
        }

        .metric-label {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.4);
            text-transform: uppercase;
        }

        /* ===== UPLOAD ZONE ===== */
        .upload-zone {
            background: rgba(79, 172, 254, 0.03);
            border: 2px dashed rgba(79, 172, 254, 0.2);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            margin: 15px 0;
        }

        .upload-icon { font-size: 3rem; margin-bottom: 10px; }
        .upload-text { color: rgba(255, 255, 255, 0.6); font-size: 0.95rem; }

        /* ===== CHAT STYLING ===== */
        .user-message {
            background: linear-gradient(135deg, rgba(79, 172, 254, 0.15), rgba(0, 242, 254, 0.08));
            border: 1px solid rgba(79, 172, 254, 0.2);
            border-radius: 18px 18px 4px 18px;
            padding: 16px 20px;
            margin: 15px 0;
            margin-left: 15%;
            color: rgba(255, 255, 255, 0.9);
        }

        .assistant-message {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 18px 18px 18px 4px;
            padding: 16px 20px;
            margin: 15px 0;
            margin-right: 10%;
            color: rgba(255, 255, 255, 0.85);
        }

        .message-label {
            font-size: 0.7rem;
            text-transform: uppercase;
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
            margin-top: 15px;
            font-size: 0.8rem;
            color: rgba(168, 237, 234, 0.7);
        }
        .source-box ul { margin-top: 5px; margin-bottom: 0; padding-left: 20px; }

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
        }

        /* ===== STATUS BADGES ===== */
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .badge-success { background: rgba(0, 255, 136, 0.1); color: #00ff88; border: 1px solid rgba(0, 255, 136, 0.2); }
        .badge-error { background: rgba(255, 82, 82, 0.1); color: #ff5252; border: 1px solid rgba(255, 82, 82, 0.2); }

        /* ===== BUTTON OVERRIDES ===== */
        .stButton > button {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
            color: #0a0a1a !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
        }
        .stButton > button[kind="secondary"] {
            background: rgba(255, 255, 255, 0.05) !important;
            color: rgba(255, 255, 255, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }

        /* ===== PIPELINE HORIZONTAL ===== */
        .pipeline-horizontal {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            padding: 15px 0;
            flex-wrap: wrap;
        }
        .pipeline-step-h {
            flex: 1;
            min-width: 120px;
            text-align: center;
            padding: 12px 8px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .pipeline-step-h.done { background: rgba(0, 255, 136, 0.05); border-color: rgba(0, 255, 136, 0.2); }
        .pipeline-step-h.active { background: rgba(79, 172, 254, 0.08); border-color: rgba(79, 172, 254, 0.3); }
        .step-icon-h { font-size: 1.2rem; margin-bottom: 6px; }
        .step-name-h { font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); }
        .pipeline-step-h.done .step-name-h { color: rgba(0, 255, 136, 0.9); }
        .pipeline-step-h.active .step-name-h { color: rgba(79, 172, 254, 0.9); }
    </style>
    """, unsafe_allow_html=True)

def render_top_nav(is_indexed: bool, pipeline_status: str, has_api_key: bool):
    if is_indexed:
        status_dot, status_text = "dot-green", "Ready"
    elif pipeline_status == "processing":
        status_dot, status_text = "dot-yellow", "Processing"
    else:
        status_dot, status_text = "dot-red", "Awaiting Upload"
    
    api_dot = "dot-green" if has_api_key else "dot-red"
    api_text = "API Connected" if has_api_key else "API Not Set"
    
    st.markdown(f"""
    <div class="top-nav">
        <div class="nav-brand">
            <span class="nav-logo">💰</span>
            <span class="nav-title">FinanceRAG Analyzer</span>
        </div>
        <div class="nav-status">
            <div class="status-pill"><span class="dot {api_dot}"></span><span>{api_text}</span></div>
            <div class="status-pill"><span class="dot {status_dot}"></span><span>{status_text}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
    <div class="main-header">
        <h1>Ask Your Financial Documents Anything</h1>
        <p>Upload documents • Get precise answers • Zero hallucination — 100% grounded in your data</p>
    </div>
    """, unsafe_allow_html=True)

def render_metrics(docs_count: int, chunks_count: int, status: str):
    status_color = "#00ff88" if status == "Ready" else "#ffc107" if status == "Processing" else "#ff5252"
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card"><div class="metric-value">{docs_count}</div><div class="metric-label">Documents</div></div>
        <div class="metric-card"><div class="metric-value">{chunks_count}</div><div class="metric-label">Chunks Indexed</div></div>
        <div class="metric-card"><div class="metric-value" style="color: {status_color};">●</div><div class="metric-label">{status}</div></div>
    </div>
    """, unsafe_allow_html=True)

def render_file_item(filename: str, file_size: float, file_type: str):
    icons = {"pdf": "📄", "csv": "📊", "xlsx": "📈", "txt": "📝", "docx": "📋"}
    icon = icons.get(file_type.lower(), "📎")
    size_str = f"{file_size:.1f} KB" if file_size < 1024 else f"{file_size/1024:.1f} MB"
    st.markdown(f"""
    <div class="file-item">
        <span style="font-size:1.3rem;">{icon}</span>
        <div>
            <div style="color:rgba(255,255,255,0.8); font-size:0.85rem; font-weight:500;">{filename}</div>
            <div style="color:rgba(255,255,255,0.3); font-size:0.75rem;">{size_str} • {file_type.upper()}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_chat_message(role: str, content: str, sources: list = None):
    """Render a chat message, fixing HTML indentation to prevent code blocks."""
    if role == "user":
        # No indentation here to prevent Markdown issues
        html = f"""
<div class="user-message">
<div class="message-label user-label">🧑 You</div>

{content}

</div>
"""
        st.markdown(html, unsafe_allow_html=True)
    else:
        source_html = ""
        if sources and len(sources) > 0:
            source_items = "".join([f"<li>{s}</li>" for s in sources[:3]])
            # Built without spaces at the start of lines to prevent markdown code blocks
            source_html = f"""
<div class="source-box">
<strong>📎 Sources Referenced:</strong>
<ul>{source_items}</ul>
</div>
"""
        
        # Combine everything flush to the left
        html = f"""
<div class="assistant-message">
<div class="message-label assistant-label">🤖 FinanceRAG</div>

{content}

{source_html}
</div>
"""
        st.markdown(html, unsafe_allow_html=True)

def render_pipeline_horizontal(steps: dict):
    html = '<div class="pipeline-horizontal">'
    icons_map = {"Upload": "📤", "Extract": "🔍", "Chunk": "✂️", "Embed": "🧬", "Index": "🗄️", "Ready": "✅"}
    for step_name, status in steps.items():
        icon = "✓" if status == "done" else "⟳" if status == "active" else icons_map.get(step_name, "○")
        html += f'<div class="pipeline-step-h {status}"><div class="step-icon-h">{icon}</div><div class="step-name-h">{step_name}</div></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def render_upload_zone():
    st.markdown("""
    <div class="upload-zone">
        <div class="upload-icon">📁</div>
        <div class="upload-text">Drop your financial documents here</div>
        <div style="color: rgba(255, 255, 255, 0.3); font-size: 0.8rem; margin-top: 8px;">PDF • CSV • XLSX • TXT • DOCX</div>
    </div>
    """, unsafe_allow_html=True)
