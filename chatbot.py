import streamlit as st
from google import genai
from google.genai import types
import os
import base64

# ---------- PAGE SETUP & CONFIGURATION ----------
st.set_page_config(page_title="Rewoor AI Assistant", layout="centered")

# ---------- CUSTOM MODERN PREMIUM CSS STYLING (Safe Layering Version) ----------
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=300;400;500;600;700;800&display=swap');

    :root {
        --orange: #FF6B35;
        --blue: #3B82F6;
        --blue-light: #60A5FA;
        --white: #F5F7FF;
        --bg: #05070D;
    }

    /* Base Layout Reset */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: var(--bg) !important;
        color: var(--white) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Background Gradients Fixed - Inhe alag back layer par rakha hai taake text block na ho */
    [data-testid="stAppViewContainer"]::before,
    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: fixed;
        width: 450px;
        height: 450px;
        border-radius: 50%;
        filter: blur(150px);
        z-index: 0 !important;
        pointer-events: none;
        opacity: 0.25;
    }
    [data-testid="stAppViewContainer"]::before {
        background: var(--blue);
        top: -150px;
        left: -150px;
    }
    [data-testid="stAppViewContainer"]::after {
        background: var(--orange);
        bottom: -150px;
        right: -150px;
    }

    /* Main Content Container Force Foreground */
    [data-testid="stMainBlockContainer"] {
        position: relative;
        z-index: 10 !important;
        background: transparent !important;
    }

    /* Top Navigation bar ko clear karne ke liye */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Glass Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(10, 12, 20, 0.85) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
        z-index: 100 !important;
    }

    .sidebar-nav-title {
        color: #7C8AA5;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 1.8px;
        margin: 22px 0 10px 10px;
        font-weight: 700;
    }

    .sidebar-nav-item {
        padding: 11px 14px;
        margin: 5px 0px;
        border-radius: 12px;
        color: #E5E9F5;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.25s ease;
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        border: 1px solid transparent;
    }
    .sidebar-nav-item:hover {
        background: linear-gradient(90deg, rgba(59,130,246,0.15), rgba(255,107,53,0.15));
        border: 1px solid rgba(255,255,255,0.08);
        color: #FFFFFF;
        transform: translateX(3px);
    }

    /* Header Area */
    .chat-header {
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        margin-bottom: 1.5rem;
    }

    .brand-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 10px 0 0 0 !important;
        background: linear-gradient(90deg, var(--blue-light), var(--orange));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .brand-title span {
        -webkit-text-fill-color: var(--white);
        color: var(--white);
    }
    .brand-subtitle {
        color: #8993A8;
        font-size: 0.9rem;
        margin-top: 4px !important;
    }

    /* Chat Elements Visibility Patch */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 0.8rem 0rem !important;
    }

    [data-testid="stChatMessageUser"] {
        border-radius: 18px 18px 4px 18px !important;
        background: linear-gradient(135deg, var(--blue) 0%, var(--orange) 100%) !important;
        color: #FFFFFF !important;
        padding: 14px 18px !important;
        margin-left: auto !important;
        max-width: 80% !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.2) !important;
    }
    [data-testid="stChatMessageUser"] p {
        color: #FFFFFF !important;
    }

    [data-testid="stChatMessageAssistant"] {
        border-radius: 18px 18px 18px 4px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #E7EAF5 !important;
        padding: 14px 18px !important;
        max-width: 80% !important;
    }
    [data-testid="stChatMessageAssistant"] p {
        color: #E7EAF5 !important;
    }

    /* Input Box */
    [data-testid="stChatInput"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
    }

    /* Quick Action Buttons */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.03) !important;
        color: #E7EAF5 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 22px !important;
        padding: 6px 16px !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, rgba(59,130,246,0.2), rgba(255,107,53,0.2)) !important;
        border-color: var(--blue) !important;
        color: #FFF !important;
    }

    /* Typing Animation */
    .typing-dots {
        display: inline-flex;
        gap: 4px;
        align-items: center;
    }
    .typing-dots span {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--orange);
        animation: typingBounce 1.2s infinite ease-in-out;
    }
    .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
    .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes typingBounce {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
        30% { transform: translateY(-5px); opacity: 1; }
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

logo_exists = os.path.exists("logo.png")

# ---------- SIDEBAR COMPONENT ----------
with st.sidebar:
    if logo_exists:
        st.image("logo.png", width=120)
    else:
        st.markdown(
            "<h2 style='background:linear-gradient(90deg,#3B82F6,#FF6B35);"
            "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
            "font-weight:800; margin-left:10px;'>Rewoor</h2>",
            unsafe_allow_html=True,
        )

    st.markdown('<div class="sidebar-nav-title">Navigation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-nav-item">🤖 Chat Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-nav-item">🛍 Buy Dresses</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-nav-item">💰 Sell Dresses</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-nav-item">📦 My Orders</div>', unsafe_allow_html=True)

    st.markdown(
        '<div style="position: absolute; bottom: 20px; left: 20px; color: #5B6478; font-size: 0.75rem;">'
        'v3.0 • Powered by Gemini</div>',
        unsafe_allow_html=True,
    )

# ---------- HEADER SECTION ----------
st.markdown('<div class="chat-header">', unsafe_allow_html=True)
if logo_exists:
    st.markdown(
        f'<div style="display:flex; justify-content:center;">'
        f'<img src="data:image/png;base64,{base64.b64encode(open("logo.png", "rb").read()).decode()}" '
        f'width="70" style="border-radius:16px;"></div>',
        unsafe_allow_html=True,
    )
st.markdown('<h1 class="brand-title">Rewoor <span>Assistant</span></h1>', unsafe_allow_html=True)
st.markdown('<p class="brand-subtitle">Your sustainable fashion companion ✨</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- CHATBOT LOGIC ----------



# Client ko session state mein daal diya taake baar baar recreate ho kar close na ho
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

SYSTEM_PROMPT = """
Tum "Rewoor" naam ke ek online resale platform ke chatbot ho.
Rewoor ek aisa platform hai jahan log apni ek ya do baar pehni hui dresses kam qeemat par buy/sell kar sakte hain.
Hamesha friendly, madadgar aur short, clear jawab dena (2-3 lines max). Tumhara theme Orange, Blue, aur White hai.
Roman Urdu ya Urdu mein baat ho to usi zaban mein reply karo, English mein ho to English mein.
"""

if "chat_session" not in st.session_state:
    st.session_state.chat_session = st.session_state.gemini_client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    st.session_state.display_messages = [
        {"role": "assistant", "content": "Assalam-o-Alaikum! I am Rewoor's assistant. Do you want to sell a dress or buy one?"}
    ]

# Render chat history
for msg in st.session_state.display_messages:
    avatar_icon = "🤖" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])

