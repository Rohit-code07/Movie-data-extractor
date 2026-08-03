from dotenv import load_dotenv
import streamlit as st

from langchain.chat_models import init_chat_model
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)

load_dotenv()

st.title("ChatBot")

if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="you are teaching assistant")
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)

prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.chat_history.append(("user", prompt))
    st.session_state.messages.append(HumanMessage(prompt))

    with st.chat_message("user"):
        st.write(prompt)

    model = init_chat_model("google_genai:gemini-2.5-flash")
    response = model.invoke(st.session_state.messages)

    st.session_state.messages.append(AIMessage(response.content))
    st.session_state.chat_history.append(("assistant", response.content))

    with st.chat_message("assistant"):
        st.write(response.content)