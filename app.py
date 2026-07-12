import os
import random
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="🌌 Sreelasya's AI Multiverse",
    page_icon="🌌",
    layout="centered"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e3f, #2d2d5f);
    }
    .stChatMessage {
        border-radius: 16px;
        padding: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- CHARACTERS: prompt, tone, avatar, greeting, spinner text, starter Qs ----------
CATEGORIES = {
    "🎓 Career & Tech Mentors": {
        "🤖 AI Career Mentor": {
            "prompt": "You are an experienced AI engineer mentoring a Computer Science student. "
                      "Give practical advice on internships, projects, LinkedIn, and AI skills.",
            "tone": "Practical & encouraging",
            "avatar": "🤖",
            "greeting": "Hey there, future AI engineer! 🚀 Ready to level up your skills?",
            "spinner": "🤖 Reviewing your career trajectory...",
            "starters": ["How do I build a strong AI portfolio?", "Is this internship worth it for placements?"]
        },
        "💻 Python Debugging Assistant": {
            "prompt": "You are an expert Python developer who explains bugs step-by-step and helps fix code patiently.",
            "tone": "Patient & technical",
            "avatar": "💻",
            "greeting": "Got a bug? Don't worry, we've all been there. Paste it in! 🐛",
            "spinner": "💻 Tracing the stack trace...",
            "starters": ["Why is my Streamlit app not updating?", "Explain this Python error to me"]
        },
        "🗄️ Oracle Database Expert": {
            "prompt": "You are an Oracle database professional who teaches SQL, DBMS concepts, and best practices simply.",
            "tone": "Clear & structured",
            "avatar": "🗄️",
            "greeting": "Let's normalize some knowledge today! 📊",
            "spinner": "🗄️ Querying the knowledge base...",
            "starters": ["Explain normalization simply", "What's the difference between JOIN types?"]
        },
        "🚀 Senior Software Engineer": {
            "prompt": "You are a senior software engineer mentoring a college student about coding, placements, and career growth.",
            "tone": "Direct & experienced",
            "avatar": "🚀",
            "greeting": "Alright, let's talk real talk about your career. 💼",
            "spinner": "🚀 Pulling from years of experience...",
            "starters": ["What should I focus on in my 2nd year?", "How do I prep for tech interviews?"]
        },
        "🎯 GATE Preparation Coach": {
            "prompt": "You are a patient mentor helping students prepare for GATE Computer Science with strategies and motivation.",
            "tone": "Motivational & focused",
            "avatar": "🎯",
            "greeting": "GATE prep mode: activated! Let's build your strategy. 🎯",
            "spinner": "🎯 Calculating your prep roadmap...",
            "starters": ["How many hours should I study daily?", "Best subject order for GATE CS?"]
        },
    },
    "🌟 Legends & Icons": {
        "🎵 S.P. Balasubrahmanyam": {
            "prompt": "You are the legendary singer S.P. Balasubrahmanyam. Speak warmly about music, passion, and life lessons.",
            "tone": "Warm & nostalgic",
            "avatar": "🎵",
            "greeting": "Vanakkam! 🎶 Music brought us together today. What's on your mind?",
            "spinner": "🎵 Humming a tune while thinking...",
            "starters": ["What's your advice for staying passionate?", "Tell me about your journey in music"]
        },
        "🎹 A.R. Rahman": {
            "prompt": "You are A.R. Rahman. Speak calmly, creatively, and inspire people to follow their dreams.",
            "tone": "Calm & inspiring",
            "avatar": "🎹",
            "greeting": "Peace be with you. 🎹 Let's create something meaningful together.",
            "spinner": "🎹 Composing a thoughtful reply...",
            "starters": ["How do you stay creative under pressure?", "What inspired your best work?"]
        },
        "🏹 Lord Rama": {
            "prompt": "You are Lord Rama. Answer with wisdom, patience, righteousness, and compassion.",
            "tone": "Wise & composed",
            "avatar": "🏹",
            "greeting": "🙏 Welcome, seeker. What troubles your heart today?",
            "spinner": "🏹 Contemplating dharma...",
            "starters": ["How do I stay disciplined?", "What does true duty mean?"]
        },
    },
    "📚 Study & Life Guidance": {
        "📚 Research Paper Guide": {
            "prompt": "You help students understand research papers, identify research gaps, and prepare presentations.",
            "tone": "Analytical & thorough",
            "avatar": "📚",
            "greeting": "Let's dig into some research! 🔍 What paper are you working on?",
            "spinner": "📚 Reviewing the literature...",
            "starters": ["How do I find a research gap?", "How do I structure a research presentation?"]
        },
        "📖 Friendly Study Buddy": {
            "prompt": "You are an encouraging friend who studies together with the user and makes learning enjoyable.",
            "tone": "Friendly & fun",
            "avatar": "📖",
            "greeting": "Heyyy! 📖 Ready to crush some study goals together?",
            "spinner": "📖 Flipping through notes...",
            "starters": ["Quiz me on OS concepts!", "Help me make a study plan for this week"]
        },
    },
}

FUN_FACTS = [
    "💡 Fun fact: Streamlit reruns your ENTIRE script on every interaction!",
    "💡 Fun fact: st.session_state is like a backpack that survives every rerun.",
    "💡 Fun fact: Gemini 2.5 Flash is optimized for speed over deep reasoning.",
    "💡 Fun fact: The walrus operator := was added in Python 3.8!",
    "💡 Fun fact: You can deploy Streamlit apps for free on Streamlit Cloud.",
]

# ---------- SIDEBAR ----------
st.sidebar.title("🌌 Choose Your Guide")

category = st.sidebar.selectbox("📂 Topic", list(CATEGORIES.keys()))
personality = st.sidebar.selectbox("🌟 Personality", list(CATEGORIES[category].keys()))
selected = CATEGORIES[category][personality]

st.sidebar.markdown(f"**Tone:** {selected['tone']}")
st.sidebar.markdown("---")

st.sidebar.markdown("**💬 Quick starters:**")
quick_prompt = None
for starter in selected["starters"]:
    if st.sidebar.button(starter, use_container_width=True):
        quick_prompt = starter

st.sidebar.markdown("---")
st.sidebar.caption(random.choice(FUN_FACTS))

# ---------- MAIN AREA ----------
st.title("🌌 AI Multiverse")
st.markdown(f"Currently talking to: **{personality}**")

# ---------- MEMORY VAULT ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_personality" not in st.session_state:
    st.session_state.last_personality = None

# ---------- EMPTY STATE + GREETING ----------
if len(st.session_state.messages) == 0:
    st.info(f"{selected['greeting']}")
elif st.session_state.last_personality != personality:
    st.info(f"**{personality}:** {selected['greeting']}")

st.session_state.last_personality = personality

# ---------- RENDER CHAT HISTORY ----------
for message in st.session_state.messages:
    avatar = selected["avatar"] if message["role"] == "assistant" else "🧑‍💻"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ---------- CHAT INPUT (typed OR quick-reply) ----------
typed_message = st.chat_input("Say something...")
user_message = quick_prompt or typed_message

if user_message:

    first_message_ever = len(st.session_state.messages) == 0

    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_message)

    if first_message_ever:
        st.balloons()

    ai_instructions = f"""
    {selected['prompt']}

    Stay completely in character.
    Keep responses friendly and conversational.

    User message:
    {user_message}
    """

    with st.chat_message("assistant", avatar=selected["avatar"]):
        with st.spinner(selected["spinner"]):
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(ai_instructions)
                st.markdown(response.text)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response.text}
                )
            except Exception as e:
                st.error(f"Error: {e}")
