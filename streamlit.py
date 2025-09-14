import streamlit as st
import requests

FASTAPI_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="💬 Gemini Chatbot", page_icon="💬")

# Page title
st.title("💬 Gemini Chatbot")
st.write("Talk to the chatbot powered by Gemini API")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Function to send message
def send_message():
    user_message = st.session_state.user_message.strip()
    if not user_message:
        return
    try:
        response = requests.post(FASTAPI_URL, json={"message": user_message})
        if response.status_code == 200:
            bot_response = response.json()["response"]
            st.session_state.messages.append({"role": "user", "text": user_message})
            st.session_state.messages.append({"role": "bot", "text": bot_response})
        else:
            st.error(f"Error: {response.json()['detail']}")
    except Exception as e:
        st.error(f"Could not connect to backend: {e}")

    # Clear input safely inside callback
    st.session_state.user_message = ""

# Input field at the bottom
st.text_input(
    "Enter your message:",
    key="user_message",
    placeholder="Type your message and press Enter...",
    autocomplete="off",
    on_change=send_message
)

# Display chat history (text form, newest first)
for msg in reversed(st.session_state.messages):
    if msg["role"] == "user":
        st.write(f"🧑 You: {msg['text']}")
    else:
        st.write(f"👽 Bot: {msg['text']}")

# Autofocus
st.components.v1.html(
    """
    <script>
    const input = window.parent.document.querySelector('input[type="text"]');
    if (input) { input.focus(); }
    </script>
    """,
    height=0,
    width=0
)
