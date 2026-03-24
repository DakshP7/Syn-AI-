import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# 1. Setup & API Initialization
load_dotenv()
# Ensure you have GROQ_API_KEY in your Streamlit secrets or .env file
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_PROMPT = """
You are a cautious AI health assistant designed for users in rural India.

When a user describes symptoms:
1. List 2–3 possible common causes in simple language
2. Give safe home care advice (only if mild)
3. Clearly mention warning signs requiring a doctor
4. If symptoms seem serious, prioritize urgency
5. Do not give exact medicines or dosages

Format response:
- Possible causes:
- What you can do:
- When to see a doctor:

Keep it under 150 words.

Always respond in user's language (English or Hindi).
Always end with: "I am not a doctor. Please consult a healthcare professional or dial 112 immediately."
"""

# 2. Page Configuration
st.set_page_config(page_title="SYN Health Checker", page_icon="🏥", layout="centered")

# 3. Unified CSS Styling (Fixes the white-on-white text issue)
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
    }

    /* Chat Message Bubbles */
    [data-testid="stChatMessage"] {
        border-radius: 15px;
        margin-bottom: 10px;
        padding: 15px;
    }

    /* Ensure Text is Always Visible (White) */
    [data-testid="stChatMessageContent"] p {
        color: #ffffff !important;
        font-size: 16px;
    }

    /* Assistant Bubble (Dark Grey) */
    [data-testid="stChatMessage"]:has([data-testid="stIconMaterial-smart_toy"]) {
        background-color: #262730 !important;
        border: 1px solid #444;
    }

    /* User Bubble (Deep Blue) */
    [data-testid="stChatMessage"]:has([data-testid="stIconMaterial-person"]) {
        background-color: #1E3A8A !important;
    }

    /* Input Box Styling */
    [data-testid="stChatInput"] textarea {
        background-color: #262730 !important;
        color: white !important;
        border: 1px solid #555 !important;
        border-radius: 10px !important;
    }

    /* Language Radio Buttons */
    .stRadio label {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. Sidebar / Header UI
with st.sidebar:
    st.title("Settings")
    lang =
