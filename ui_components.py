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
        
        /* Hide sidebar */
        section[data-testid="stSidebar"] {display: none !important;}
        div[data-testid="collapsedControl"] {display: none !important;}

        /* Tighten main content padding to remove top whitespace */
        .main .block-container {
            padding-top: 1.5rem !important;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 100%;
        }

        /* ===== TABS STYLING ===== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: rgba(255, 255, 255, 0.02);
            padding: 15px 15px 0 15px;
            border-radius: 20px 20px 0 0;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-bottom: none;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 255, 255, 0.02);
            border-radius: 12px 12px 0 0;
            color: rgba(255, 255, 255, 0.5);
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

        /* ===== BUTTON STYLING (Primary vs Secondary) ===== */
        /* Primary Action Buttons (Bright Blue) */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
            color: #0a0a1a !important; 
            border: none !important;
            border-radius: 10px !important; 
            padding: 8px 20px !important; 
            font-weight: 600 !important;
            transition: all 0.2s ease;
        }
        .stButton > button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4) !important;
        }

        /* Secondary Utility Buttons (Subtle Glass) */
        .stButton > button[kind="secondary"] {
            background: rgba(255, 255, 255, 0.03) !important;
            color: rgba(255, 255, 255, 0.8) !important; 
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important; 
            padding: 8px 15px !important;
            font-weight: 500 !important;
            font-size: 0.85rem !important;
            transition: all 0.2s ease;
        }
        .stButton > button[kind="secondary"]:hover {
            background: rgba(255, 255, 255, 0.08) !important;
            border-color: rgba(79, 172, 254, 0.4) !important;
        }

        /* ===== GLASSMORPHIC CONTAINERS ===== */
        .glass-container {
            background: rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }

        /* ===== HEADER STYLING ===== */
        .main-header { 
            text-align: center; 
            padding: 10px 20px 25px 20px; /* Tighter padding */
        }
        .main-header h1 {
            font-size: 2.2rem; font-weight: 800;
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 50%, #a8edea 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        .main-header p { color: rgba(255, 255, 255, 0.5); font-size: 0.95rem; font-weight: 300; }

        /* ===== SETTINGS PANEL ===== */
        .settings-panel {
            background: rgba(15, 15, 35, 0.7);
            backdrop-filter: blur(30px);
            border: 1px solid rgba(79, 172, 254, 0.2);
            border-radius: 16px;
            padding: 25px 30px;
            margin-bottom: 15px;
            box-shadow: 0 10px 40px rgba(79, 172, 254, 0.15);
        }
        .settings-title { color: rgba(255, 255, 255, 0.9); font-size: 1.1rem; font-weight: 600; margin-bottom: 5px; }
        .settings-label { font-size: 0.8rem; color: rgba(255, 255, 255, 0.6); text-transform: uppercase; font-weight: 600; margin-bottom: 8px; }

        /* ===== CHAT STYLING ===== */
        .user-message {
            background: linear-gradient(135deg, rgba(79, 172, 254, 0.1), rgba(0, 242, 254, 0.05));
            border: 1px solid rgba(79, 172, 254, 0.15);
            border-radius: 18px 18px 4px 18px;
            padding: 16px 20px; margin: 15px 0; margin-left: 15%;
            color: rgba(255, 255, 255, 0.9);
        }
        .assistant-message {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 18px 18px 18px 4px;
            padding: 16px 20px; margin: 15px 0; margin-right: 10%;
            color: rgba(255, 255, 255, 0.85);
        }
        .message-label { font-size: 0.7rem; text-transform: uppercase; font-weight: 600; margin-bottom: 8px; }
        .user-label { color: #4facfe; }
        .assistant-label { color: #a8edea; }
        .source-box { background: rgba(168, 237, 234, 0.05); border: 1px solid rgba(168, 237, 234, 0.15); border-radius: 12px; padding: 12px 16px; margin-top: 15px; font-size: 0.8rem; color: rgba(168, 237, 234, 0.7); }
        .source-box ul { margin-top: 5px; margin-bottom: 0; padding-left: 20px; }

        /* 🚀 PINNED CHAT INPUT PANEL AT BOTTOM */
        div[data-testid="stChatInput"] {
            position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100vw !important;
            background: linear-gradient(0deg, rgba(10,10,26,1) 50%, rgba(10,10,26,0) 100%) !important;
            padding: 40px 2rem 30px 2rem !important; z-index: 9999 !important;
            display: flex; justify-content: center; align-items: center;
        }
        div[data-testid="stChatInput"] > div {
            width: 100% !important; max-width: 900px !important;
            background: rgba(20, 20, 35, 0.95) !important;
            border: 1px solid rgba(79, 172, 254, 0.3) !important;
            border-radius: 16px !important; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(15px);
        }
        .chat-bottom-spacer { height: 120px; width: 100%; }

        /* ===== OTHER UI ELEMENTS ===== */
        .upload-zone { background: rgba(79, 172, 254, 0.03); border: 2px dashed rgba(79, 172, 254, 0.2); border-radius: 20px; padding: 40px; text-align: center; margin: 15px 0; }
        .file-item { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 12px 16px; margin: 8px 0; display: flex; align-items: center; gap: 12px; }
        .pipeline-horizontal { display: flex; justify-content: space-between; gap: 10px; padding: 15px 0; flex-wrap: wrap; }
        .pipeline-step-h { flex: 1; min-width: 120px; text-align: center; padding: 12px 8px; border-radius: 12px; background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); }
        .pipeline-step-h.done { background: rgba(0, 255, 136, 0.05); border-color: rgba(0, 255, 136, 0.2); }
        .pipeline-step-h.active { background: rgba(79, 172, 254, 0.08); border-color: rgba(79, 172, 254, 0.3); }
        .step-icon-h { font-size: 1.2rem; margin-bottom: 6px; }
        .step-name-h { font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); }
        .pipeline-step-h.done .step-name-h { color: rgba(0, 255, 136, 0.9); }
        .pipeline-step-h.active .step-name-h { color: rgba(79, 172, 254, 0.9); }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
    <div class="main-header">
        <h1>Ask Your Financial Documents Anything</h1>
        <p>Upload documents • Get precise answers • Zero hallucination</p>
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
