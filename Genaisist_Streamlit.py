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
    api_version="2023-12-01-preview",
    azure_endpoint="https://genaisistopenai.openai.azure.com/"
)

deployment_name = 'gpt-4o'  # Replace with your actual deployment name

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Streamlit App
st.set_page_config(page_title="Chat with Azure OpenAI", layout="wide")
st.title("InsightBuddy: Productivity Insights from JIRA")
st.markdown("""<style>
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 5px;
        background-color: #ffffff;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    .chat-bubble {
        margin: 10px 0;
        padding: 15px;
        border-radius: 20px;
        max-width: 75%;
        font-size: 16px;
        line-height: 1.4;
        word-wrap: break-word;
    }
    .chat-user {
        background-color: #0078d7;
        color: white;
        text-align: right;
        margin-left: auto;
        animation: fadeIn 0.3s ease-in-out;
    }
    .chat-bot {
        background-color: #f1f1f1;
        color: #333;
        text-align: left;
        margin-right: auto;
        animation: fadeIn 0.3s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .input-container {
        margin-top: 20px;
        text-align: center;
    }
    .send-button {
        background-color: #0078d7;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    .send-button:hover {
        background-color: #005a9e;
    }
</style>""", unsafe_allow_html=True)

# Input container
with st.container():
    st.subheader("Chat")
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "You:", key="input_box", placeholder="Type your message here...", label_visibility="collapsed"
        )
        submit_button = st.form_submit_button("Send", help="Click to send your message")

    if submit_button and user_input.strip():
        # Append user message to chat history
        st.session_state["messages"].append({"sender": "user", "text": user_input.strip(), "time": datetime.now()})

        try:
            # Call AzureOpenAI API for a response
            user_data = "You are a helpful assistant."
            user_query = user_input.strip()
            response = client.chat.completions.create(
                model=deployment_name,
                messages=[
                    { "role": "system", "content": user_data },
                    { "role": "user", "content": user_query }
                ],
                max_tokens=2000
            )
            bot_response = response.choices[0].message.content
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
            f'<strong>{"You" if message["sender"] == "user" else "InsightBuddy"}</strong>: {message["text"]}'
            f'</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# Scroll to the bottom of the chat automatically
st.markdown("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)
