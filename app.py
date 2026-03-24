import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# 1. Setup & API Initialization
load_dotenv()
# Ensure you have GROQ_API_KEY in your Streamlit secrets or .env file
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_PROMPT = """
You are a caring and cautious AI health assistant for users in rural India.

When a user describes symptoms:
- Respond in a natural, human-like, slightly emotional and supportive tone
- Make the user feel heard (like ChatGPT does)
- Briefly explain possible causes in simple language
- Give practical and easy-to-follow advice
- Clearly mention warning signs

Style:
- Start with a gentle, empathetic sentence (e.g., “It sounds like you're not feeling well”)
- Use short paragraphs for explanation
- Use a few bullet points ONLY for important actions or warning signs
- Add light, relevant emojis (not too many, keep it clean and helpful)
- Keep response around 120–200 words

Safety:
- Do NOT give exact medicines or dosages
- Do NOT diagnose definitively
- If symptoms seem serious, clearly emphasize urgency

Language:
- Respond in the same language as the user (English or Hindi)

End ALWAYS with:
"I am not a doctor. Please consult a healthcare professional or dial 112 immediately."
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
    lang = st.radio("Select Language", ["English", "Hindi"])
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

st.title("SYN Health Symptom Checker")
st.caption("Describe your symptoms for basic guidance. Not a substitute for a doctor.")

st.warning("⚠️ This tool is for informational purposes only. Always consult a real doctor or dial 112 in emergencies.")

# 5. Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
user_input = st.chat_input("Describe your symptoms (e.g., 'I have a headache and fever')")

if user_input:
    # Construct the internal prompt with language context
    full_prompt = f"Language: {lang}\nSymptoms: {user_input}"

    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing symptoms..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        *st.session_state.messages
                    ]
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")

# 6. Footer
st.divider()
st.caption("SYN | Built by a student developer | Not a medical device")
