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

        .nav-brand { display: flex; align-items: center; gap: 12px; }
        .nav-logo { font-size: 1.6rem; }
        .nav-title {
            font-size: 1.2rem; font-weight: 700;
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .nav-status { display: flex; align-items: center; gap: 20px; }

        .status-pill {
            display: inline-flex; align-items: center; gap: 6px;
            padding: 6px 14px; border-radius: 20px;
            font-size: 0.78rem; font-weight: 500;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: rgba(255, 255, 255, 0.7);
        }
        .status-pill .dot { width: 8px; height: 8px; border-radius: 50%; }
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

        /* ===== HEADER STYLING ===== */
        .main-header { text-align: center; padding: 20px 20px 15px 20px; }
        .main-header h1 {
            font-size: 2.4rem; font-weight: 800;
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 50%, #a8edea 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        .main-header p { color: rgba(255, 255, 255, 0.5); font-size: 1rem; font-weight: 300; }

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
            font-size: 0.7rem; text-transform: uppercase;
            font-weight: 600; margin-bottom: 8px;
        }
        .user-label { color: #4facfe; }
        .assistant-label { color: #a8edea; }

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

        /* =========================================================
           🚀 THE FIX: PINNED CHAT INPUT PANEL AT BOTTOM OF SCREEN
           ========================================================= */
        div[data-testid="stChatInput"] {
            position: fixed !important;
            bottom: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            /* Gradient background to fade out text as it scrolls behind */
            background: linear-gradient(0deg, rgba(10,10,26,1) 50%, rgba(10,10,26,0) 100%) !important;
            padding: 40px 2rem 30px 2rem !important;
            z-index: 9999 !important;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* Target the actual input box */
        div[data-testid="stChatInput"] > div {
            width: 100% !important;
            max-width: 900px !important;
            background: rgba(20, 20, 35, 0.95) !important;
            border: 1px solid rgba(79, 172, 254, 0.4) !important;
            border-radius: 16px !important;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(15px);
        }

        /* Spacer to push final messages above the floating chat bar */
        .chat-bottom-spacer {
            height: 120px;
            width: 100%;
        }
        /* ========================================================= */

        /* ===== OTHER UI ELEMENTS ===== */
        .upload-zone {
            background: rgba(79, 172, 254, 0.03);
            border: 2px dashed rgba(79, 172, 254, 0.2);
            border-radius: 20px; padding: 40px; text-align: center; margin: 15px 0;
        }
        .upload-icon { font-size: 3rem; margin-bottom: 10px; }
        
        .file-item {
            background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px; padding: 12px 16px; margin: 8px 0;
            display: flex; align-items: center; gap: 12px;
        }
        
        .pipeline-horizontal {
            display: flex; justify-content: space-between; gap: 10px; padding: 15px 0; flex-wrap: wrap;
        }
        .pipeline-step-h {
            flex: 1; min-width: 120px; text-align: center; padding: 12px 8px;
            border-radius: 12px; background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .pipeline-step-h.done { background: rgba(0, 255, 136, 0.05); border-color: rgba(0, 255, 136, 0.2); }
        .pipeline-step-h.active { background: rgba(79, 172, 254, 0.08); border-color: rgba(79, 172, 254, 0.3); }
        .step-icon-h { font-size: 1.2rem; margin-bottom: 6px; }
        .step-name-h { font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); }
        .pipeline-step-h.done .step-name-h { color: rgba(0, 255, 136, 0.9); }
        .pipeline-step-h.active .step-name-h { color: rgba(79, 172, 254, 0.9); }
        
        .stButton > button {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
            color: #0a0a1a !important; border: none !important;
            border-radius: 12px !important; padding: 10px 24px !important; font-weight: 600 !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_top_nav(is_indexed: bool, pipeline_status: str, has_api_key: bool):
    if is_indexed: status_dot, status_text = "dot-green", "Ready"
    elif pipeline_status == "processing": status_dot, status_text = "dot-yellow", "Processing"
    else: status_dot, status_text = "dot-red", "Awaiting Upload"
    
    api_dot = "dot-green" if has_api_key else "dot-red"
    api_text = "API Connected" if has_api_key else "API Not Set"
    
    st.markdown(f"""
    <div class="top-nav">
        <div class="nav-brand"><span class="nav-logo">💰</span><span class="nav-title">FinanceRAG Analyzer</span></div>
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
        <p>Upload documents • Get precise answers • Zero hallucination</p>
    </div>
    """, unsafe_allow_html=True)

def render_metrics(docs_count: int, chunks_count: int, status: str):
    pass # Replaced by the Tabs UI

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
    if role == "user":
        html = f"""<div class="user-message"><div class="message-label user-label">🧑 You</div>{content}</div>"""
        st.markdown(html, unsafe_allow_html=True)
    else:
        source_html = ""
        if sources and len(sources) > 0:
            source_items = "".join([f"<li>{s}</li>" for s in sources[:3]])
            source_html = f"""<div class="source-box"><strong>📎 Sources Referenced:</strong><ul>{source_items}</ul></div>"""
        html = f"""<div class="assistant-message"><div class="message-label assistant-label">🤖 FinanceRAG</div>{content}{source_html}</div>"""
        st.markdown(html, unsafe_allow_html=True)

def render_chat_spacer():
    """Adds invisible spacing so the last message isn't hidden behind the floating chat bar"""
    st.markdown('<div class="chat-bottom-spacer"></div>', unsafe_allow_html=True)

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
        <div style="color: rgba(255,255,255,0.6); font-size: 0.95rem;">Drop your financial documents here</div>
        <div style="color: rgba(255,255,255,0.3); font-size: 0.8rem; margin-top: 8px;">PDF • CSV • XLSX • TXT • DOCX</div>
    </div>
    """, unsafe_allow_html=True)
