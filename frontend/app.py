import streamlit as st
import requests
import os
import time
import tempfile
from PIL import Image
from streamlit_mic_recorder import mic_recorder
import streamlit.components.v1 as components

# =========================
# 1. PAGE CONFIG - SABSE PEHLE
# =========================
st.set_page_config(
    page_title="EduAI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================
# 2. WHISPER MODEL LOAD
# =========================
#✅ Ye daalo
try:
    import whisper
    @st.cache_resource
    def load_whisper_model():
        return whisper.load_model("base")
    model = load_whisper_model()
    WHISPER_AVAILABLE = True
except:
    WHISPER_AVAILABLE = False
    model = None

# =========================
# 3. BASE DIRECTORY (Image path fix)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =========================
# 4. CUSTOM CSS
# =========================
st.markdown("""
<style>

/* ===================== */
/* ANIMATED BACKGROUND   */
/* ===================== */
@keyframes bgMove {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp {
    background: linear-gradient(
        270deg,
        #020617, #0f172a, #1e1b4b, #0f172a
    );
    background-size: 400% 400%;
    animation: bgMove 10s ease infinite;
    color: white;
}

/* ===================== */
/* SIDEBAR               */
/* ===================== */
section[data-testid="stSidebar"] {
    background: rgba(10, 15, 30, 0.97);
    border-right: 1px solid rgba(56,189,248,0.2);
    box-shadow: 4px 0 20px rgba(56,189,248,0.1);
}

/* ===================== */
/* ANIMATED TITLE        */
/* ===================== */
@keyframes titleGlow {
    0%   { text-shadow: 0 0 10px #38bdf8, 0 0 20px #818cf8; }
    50%  { text-shadow: 0 0 30px #ec4899, 0 0 60px #818cf8; }
    100% { text-shadow: 0 0 10px #38bdf8, 0 0 20px #818cf8; }
}

@keyframes titleFloat {
    0%   { transform: translateY(0px); }
    50%  { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
}

.main-title {
    font-size: 70px;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(to right, #38bdf8, #818cf8, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: titleFloat 3s ease-in-out infinite;
    margin-top: 20px;
}

/* ===================== */
/* SUBTITLE              */
/* ===================== */
@keyframes subtitleFade {
    0%   { opacity: 0.6; }
    50%  { opacity: 1; }
    100% { opacity: 0.6; }
}

.subtitle {
    text-align: center;
    font-size: 22px;
    color: #cbd5e1;
    margin-bottom: 40px;
    animation: subtitleFade 3s ease-in-out infinite;
}

/* ===================== */
/* INPUT BOX             */
/* ===================== */
.stTextInput > div > div > input {
    background-color: rgba(15, 23, 42, 0.9);
    color: white;
    border-radius: 15px;
    border: 1px solid #38bdf8;
    padding: 15px;
    font-size: 18px;
    box-shadow: 0 0 10px rgba(56,189,248,0.3);
    transition: 0.3s;
}

.stTextInput > div > div > input:focus {
    border: 1px solid #ec4899;
    box-shadow: 0 0 20px rgba(236,72,153,0.5);
}

/* ===================== */
/* NEON BUTTON           */
/* ===================== */
@keyframes btnGlow {
    0%   { box-shadow: 0 0 10px #2563eb, 0 0 20px #7c3aed; }
    50%  { box-shadow: 0 0 20px #38bdf8, 0 0 40px #ec4899; }
    100% { box-shadow: 0 0 10px #2563eb, 0 0 20px #7c3aed; }
}

.stButton > button {
    width: 100%;
    background: linear-gradient(to right, #2563eb, #7c3aed);
    color: white;
    border-radius: 15px;
    height: 55px;
    font-size: 20px;
    font-weight: bold;
    border: none;
    animation: btnGlow 3s ease-in-out infinite;
    transition: transform 0.2s;
}

.stButton > button:hover {
    transform: scale(1.04);
    background: linear-gradient(to right, #1d4ed8, #6d28d9);
}

/* ===================== */
/* NEON TABS             */
/* ===================== */
.stTabs [data-baseweb="tab"] {
    color: #94a3b8;
    font-size: 18px;
    font-weight: bold;
    padding: 10px 25px;
    border-radius: 10px;
    transition: 0.3s;
}

.stTabs [aria-selected="true"] {
    color: #38bdf8 !important;
    border-bottom: 3px solid #38bdf8 !important;
    text-shadow: 0 0 10px #38bdf8;
}

/* ===================== */
/* NEON DIVIDER          */
/* ===================== */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, #38bdf8, #ec4899, transparent);
    margin: 20px 0;
}

/* ===================== */
/* FOOTER                */
/* ===================== */
@keyframes footerGlow {
    0%   { color: #94a3b8; text-shadow: none; }
    50%  { color: #38bdf8; text-shadow: 0 0 10px #38bdf8; }
    100% { color: #94a3b8; text-shadow: none; }
}

.footer {
    text-align: center;
    margin-top: 50px;
    font-size: 16px;
    animation: footerGlow 3s ease-in-out infinite;
}

/* ===================== */
/* MOBILE RESPONSIVE     */
/* ===================== */

/* Mobile — 768px se chota */
@media (max-width: 768px) {

    /* Title chota karo */
    .main-title {
        font-size: 36px !important;
    }

    .subtitle {
        font-size: 15px !important;
        margin-bottom: 20px !important;
    }

    /* Button full width */
    .stButton > button {
        height: 48px !important;
        font-size: 16px !important;
        border-radius: 12px !important;
    }

    /* Input box */
    .stTextInput > div > div > input {
        font-size: 15px !important;
        padding: 10px !important;
    }

    /* Chat bubbles full width */
    .user-message, .ai-message {
        max-width: 95% !important;
        font-size: 15px !important;
        padding: 12px !important;
    }

    /* Tabs scroll karo */
    .stTabs [data-baseweb="tab-list"] {
        overflow-x: auto !important;
        flex-wrap: nowrap !important;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: 14px !important;
        padding: 8px 15px !important;
        white-space: nowrap !important;
    }

    /* Sidebar hide hoga mobile mein */
    section[data-testid="stSidebar"] {
        width: 100% !important;
    }

    /* Footer */
    .footer {
        font-size: 13px !important;
        margin-top: 30px !important;
    }

    /* Columns stack ho jayein */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
    }

    /* Flashcard mobile */
    div[style*="min-height: 200px"] {
        padding: 20px !important;
        font-size: 16px !important;
    }

    /* Mindmap scroll */
    div[style*="display:flex;flex-wrap:wrap"] {
        flex-direction: column !important;
        align-items: center !important;
    }
}

/* Tablet — 768px to 1024px */
@media (min-width: 768px) and (max-width: 1024px) {

    .main-title {
        font-size: 50px !important;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: 16px !important;
        padding: 8px 18px !important;
    }
}
            
</style>
""", unsafe_allow_html=True)
# =========================
# 5. SIDEBAR
# =========================
with st.sidebar:

    st.markdown("## 🤖 EduAI")
    st.write("### Your Personal AI Study Assistant")
    st.write("---")

    # Developer Image - FIXED PATH
    image_path = os.path.join(BASE_DIR, "assets", "himanshu.jpg")

    if os.path.exists(image_path):
        st.image(image_path, width=180)
    else:
        st.warning("⚠️ Developer image not found! assets/himanshu.jpg rakho.")

    # Developer Info
    st.markdown("""
## 👨‍💻 Developer

### Himanshu Shekhar ⚡

🎓 Student Developer  
🚀 Creator of EduAI  
💻 Python | AI | FastAPI | Streamlit  
📚 Passionate about AI & Innovation

---

### 🌟 About Me

I am building futuristic AI tools  
to help students learn smarter.

EduAI is my personal AI assistant  
project with PDF Chat, Voice Tutor,  
Memory Chat and more.

---

### 🔗 Connect With Me

📧 himanshushekhar82100@gmail.com  
🐙 github.com/himanshu  
💼 linkedin.com/in/himanshu
""")

    st.write("---")

    st.markdown("## 🚀 Features")
    st.write("✅ PDF Chat")
    st.write("✅ Voice Tutor")
    st.write("✅ Memory Chat")
    st.write("✅ Quiz Generator")
    st.write("✅ Smart Notes")

    st.write("---")

    # PDF Upload
    uploaded_file = st.file_uploader(
        "📄 Upload PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:
        upload_dir = os.path.join(BASE_DIR, "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        upload_path = os.path.join(upload_dir, uploaded_file.name)

        with open(upload_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"✅ PDF Upload Hua: {uploaded_file.name}")

    st.write("---")

    # Clear Chat Button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# =========================
# 6. MAIN TITLE
# =========================
st.markdown(
    '<div class="main-title">EduAI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your futuristic AI-powered learning companion 🚀</div>',
    unsafe_allow_html=True
)

st.write("---")
tab1, tab2 = st.tabs(["💬 Chat", "🚀 Smart Features"])

with tab1:

    # =========================
    # 7. CHAT HISTORY INIT
    # =========================
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # =========================
    # 8. VOICE INPUT
    # =========================
    voice = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop Recording",
        just_once=True
    )

    voice_input = ""

    if voice:
        audio_bytes = voice["bytes"]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_webm:
            temp_webm.write(audio_bytes)
            webm_path = temp_webm.name

        wav_path = webm_path.replace(".webm", ".wav")

        from pydub import AudioSegment
        audio = AudioSegment.from_file(webm_path, format="webm")
        audio.export(wav_path, format="wav")

        with st.spinner("🎤 Voice samajh raha hoon..."):
            result = model.transcribe(wav_path, fp16=False)
            voice_input = result["text"].strip()

        st.session_state.user_input = voice_input
        st.success(f"🎤 Aapne kaha: **{voice_input}**")

        os.remove(webm_path)
        os.remove(wav_path)

    # =========================
    # 9. TEXT INPUT
    # =========================
    text_input = st.text_input(
        "💬 Apna sawaal yahan likho:",
        value=st.session_state.get("user_input", ""),
        placeholder="Koi bhi sawaal pucho..."
    )

    user_input = text_input.strip()

    # =========================
    # 10. ASK BUTTON
    # =========================
    if st.button("✨ Ask EduAI"):

        if user_input:

            st.session_state.user_input = ""

            st.session_state.messages.append(
                {"role": "user", "content": user_input}
            )

            try:
                if uploaded_file is not None:
                    url = f"http://127.0.0.1:8000/pdfchat?query={user_input}&filename={uploaded_file.name}"
                else:
                    url = f"http://127.0.0.1:8000/chat?query={user_input}"

                with st.spinner("🤖 EduAI soch raha hai..."):
                    response = requests.get(url, timeout=30)
                    data = response.json()
                    ai_response = data["response"]

                st.session_state.messages.append(
                    {"role": "ai", "content": ai_response}
                )

            except requests.exceptions.ConnectionError:
                st.session_state.messages.append(
                    {"role": "ai", "content": "⚠️ Backend server nahi mila! FastAPI server start karo."}
                )

            except Exception as e:
                st.session_state.messages.append(
                    {"role": "ai", "content": f"❌ Error aaya: {str(e)}"}
                )

            st.rerun()

        else:
            st.warning("⚠️ Pehle kuch likho ya bolo!")

    # =========================
    # 11. CHAT HISTORY DISPLAY
    # =========================
    for message in st.session_state.messages:

        if message["role"] == "user":
            st.markdown(
                f"""
                <div style="
                    display:flex;
                    justify-content:flex-end;
                    margin-top:15px;
                ">
                    <div style="
                        background:linear-gradient(to right,#2563eb,#3b82f6);
                        padding:15px 20px;
                        border-radius:18px;
                        max-width:70%;
                        color:white;
                        font-size:18px;
                        box-shadow:0 0 10px rgba(37,99,235,0.4);
                    ">
                        👤 <b>You</b><br><br>
                        {message["content"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.markdown(
                f"""
                <div style="
                    display:flex;
                    justify-content:flex-start;
                    margin-top:15px;
                ">
                    <div style="
                        background:rgba(30,41,59,0.95);
                        padding:15px 20px;
                        border-radius:18px;
                        max-width:70%;
                        color:white;
                        font-size:18px;
                        border-left:5px solid #38bdf8;
                        box-shadow:0 0 10px rgba(56,189,248,0.3);
                    ">
                        🤖 <b>EduAI</b><br><br>
                        {message["content"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================
# TAB 2 - SMART NOTES
# =========================
with tab2:

    # ==============================
    # TABS INSIDE TAB2
    # ==============================
    subtab1, subtab2, subtab3 = st.tabs([
        "📝 Smart Notes",
        "🃏 Flashcards",
        "🧠 Mindmap"
    ])

    # ==============================
    # SUBTAB 1 — SMART NOTES
    # ==============================
    with subtab1:
        with subtab1:

         st.markdown("## 📝 Smart Notes Generator")
        st.write("Koi bhi topic dalo — AI notes banayega!")
        st.write("---")

        if "generated_notes" not in st.session_state:
            st.session_state.generated_notes = ""

        if "notes_topic" not in st.session_state:
            st.session_state.notes_topic = ""

        topic = st.text_input(
            "📚 Topic likho:",
            placeholder="e.g. Photosynthesis, Python Functions..."
        )

        if st.button("✨ Notes Generate Karo"):
            if topic:
                with st.spinner("📝 Notes ban rahe hain..."):
                    url = f"http://127.0.0.1:8000/generate-notes?topic={topic}"
                    response = requests.get(url, timeout=60)
                    data = response.json()
                    st.session_state.generated_notes = data["notes"]
                    st.session_state.notes_topic = topic
                st.success("✅ Notes ready!")
            else:
                st.warning("⚠️ Topic likho pehle!")

        if st.session_state.generated_notes:
            st.write("---")
            st.markdown(st.session_state.generated_notes)
            st.write("---")

            if st.button("📥 PDF Download Karo"):

                from reportlab.lib.pagesizes import A4
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
                from reportlab.lib.units import inch
                from reportlab.lib import colors
                import io, re

                def clean_line(text):
                    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
                    text = re.sub(r'\*(.*?)\*', r'\1', text)
                    text = re.sub(r'[^\x00-\x7F]+', '', text)
                    return text.strip()

                buffer = io.BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=A4,
                    rightMargin=40, leftMargin=40,
                    topMargin=40, bottomMargin=40)

                styles = getSampleStyleSheet()
                h1 = ParagraphStyle('H1', parent=styles['Heading1'],
                    fontSize=18, textColor=colors.HexColor('#2563eb'), spaceAfter=10)
                h2 = ParagraphStyle('H2', parent=styles['Heading2'],
                    fontSize=14, textColor=colors.HexColor('#0096c8'), spaceAfter=6)
                normal = ParagraphStyle('N', parent=styles['Normal'],
                    fontSize=11, spaceAfter=4)

                story = []
                story.append(Paragraph("EduAI - Smart Notes", h1))
                story.append(Paragraph("Developer: Himanshu Shekhar", normal))
                story.append(Spacer(1, 0.2 * inch))

                for line in st.session_state.generated_notes.split("\n"):
                    line = line.strip()
                    if not line:
                        story.append(Spacer(1, 0.1 * inch))
                        continue
                    clean = clean_line(line)
                    if not clean:
                        continue
                    if clean.startswith("# "):
                        story.append(Paragraph(clean[2:], h1))
                    elif clean.startswith("## "):
                        story.append(Paragraph(clean[3:], h2))
                    elif clean.startswith("- ") or clean.startswith("* "):
                        story.append(Paragraph("• " + clean[2:], normal))
                    else:
                        story.append(Paragraph(clean, normal))

                doc.build(story)

                st.download_button(
                    label="⬇️ PDF Download Karo",
                    data=buffer.getvalue(),
                    file_name=f"Notes_{st.session_state.notes_topic}.pdf",
                    mime="application/pdf"
                )
        # Tumhara existing Smart Notes code yahan rahega
        # (topic input se lekar PDF download tak)

    # ==============================
    # SUBTAB 2 — FLASHCARDS
    # ==============================
    with subtab2:

        st.markdown("## 🃏 Flashcard Generator")
        st.write("Topic deke AI flashcards banao!")
        st.write("---")

        if "flashcards" not in st.session_state:
            st.session_state.flashcards = []

        if "card_index" not in st.session_state:
            st.session_state.card_index = 0

        if "show_answer" not in st.session_state:
            st.session_state.show_answer = False

        # Topic input
        fc_topic = st.text_input(
            "📚 Flashcard topic:",
            placeholder="e.g. Photosynthesis, Python..."
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✨ Topic se Flashcards"):
                if fc_topic:
                    with st.spinner("🃏 Flashcards ban rahe hain..."):
                        url = f"http://127.0.0.1:8000/generate-flashcards?topic={fc_topic}"
                        response = requests.get(url, timeout=60)
                        data = response.json()
                        st.session_state.flashcards = data["flashcards"]
                        st.session_state.card_index = 0
                        st.session_state.show_answer = False
                    st.success("✅ Flashcards ready!")
                else:
                    st.warning("⚠️ Topic likho pehle!")

        with col2:
            if st.button("📝 Notes se Flashcards"):
                if st.session_state.generated_notes:
                    with st.spinner("🃏 Notes se flashcards ban rahe hain..."):
                        notes_topic = st.session_state.get("notes_topic", "Notes")
                        url = f"http://127.0.0.1:8000/generate-flashcards?topic={notes_topic}"
                        response = requests.get(url, timeout=60)
                        data = response.json()
                        st.session_state.flashcards = data["flashcards"]
                        st.session_state.card_index = 0
                        st.session_state.show_answer = False
                    st.success("✅ Flashcards ready!")
                else:
                    st.warning("⚠️ Pehle Smart Notes tab mein notes banao!")

        # Flashcard Display
        if st.session_state.flashcards:

            cards = st.session_state.flashcards
            idx = st.session_state.card_index
            total = len(cards)

            st.write("---")
            st.markdown(f"**Card {idx + 1} of {total}**")

            # Progress bar
            st.progress((idx + 1) / total)

            # Card display
            card = cards[idx]

            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(to right, #1e293b, #0f172a);
                    border: 2px solid #38bdf8;
                    border-radius: 20px;
                    padding: 40px;
                    text-align: center;
                    min-height: 200px;
                    margin: 20px 0;
                    box-shadow: 0 0 20px rgba(56,189,248,0.3);
                ">
                    <div style="color:#38bdf8; font-size:14px; margin-bottom:10px;">
                        QUESTION
                    </div>
                    <div style="color:white; font-size:22px; font-weight:bold;">
                        {card['question']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.session_state.show_answer:
                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(to right, #064e3b, #065f46);
                        border: 2px solid #34d399;
                        border-radius: 20px;
                        padding: 40px;
                        text-align: center;
                        min-height: 150px;
                        margin: 10px 0;
                        box-shadow: 0 0 20px rgba(52,211,153,0.3);
                    ">
                        <div style="color:#34d399; font-size:14px; margin-bottom:10px;">
                            ANSWER
                        </div>
                        <div style="color:white; font-size:20px;">
                            {card['answer']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Buttons
            st.write("")
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("⬅️ Previous"):
                    if idx > 0:
                        st.session_state.card_index -= 1
                        st.session_state.show_answer = False
                        st.rerun()

            with col2:
                if st.button("👁️ Show Answer" if not st.session_state.show_answer else "🙈 Hide Answer"):
                    st.session_state.show_answer = not st.session_state.show_answer
                    st.rerun()

            with col3:
                if st.button("➡️ Next"):
                    if idx < total - 1:
                        st.session_state.card_index += 1
                        st.session_state.show_answer = False
                        st.rerun()

    # ==============================
    # SUBTAB 3 — MINDMAP
    # ==============================
with subtab3:

    st.markdown("## 🧠 Mindmap Generator")
    st.write("Topic deke interactive mindmap banao!")
    st.write("---")

    if "mindmap_data" not in st.session_state:
        st.session_state.mindmap_data = {}

    mm_topic = st.text_input(
        "🧠 Mindmap topic:",
        placeholder="e.g. Machine Learning, World War 2..."
    )
    if mm_topic:
        st.session_state.mm_topic = mm_topic

    if st.button("✨ Mindmap Generate Karo"):
        if mm_topic:
            with st.spinner("🧠 Mindmap ban raha hai..."):
                url = f"http://127.0.0.1:8000/generate-mindmap?topic={mm_topic}"
                response = requests.get(url, timeout=60)
                data = response.json()
                st.session_state.mindmap_data = data["mindmap"]
                st.session_state.mm_topic = mm_topic
            st.success("✅ Mindmap ready!")
        else:
            st.warning("⚠️ Topic likho pehle!")

    if st.session_state.mindmap_data:

        mm = st.session_state.mindmap_data
        st.write("---")

        branches = mm.get("branches", [])
        center = mm.get("center", st.session_state.get("mm_topic", "Mindmap"))

        colors_list = [
            "#3b82f6", "#ec4899", "#10b981",
            "#f59e0b", "#8b5cf6"
        ]

        branches_html = ""
        for i, branch in enumerate(branches):
            color = colors_list[i % len(colors_list)]
            points_html = "".join([
                f'<li style="margin:4px 0;">{p}</li>'
                for p in branch.get("points", [])
            ])
            branches_html += f"""<div style="background:rgba(30,41,59,0.9);border:2px solid {color};border-radius:15px;padding:15px 20px;margin:10px;min-width:200px;max-width:220px;box-shadow:0 0 15px {color}44;"><div style="color:{color};font-weight:bold;font-size:16px;margin-bottom:8px;">{branch['title']}</div><ul style="color:#cbd5e1;font-size:13px;padding-left:15px;margin:0;">{points_html}</ul></div>"""

        mindmap_html = f"""
        <div style="background:linear-gradient(to right,#020617,#0f172a);border-radius:20px;padding:30px;margin:10px 0;">
            <div style="text-align:center;background:linear-gradient(to right,#2563eb,#7c3aed);color:white;font-size:24px;font-weight:bold;padding:15px 30px;border-radius:50px;display:inline-block;width:100%;box-sizing:border-box;margin-bottom:30px;">
                {center}
            </div>
            <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:10px;">
                {branches_html}
            </div>
        </div>
        """

        # ✅ YAHI FIX HAI — st.markdown ki jagah ye use karo
        st.components.v1.html(mindmap_html, height=600, scrolling=True)

            # PDF Download
    st.write("---")
    if st.button("📥 Mindmap PDF Download"):

                from reportlab.lib.pagesizes import A4
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
                from reportlab.lib.units import inch
                from reportlab.lib import colors
                import io

                buffer = io.BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=A4,
                    rightMargin=40, leftMargin=40,
                    topMargin=40, bottomMargin=40)

                styles = getSampleStyleSheet()

                h1 = ParagraphStyle('H1', parent=styles['Heading1'],
                    fontSize=20, textColor=colors.HexColor('#2563eb'), spaceAfter=12)
                h2 = ParagraphStyle('H2', parent=styles['Heading2'],
                    fontSize=14, textColor=colors.HexColor('#0096c8'), spaceAfter=6)
                normal = ParagraphStyle('N', parent=styles['Normal'],
                    fontSize=11, spaceAfter=4)

                story = []
                story.append(Paragraph(f"EduAI - Mindmap: {center}", h1))
                story.append(Paragraph("Developer: Himanshu Shekhar", normal))
                story.append(Spacer(1, 0.3 * inch))

                for branch in branches:
                    story.append(Paragraph(branch['title'], h2))
                    for point in branch.get('points', []):
                        story.append(Paragraph(f"• {point}", normal))
                    story.append(Spacer(1, 0.15 * inch))

                doc.build(story)

                st.download_button(
                    label="⬇️ Mindmap PDF Download Karo",
                    data=buffer.getvalue(),
                    file_name=f"Mindmap_{center}.pdf",
                    mime="application/pdf"
                )
# =========================
# 12. FOOTER
# =========================
st.markdown(
    '<div class="footer">⚡ Developed with ❤️ by Himanshu Shekhar ⚡</div>',
    unsafe_allow_html=True
)