# ---------- QUICK SUGGESTIONS (PILLS) ----------
st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
p1, p2, p3, _ = st.columns([1.2, 1.2, 1.2, 2])

pill_input = None
with p1:
    if st.button("🛍 How to Buy?"):
        pill_input = "How to buy dresses on Rewoor?"
with p2:
    if st.button("💰 How to Sell?"):
        pill_input = "How can I sell my dress?"
with p3:
    if st.button("📦 Track Order"):
        pill_input = "How do I track my order?"

# ---------- CHAT INPUT HANDLING ----------
user_input = st.chat_input("Apna sawal likhein...")
final_input = user_input if user_input else pill_input

if final_input:
    # 1. User message display & save
    with st.chat_message("user", avatar="👤"):
        st.markdown(final_input)
    st.session_state.display_messages.append({"role": "user", "content": final_input})
    
    # 2. Assistant loader & API call
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        placeholder.markdown(
            '<div class="typing-dots"><span></span><span></span><span></span></div>',
            unsafe_allow_html=True,
        )
        try:
            response = st.session_state.chat_session.send_message(message=final_input)
            reply = response.text
        except Exception as e:
            reply = f"Error: {e}"

        placeholder.markdown(reply)
        
    st.session_state.display_messages.append({"role": "assistant", "content": reply})
    
    # Quick rerun if pill was clicked to avoid double processing
    if pill_input:
        st.rerun()
