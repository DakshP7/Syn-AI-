import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

st.set_page_config(page_title="SYN Health Checker", page_icon="🏥", layout="centered")
st.markdown("""
<style>
/* Background */
body {
    background-color: #f5f7fb;
}

/* Chat bubbles */
.stChatMessage {
    border-radius: 15px;
    padding: 12px;
    margin-bottom: 8px;
}

/* User message */
[data-testid="stChatMessageContent"]:has(p:contains("user")) {
    background-color: #d1e7ff;
}

/* Assistant message */
[data-testid="stChatMessageContent"] {
    background-color: #ffffff;
}

/* Buttons */
.stButton>button {
    border-radius: 10px;
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
}

/* Input box */
textarea {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)
# Language selector
lang = st.radio("Language", ["English", "Hindi"])


st.title("SYN Health Symptom Checker")
st.caption("Describe your symptoms and get basic health guidance. Not a substitute for professional medical advice.")

st.warning("This tool is for informational purposes only. Always consult a real doctor for medical advice or dial 112.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Describe your symptoms here...")

if user_input:
    prompt = f"Language: {lang}\nSymptoms: {user_input}"

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing symptoms..."):
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

st.divider()
st.caption("SYN | Built by a student developer | Not a medical device | Always see a doctor for serious symptoms")