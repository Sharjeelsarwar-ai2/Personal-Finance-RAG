"""Professional glassmorphic UI primitives for the FinanceRAG Streamlit app."""

from html import escape
from typing import Dict, List, Optional

import streamlit as st


# -----------------------------------------------------------------------------
# Theme
# -----------------------------------------------------------------------------

def inject_custom_css() -> None:
    """Inject the complete visual system used by the application."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        :root {
            --ink: #f5f7fb;
            --muted: #8f9ab0;
            --faint: #68748a;
            --cyan: #58d5ff;
            --violet: #9d8cff;
            --mint: #68e6bd;
            --panel: rgba(19, 25, 43, .68);
            --panel-soft: rgba(255, 255, 255, .045);
            --line: rgba(255, 255, 255, .105);
        }

        /* Base canvas */
        html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
        .stApp {
            color: var(--ink);
            background:
                radial-gradient(900px 520px at 8% -12%, rgba(88, 213, 255, .16), transparent 60%),
                radial-gradient(760px 520px at 96% 8%, rgba(157, 140, 255, .16), transparent 58%),
                radial-gradient(680px 480px at 50% 110%, rgba(104, 230, 189, .08), transparent 62%),
                #080c18;
            background-attachment: fixed;
        }
        .stApp::before {
            content: "";
            position: fixed; inset: 0; pointer-events: none; opacity: .25;
            background-image: linear-gradient(rgba(255,255,255,.018) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.018) 1px, transparent 1px);
            background-size: 48px 48px;
            mask-image: linear-gradient(to bottom, black, transparent 84%);
        }
        #MainMenu, footer, header, .stDeployButton { display: none !important; }
        section[data-testid="stSidebar"], div[data-testid="collapsedControl"] { display: none !important; }
        .main .block-container { max-width: 1260px; padding: 1.25rem 2rem 5rem !important; }

        /* App chrome */
        .app-bar {
            display: flex; align-items: center; justify-content: space-between; gap: 20px;
            padding: 12px 0 26px; border-bottom: 1px solid rgba(255,255,255,.07); margin-bottom: 34px;
        }
        .brand { display: flex; align-items: center; gap: 12px; }
        .brand-mark {
            width: 36px; height: 36px; display: grid; place-items: center; border-radius: 12px;
            color: #07111d; font-size: 17px; font-weight: 800;
            background: linear-gradient(135deg, var(--cyan), var(--mint));
            box-shadow: 0 0 28px rgba(88,213,255,.25);
        }
        .brand-name { font-size: .88rem; font-weight: 800; letter-spacing: .02em; }
        .brand-caption { margin-top: 2px; color: var(--muted); font-size: .66rem; letter-spacing: .08em; text-transform: uppercase; }
        .status-pill {
            display: inline-flex; align-items: center; gap: 8px; color: #b9f6df; font-size: .68rem; font-weight: 700;
            letter-spacing: .05em; text-transform: uppercase; background: rgba(104,230,189,.08);
            border: 1px solid rgba(104,230,189,.2); border-radius: 999px; padding: 8px 12px;
        }
        .status-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--mint); box-shadow: 0 0 10px var(--mint); }

        /* Hero */
        .hero { max-width: 810px; margin: 0 auto 34px; text-align: center; }
        .eyebrow { color: var(--cyan); font-family: 'DM Mono', monospace; font-size: .67rem; letter-spacing: .18em; text-transform: uppercase; }
        .hero h1 { margin: 12px 0 12px; font-size: clamp(2rem, 4.3vw, 3.75rem); line-height: 1.05; letter-spacing: -.065em; font-weight: 800; }
        .hero h1 span { background: linear-gradient(105deg, #fff 8%, #b7eaff 46%, #b6aaff 92%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero p { max-width: 550px; margin: 0 auto; color: var(--muted); font-size: .92rem; line-height: 1.7; }

        /* Reusable glass surfaces */
        .glass-card, .settings-panel, .upload-zone {
            background: linear-gradient(145deg, rgba(255,255,255,.075), rgba(255,255,255,.025));
            border: 1px solid var(--line); border-radius: 22px; box-shadow: 0 18px 55px rgba(0,0,0,.22), inset 0 1px rgba(255,255,255,.04);
            backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: linear-gradient(145deg, rgba(255,255,255,.075), rgba(255,255,255,.025));
            border: 1px solid var(--line); border-radius: 22px; padding: 4px 18px 18px;
            box-shadow: 0 18px 55px rgba(0,0,0,.22), inset 0 1px rgba(255,255,255,.04);
            backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
        }
        .section-kicker { color: var(--faint); font-family: 'DM Mono', monospace; font-size: .64rem; letter-spacing: .14em; text-transform: uppercase; }
        .section-title { color: var(--ink); font-size: 1rem; font-weight: 700; margin: 6px 0 0; }

        /* Tabs */
        .stTabs { margin-top: 12px; }
        .stTabs [data-baseweb="tab-list"] { gap: 7px; padding: 5px; background: rgba(255,255,255,.035); border: 1px solid rgba(255,255,255,.075); border-radius: 15px; }
        .stTabs [data-baseweb="tab"] { height: 38px; padding: 0 16px; border-radius: 10px; color: var(--muted); font-size: .76rem; font-weight: 700; border: 1px solid transparent; }
        .stTabs [data-baseweb="tab"]:hover { color: var(--ink); background: rgba(255,255,255,.045); }
        .stTabs [aria-selected="true"] { color: #07111d !important; background: linear-gradient(110deg, var(--cyan), #9ce9ff) !important; border-color: transparent !important; }
        .stTabs [data-baseweb="tab-highlight"] { display: none; }
        .stTabs [data-baseweb="tab-border"] { background: transparent; }

        /* Inputs and controls */
        .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] > div, .stNumberInput input {
            color: var(--ink) !important; background: rgba(4, 8, 20, .38) !important; border: 1px solid rgba(255,255,255,.1) !important; border-radius: 12px !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus { border-color: rgba(88,213,255,.65) !important; box-shadow: 0 0 0 3px rgba(88,213,255,.11) !important; }
        label, .stSlider label, .stSelectbox label, .stFileUploader label { color: var(--muted) !important; font-size: .7rem !important; font-weight: 700 !important; letter-spacing: .06em; text-transform: uppercase; }
        .stButton > button { min-height: 40px; border-radius: 12px !important; font-family: inherit !important; font-size: .76rem !important; font-weight: 700 !important; transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease !important; }
        .stButton > button:hover { transform: translateY(-2px); }
        .stButton > button[kind="primary"] { color: #06101d !important; background: linear-gradient(110deg, var(--cyan), #a8edff) !important; border: 0 !important; box-shadow: 0 8px 22px rgba(88,213,255,.17); }
        .stButton > button[kind="secondary"] { color: var(--ink) !important; background: rgba(255,255,255,.045) !important; border: 1px solid rgba(255,255,255,.11) !important; }
        .stButton > button[kind="secondary"]:hover { border-color: rgba(88,213,255,.45) !important; background: rgba(88,213,255,.08) !important; }

        /* Chat */
        .chat-stream { padding: 4px 0 8px; }
        .user-message, .assistant-message { position: relative; padding: 17px 20px; margin: 16px 0; line-height: 1.68; font-size: .88rem; }
        .user-message { margin-left: 14%; color: #e9f8ff; background: linear-gradient(135deg, rgba(88,213,255,.14), rgba(88,213,255,.045)); border: 1px solid rgba(88,213,255,.2); border-radius: 19px 19px 5px 19px; }
        .assistant-message { margin-right: 8%; color: #e9edf7; background: rgba(255,255,255,.045); border: 1px solid rgba(255,255,255,.095); border-radius: 19px 19px 19px 5px; }
        .message-label { display: flex; align-items: center; gap: 8px; margin-bottom: 7px; font-family: 'DM Mono', monospace; font-size: .63rem; font-weight: 500; letter-spacing: .08em; text-transform: uppercase; }
        .user-label { color: var(--cyan); } .assistant-label { color: var(--mint); }
        .source-box { margin-top: 16px; padding: 12px 14px; color: #a9b8c9; font-size: .73rem; background: rgba(104,230,189,.055); border: 1px solid rgba(104,230,189,.15); border-radius: 13px; }
        .source-box strong { color: var(--mint); font-size: .65rem; letter-spacing: .06em; text-transform: uppercase; }
        .source-box ul { margin: 7px 0 0; padding-left: 18px; } .source-box li { margin: 3px 0; }
        .chat-bottom-spacer { height: 125px; }
        div[data-testid="stChatInput"] { position: fixed !important; z-index: 999 !important; bottom: 0 !important; left: 0 !important; width: 100vw !important; padding: 30px 2rem 23px !important; background: linear-gradient(0deg, #080c18 40%, rgba(8,12,24,0) 100%) !important; }
        div[data-testid="stChatInput"] > div { width: min(900px, 100%) !important; margin: auto !important; background: rgba(17,24,42,.9) !important; border: 1px solid rgba(88,213,255,.3) !important; border-radius: 17px !important; box-shadow: 0 14px 40px rgba(0,0,0,.42), 0 0 0 4px rgba(88,213,255,.035) !important; backdrop-filter: blur(20px); }

        /* Upload and file cards */
        .upload-zone { padding: 36px 24px; margin: 12px 0 18px; text-align: center; border-style: dashed; border-color: rgba(88,213,255,.32); background: linear-gradient(135deg, rgba(88,213,255,.06), rgba(157,140,255,.04)); }
        .upload-icon { display: grid; place-items: center; width: 48px; height: 48px; margin: 0 auto 14px; border-radius: 15px; color: var(--cyan); font-size: 1.25rem; background: rgba(88,213,255,.1); border: 1px solid rgba(88,213,255,.2); }
        .file-item { display: flex; align-items: center; gap: 12px; padding: 12px 14px; margin: 8px 0; border-radius: 14px; background: rgba(255,255,255,.035); border: 1px solid rgba(255,255,255,.075); }
        .file-item:hover { background: rgba(255,255,255,.06); border-color: rgba(88,213,255,.22); }
        .file-icon { display: grid; place-items: center; width: 34px; height: 34px; flex: 0 0 34px; border-radius: 10px; color: var(--cyan); background: rgba(88,213,255,.09); font-size: .95rem; }
        .file-name { overflow: hidden; color: #e8edf6; font-size: .78rem; font-weight: 700; text-overflow: ellipsis; white-space: nowrap; }
        .file-meta { color: var(--faint); font-family: 'DM Mono', monospace; font-size: .61rem; margin-top: 3px; }

        /* Ingestion pipeline */
        .pipeline-horizontal { display: grid; grid-template-columns: repeat(6, 1fr); gap: 8px; padding: 15px 0; }
        .pipeline-step-h { position: relative; padding: 13px 7px; text-align: center; background: rgba(255,255,255,.025); border: 1px solid rgba(255,255,255,.07); border-radius: 13px; }
        .pipeline-step-h:not(:last-child)::after { content: '›'; position: absolute; right: -8px; top: 29%; z-index: 2; color: var(--faint); font-size: .9rem; }
        .pipeline-step-h.done { background: rgba(104,230,189,.07); border-color: rgba(104,230,189,.22); }
        .pipeline-step-h.active { background: rgba(88,213,255,.09); border-color: rgba(88,213,255,.35); box-shadow: 0 0 20px rgba(88,213,255,.08); }
        .step-icon-h { margin-bottom: 6px; color: var(--faint); font-size: .95rem; } .done .step-icon-h { color: var(--mint); } .active .step-icon-h { color: var(--cyan); }
        .step-name-h { color: var(--faint); font-family: 'DM Mono', monospace; font-size: .59rem; text-transform: uppercase; letter-spacing: .04em; } .done .step-name-h { color: var(--mint); } .active .step-name-h { color: var(--cyan); }

        @media (max-width: 720px) {
            .main .block-container { padding: .9rem 1rem 4rem !important; }
            .app-bar { margin-bottom: 24px; } .status-pill { display: none; }
            .hero { margin-bottom: 25px; } .hero h1 { font-size: 2.25rem; }
            .user-message { margin-left: 3%; } .assistant-message { margin-right: 3%; }
            .pipeline-horizontal { grid-template-columns: repeat(3, 1fr); } .pipeline-step-h:not(:last-child)::after { display: none; }
            div[data-testid="stChatInput"] { padding: 24px 1rem 15px !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# Application chrome and content primitives
# -----------------------------------------------------------------------------

def render_header() -> None:
    """Render the product chrome and hero section."""
    st.markdown(
        """
        <div class="app-bar">
            <div class="brand">
                <div class="brand-mark">⌁</div>
                <div><div class="brand-name">FinanceRAG</div><div class="brand-caption">Intelligent document workspace</div></div>
            </div>
            <div class="status-pill"><span class="status-dot"></span>Secure workspace</div>
        </div>
        <div class="hero">
            <div class="eyebrow">Your private financial intelligence layer</div>
            <h1>Ask your documents.<br><span>Get answers you can trust.</span></h1>
            <p>Bring your reports, statements, and spreadsheets into one focused workspace. Search contextually and move from question to insight in seconds.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_file_item(filename: str, file_size: float, file_type: str) -> None:
    """Render a compact file row with human-readable metadata."""
    icons = {"pdf": "▤", "csv": "▦", "xlsx": "▥", "txt": "≡", "docx": "▧"}
    safe_name = escape(str(filename))
    safe_type = escape(str(file_type).upper())
    icon = icons.get(str(file_type).lower(), "□")
    size_str = f"{file_size:.1f} KB" if file_size < 1024 else f"{file_size / 1024:.1f} MB"
    st.markdown(
        f"""
        <div class="file-item">
            <div class="file-icon">{icon}</div>
            <div style="min-width:0; flex:1"><div class="file-name">{safe_name}</div><div class="file-meta">{size_str} &nbsp;·&nbsp; {safe_type}</div></div>
            <div style="color:#68e6bd; font-size:.72rem">●</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chat_message(role: str, content: str, sources: Optional[List[str]] = None) -> None:
    """Render a user or assistant message, optionally with cited sources."""
    if role == "user":
        st.markdown(
            f'<div class="user-message"><div class="message-label user-label">◉ &nbsp; You</div>{content}</div>',
            unsafe_allow_html=True,
        )
        return

    source_html = ""
    if sources:
        source_items = "".join(f"<li>{escape(str(source))}</li>" for source in sources[:3])
        source_html = f'<div class="source-box"><strong>Referenced sources</strong><ul>{source_items}</ul></div>'
    st.markdown(
        f'<div class="assistant-message"><div class="message-label assistant-label">✦ &nbsp; FinanceRAG</div>{content}{source_html}</div>',
        unsafe_allow_html=True,
    )


def render_chat_spacer() -> None:
    """Reserve space for the fixed chat composer."""
    st.markdown('<div class="chat-bottom-spacer"></div>', unsafe_allow_html=True)


def render_pipeline_horizontal(steps: Dict[str, str]) -> None:
    """Render ingestion status as a compact visual pipeline."""
    icons_map = {"Upload": "↥", "Extract": "⌕", "Chunk": "⫴", "Embed": "◈", "Index": "▦", "Ready": "✓"}
    items = []
    for step_name, status in steps.items():
        icon = "✓" if status == "done" else "↻" if status == "active" else icons_map.get(step_name, "·")
        items.append(
            f'<div class="pipeline-step-h {escape(str(status))}"><div class="step-icon-h">{icon}</div><div class="step-name-h">{escape(str(step_name))}</div></div>'
        )
    st.markdown(f'<div class="pipeline-horizontal">{"".join(items)}</div>', unsafe_allow_html=True)


def render_upload_zone() -> None:
    """Render the visual drop-zone companion for st.file_uploader."""
    st.markdown(
        """
        <div class="upload-zone">
            <div class="upload-icon">↥</div>
            <div style="color:#edf6ff; font-size:.9rem; font-weight:700;">Drop your financial documents here</div>
            <div style="color:#7f8ba0; font-size:.72rem; margin-top:8px;">PDF &nbsp;·&nbsp; CSV &nbsp;·&nbsp; XLSX &nbsp;·&nbsp; TXT &nbsp;·&nbsp; DOCX</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
