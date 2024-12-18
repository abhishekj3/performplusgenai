import streamlit as st
from openai import AzureOpenAI
import os
from datetime import datetime

# Set up environment variables
os.environ["AZURE_API_KEY"] = "CUCezjchUShB635Ua3YGnJNwScJE3vIGE7yg6qPOZw8JJ0DldvDaJQQJ99ALACYeBjFXJ3w3AAABACOGH3Ff"
os.environ["AZURE_API_ENDPOINT"] = "https://genaisistopenai.openai.azure.com/"

# Initialize AzureOpenAI client
client = AzureOpenAI(
    api_key="CUCezjchUShB635Ua3YGnJNwScJE3vIGE7yg6qPOZw8JJ0DldvDaJQQJ99ALACYeBjFXJ3w3AAABACOGH3Ff",
    api_version="2024-02-01",
    azure_endpoint="https://genaisistopenai.openai.azure.com/"
)

deployment_name = 'gpt-35-turbo'  # Replace with your actual deployment name

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Streamlit App
st.set_page_config(page_title="Chat with Azure OpenAI", layout="wide")
st.title("Chat with Azure OpenAI")
st.markdown("""<style>
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 5px;
        background-color: #f9f9f9;
    }
    .chat-bubble {
        margin: 10px 0;
        padding: 10px;
        border-radius: 10px;
        max-width: 70%;
    }
    .chat-user {
        background-color: #d1e7ff;
        align-self: flex-end;
        margin-left: auto;
    }
    .chat-bot {
        background-color: #f1f0f0;
        align-self: flex-start;
        margin-right: auto;
    }
</style>""", unsafe_allow_html=True)

# Input container
with st.container():
    st.subheader("Chat")
    user_input = st.text_input("You:", "", key="input_box", placeholder="Type your message here...")
    if st.button("Send") and user_input.strip():
        # Append user message to chat history
        st.session_state["messages"].append({"sender": "user", "text": user_input.strip(), "time": datetime.now()})

        try:
            # Call AzureOpenAI API for a response
            response = client.completions.create(
                model=deployment_name,
                prompt=user_input,
                max_tokens=150
            )
            bot_response = response.choices[0].text.strip()
        except Exception as e:
            bot_response = f"An error occurred: {e}"

        # Append bot response to chat history
        st.session_state["messages"].append({"sender": "bot", "text": bot_response, "time": datetime.now()})

# Chat history display
with st.container():
    st.markdown("### Conversation")
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state["messages"]:
        sender_class = "chat-user" if message["sender"] == "user" else "chat-bot"
        st.markdown(
            f'<div class="chat-bubble {sender_class}">'
            f'<strong>{"You" if message["sender"] == "user" else "Azure AI"}</strong>: {message["text"]}'
            f'</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# Scroll to the bottom of the chat automatically
st.markdown("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)
