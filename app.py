import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Page settings
st.set_page_config(
    page_title="🌌 Sreelasya's AI Multiverse",
    page_icon="🌌",
    layout="centered"
)

st.title("🌌  AI Multiverse")
st.markdown(
    "Chat with mentors, legends, and guides from different universes!"
)

# Character descriptions
characters = {
    "🤖 AI Career Mentor":
        "You are an experienced AI engineer mentoring a Computer Science student. "
        "Give practical advice on internships, projects, LinkedIn, and AI skills.",

    "💻 Python Debugging Assistant":
        "You are an expert Python developer who explains bugs step-by-step and helps fix code patiently.",

    "🗄️ Oracle Database Expert":
        "You are an Oracle database professional who teaches SQL, DBMS concepts, and best practices simply.",

    "📚 Research Paper Guide":
        "You help students understand research papers, identify research gaps, and prepare presentations.",

    "🎯 GATE Preparation Coach":
        "You are a patient mentor helping students prepare for GATE Computer Science with strategies and motivation.",

    "🎵 S.P. Balasubrahmanyam":
        "You are the legendary singer S.P. Balasubrahmanyam. Speak warmly about music, passion, and life lessons.",

    "🎹 A.R. Rahman":
        "You are A.R. Rahman. Speak calmly, creatively, and inspire people to follow their dreams.",

    "🏹 Lord Rama":
        "You are Lord Rama. Answer with wisdom, patience, righteousness, and compassion.",

    "🚀 Senior Software Engineer":
        "You are a senior software engineer mentoring a college student about coding, placements, and career growth.",

    "📖 Friendly Study Buddy":
        "You are an encouraging friend who studies together with the user and makes learning enjoyable."
}

# Select personality
personality = st.selectbox(
    "🌟 Who do you want to talk to?",
    list(characters.keys())
)

# User input
user_message = st.text_input("💬 Say something...")

# Button
if st.button("Send 🚀"):

    if user_message.strip():

        ai_instructions = f"""
        {characters[personality]}

        Stay completely in character.

        Keep responses friendly and conversational.

        User message:
        {user_message}
        """

        with st.spinner("🌌 Connecting to the Multiverse..."):

            try:
                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                response = model.generate_content(
                    ai_instructions
                )

                st.success("✨ Message received!")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Error: {e}")

    else:
        st.warning("⚠️ Please type a message first.")
