import os
import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage

# Import your compiled LangGraph app
from main import app

st.set_page_config(
    page_title="Traviara | AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# --- CUSTOM CSS (Midnight Teal & Emerald Theme) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

html, body, .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #040d12; /* Deep midnight base */
}

/* ── Hero ── */
.hero-wrapper {
    position: relative;
    border-radius: 24px;
    overflow: hidden;
    margin-bottom: 2rem;
    height: 300px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.hero-bg {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    filter: brightness(0.4) saturate(1.2);
    position: absolute;
    top: 0; left: 0;
}
.hero-content {
    position: relative;
    z-index: 2;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}
.hero-badge {
    background: rgba(45, 212, 191, 0.15);
    border: 1px solid rgba(45, 212, 191, 0.4);
    color: #5eead4 !important;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.4rem 1rem;
    border-radius: 30px;
    margin-bottom: 1rem;
    backdrop-filter: blur(4px);
    display: inline-block;
}
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 0.8rem;
    line-height: 1.1;
    letter-spacing: -0.02em;
}
.hero-sub {
    color: #94a3b8;
    font-size: 1.05rem;
    max-width: 600px;
    font-weight: 400;
}

/* ── Input card ── */
.input-label {
    color: #5eead4;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* ── Quick destinations ── */
.dest-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin: 0.8rem 0 1.2rem;
}
.dest-chip {
    background: #0f172a;
    border: 1px solid #1e293b;
    color: #f8fafc;
    padding: 0.35rem 0.85rem;
    border-radius: 20px;
    font-size: 0.82rem;
    cursor: pointer;
    transition: all 0.2s;
}
.dest-chip:hover { background: #134e4a; border-color: #2dd4bf; color: #fff; }

/* ── Generate button ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #0d9488 0%, #0369a1 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 2.5rem !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    width: 100% !important;
    box-shadow: 0 4px 20px rgba(13, 148, 136, 0.4) !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stButton"] > button:hover {
    box-shadow: 0 6px 28px rgba(13, 148, 136, 0.6) !important;
    transform: translateY(-2px) !important;
    background: linear-gradient(135deg, #14b8a6 0%, #0284c7 100%) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ── Agent status cards ── */
[data-testid="stStatusWidget"] {
    background: #0b1a20 !important;
    border: 1px solid #11323b !important;
    border-radius: 14px !important;
}
[data-testid="stStatusWidget"] > div:first-child {
    background: #0b1a20 !important;
    border-radius: 14px 14px 0 0 !important;
}
[data-testid="stStatusWidget"] details,
[data-testid="stStatusWidget"] details > div,
[data-testid="stStatusWidget"] [data-testid="stVerticalBlock"] {
    background: #061014 !important;
    color: #f8fafc !important;
    padding: 0.25rem 0.5rem !important;
}
[data-testid="stStatusWidget"] * { color: #f8fafc !important; }
[data-testid="stStatusWidget"] a { color: #2dd4bf !important; }
[data-testid="stStatusWidget"] hr { border-color: #11323b !important; }

/* ── Section headers ── */
.sec-head {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2rem 0 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #11323b;
}
.sec-head span { font-size: 1.2rem; font-weight: 700; color: #ccfbf1; }

/* ── Metric bar ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
}
.metric-box {
    flex: 1;
    background: #081419;
    border: 1px solid #11323b;
    border-radius: 16px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
.metric-val { font-size: 2rem; font-weight: 800; color: #2dd4bf; }
.metric-lbl { font-size: 0.8rem; color: #94a3b8 !important; margin-top: 0.3rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600;}

/* ── Final plan ── */
.final-card {
    background: linear-gradient(160deg, #081419 0%, #040d12 100%);
    border: 1px solid #11323b;
    border-left: 4px solid #0d9488;
    border-radius: 16px;
    padding: 2rem;
    line-height: 1.8;
    color: #e2e8f0;
    font-size: 1rem;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}

/* ── Save bar ── */
.save-bar {
    background: #081419;
    border: 1px solid #11323b;
    border-radius: 12px;
    padding: 0.85rem 1.2rem;
    color: #94a3b8 !important;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}
.save-bar code { color: #5eead4 !important; background: #040d12 !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #040a0f !important;
    border-right: 1px solid #0f172a !important;
}
.sidebar-chip {
    background: #0b1a20;
    border: 1px solid #11323b;
    border-radius: 8px;
    padding: 0.5rem 0.8rem;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
    color: #94a3b8;
    font-weight: 500;
}
.sidebar-title { color: #ccfbf1; font-size: 1.05rem; font-weight: 700; margin: 1.2rem 0 0.6rem; letter-spacing: 0.02em;}

/* Hide branding */
#MainMenu, footer, header { visibility: hidden; }

/* Inputs & Forms */
.stTextArea textarea {
    background: #081419 !important;
    border: 1px solid #11323b !important;
    border-radius: 12px !important;
    color: #f8fafc !important;
    font-size: 1rem !important;
    resize: none !important;
    padding: 1rem !important;
}
.stTextArea textarea:focus, input[type="text"]:focus, .stTextInput input:focus {
    border-color: #2dd4bf !important;
    box-shadow: 0 0 0 2px rgba(45, 212, 191, 0.2) !important;
}
.stTextArea textarea::placeholder { color: #475569 !important; }
input[type="text"], .stTextInput input {
    background: #0b1a20 !important;
    border: 1px solid #11323b !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
}
input[type="text"]::placeholder { color: #475569 !important; }
.stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label {
    color: #5eead4 !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
}

/* Markdown elements */
.stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th { color: #e2e8f0 !important; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #f8fafc !important; font-weight: 700; }
.stMarkdown code {
    background: #0b1a20 !important;
    color: #5eead4 !important;
    padding: 0.2em 0.5em;
    border-radius: 6px;
}
.stAlert { background: #0b1a20 !important; border-radius: 12px !important; border: 1px solid #11323b !important;}
.stAlert p, .stAlert div { color: #f8fafc !important; }
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] .stMarkdown { color: #94a3b8 !important; }
section[data-testid="stSidebar"] hr { border-color: #11323b !important; }

/* Download button */
div[data-testid="stDownloadButton"] > button {
    background: #0b1a20 !important;
    color: #f8fafc !important;
    border: 1px solid #2dd4bf !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: #11323b !important;
    color: #5eead4 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sidebar-title'>🌍 Traviara Planner</div>", unsafe_allow_html=True)
    st.markdown("---")

    thread_id = st.text_input("👤 User ID", value="guest_session",
                              help="Your session ID — keeps travel history across queries")

    st.markdown("<div class='sidebar-title'>Powered by</div>", unsafe_allow_html=True)
    for tech in ["🔗 LangGraph", "🧠 Groq · LLaMA 3.3 70B", "🐘 PostgreSQL", "🔍 Tavily Search", "✈️ AviationStack"]:
        st.markdown(f"<div class='sidebar-chip'>{tech}</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-title'>Agent Pipeline</div>", unsafe_allow_html=True)
    for step in ["① Flight Agent", "② Hotel Agent", "③ Itinerary Agent", "④ Final Agent"]:
        st.markdown(f"<div class='sidebar-chip'>{step}</div>", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <img class="hero-bg"
         src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1400&q=80"
         alt="airplane above clouds"/>
    <div class="hero-content">
        <div class="hero-badge">✦ Multi-Agent AI System</div>
        <div class="hero-title">✈️ Traviara</div>
        <div class="hero-sub">Four specialized agents working seamlessly to search flights, curate hotels, and craft your perfect itinerary autonomously.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Destination image strip ───────────────────────────────────────────────────
DESTINATIONS = [
    ("🇬🇷 Santorini",  "https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?w=300&q=70"),
    ("🇨🇭 Swiss Alps", "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=300&q=70"),
    ("🇲🇻 Maldives",   "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=300&q=70"),
    ("🇺🇸 New York",   "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=300&q=70"),
    ("🇿🇦 Cape Town",  "https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=300&q=70"),
]

cols = st.columns(5)
for col, (name, img_url) in zip(cols, DESTINATIONS):
    with col:
        st.markdown(f"""
        <div style="border-radius:14px;overflow:hidden;position:relative;height:100px;cursor:pointer;box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
            <img src="{img_url}" style="width:100%;height:100%;object-fit:cover;filter:brightness(0.6);" />
            <div style="position:absolute;bottom:10px;left:0;right:0;text-align:center;
                        color:#fff;font-size:0.85rem;font-weight:700;letter-spacing:0.05em;">{name}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown("<div class='input-label'>🗺️ Describe your trip</div>", unsafe_allow_html=True)

QUICK = ["Santorini 5 days", "Swiss Alps skiing 7 days", "5-day NYC tech tour", "Maldives relaxation under $5k"]
qcols = st.columns(len(QUICK))
quick_fill = ""
for qc, label in zip(qcols, QUICK):
    with qc:
        if st.button(label, key=f"q_{label}"):
            quick_fill = label

user_query = st.text_area(
    "",
    value=quick_fill,
    placeholder="e.g. Plan a complete 7-day trip to the Swiss Alps including flights, hotels and sightseeing",
    height=110,
    label_visibility="collapsed",
)

generate = st.button("🚀  Generate My Travel Plan", use_container_width=True)

# ── Agent pipeline ────────────────────────────────────────────────────────────
AGENT_META = {
    "flight_agent":    ("✈️", "Flight Agent"),
    "hotel_agent":     ("🏨", "Hotel Agent"),
    "itinerary_agent": ("🗓️", "Itinerary Agent"),
    "final_agent":     ("🧠", "Final Agent"),
}

if generate:
    if not user_query.strip():
        st.warning("Please describe your trip first.")
    else:
        config = {"configurable": {"thread_id": thread_id}}
        collected = {"flight_results": "", "hotel_results": "",
                     "itinerary": "", "final_response": "", "llm_calls": 0}

        st.markdown("---")
        st.markdown("<div class='sec-head'><span>🤖 Agent Pipeline — Live</span></div>",
                    unsafe_allow_html=True)

        for chunk in app.stream(
            {
                "messages": [HumanMessage(content=user_query)],
                "user_query": user_query,
                "flight_results": "",
                "hotel_results": "",
                "itinerary": "",
                "llm_calls": 0,
            },
            config=config,
            stream_mode="updates",
        ):
            for node_name, state_update in chunk.items():
                icon, label = AGENT_META.get(node_name, ("🔧", node_name))

                with st.status(f"{icon}  {label}", state="complete", expanded=True):
                    if node_name == "flight_agent":
                        text = state_update.get("flight_results", "")
                        collected["flight_results"] = text
                        st.markdown(text or "_No flight data returned._")

                    elif node_name == "hotel_agent":
                        text = state_update.get("hotel_results", "")
                        collected["hotel_results"] = text
                        st.markdown(text or "_No hotel data returned._")

                    elif node_name == "itinerary_agent":
                        text = state_update.get("itinerary", "")
                        collected["itinerary"] = text
                        st.markdown(text or "_No itinerary generated._")

                    elif node_name == "final_agent":
                        msgs = state_update.get("messages", [])
                        text = msgs[-1].content if msgs else ""
                        collected["final_response"] = text
                        st.markdown(text or "_No final response._")

                    collected["llm_calls"] = state_update.get("llm_calls", collected["llm_calls"])

        # Metrics
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box"><div class="metric-val">4</div><div class="metric-lbl">Agents Run</div></div>
            <div class="metric-box"><div class="metric-val">{collected['llm_calls']}</div><div class="metric-lbl">LLM Calls</div></div>
            <div class="metric-box"><div class="metric-val">✅</div><div class="metric-lbl">Status</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Final plan card
        if collected["final_response"]:
            st.markdown("<div class='sec-head'><span>🧠 Final Travel Plan</span></div>",
                        unsafe_allow_html=True)
            st.markdown(f"<div class='final-card'>{collected['final_response']}</div>",
                        unsafe_allow_html=True)

        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"traviara_plan_{timestamp}.md"
        save_dir = os.path.join(os.path.dirname(__file__), "travel_plans")
        os.makedirs(save_dir, exist_ok=True)

        file_content = f"""# Traviara Travel Plan
**Query:** {user_query}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**User ID:** {thread_id}

---

## ✈️ Flight Information
{collected['flight_results'] or 'N/A'}

---

## 🏨 Hotel Information
{collected['hotel_results'] or 'N/A'}

---

## 🗓️ Itinerary
{collected['itinerary'] or 'N/A'}

---

## 🧠 Final Travel Plan
{collected['final_response'] or 'N/A'}

---
*LLM Calls: {collected['llm_calls']}*
"""
        with open(os.path.join(save_dir, filename), "w", encoding="utf-8") as f:
            f.write(file_content)

        dl_col, info_col = st.columns([1, 3])
        with dl_col:
            st.download_button("⬇️ Download Plan", data=file_content,
                               file_name=filename, mime="text/markdown",
                               use_container_width=True)
        with info_col:
            st.markdown(f"<div class='save-bar'>📁 Auto-saved → <code>travel_plans/{filename}</code></div>",
                        unsafe_allow_html=True)