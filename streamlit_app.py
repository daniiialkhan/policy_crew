import streamlit as st
from dotenv import load_dotenv
from src.ai_researcher.crew import AiResearcher
import os

# Load environment variables
load_dotenv()

# Streamlit app title
st.title("Policy Word Agent Chatbot")

def format_chat_history(messages):
    """
    Format chat history as a string in the format:
    <role>:<content>,<role>:<content>, ...
    """
    return ",".join([f"{msg['role']}:{msg['content']}" for msg in messages])

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input using st.chat_input
if prompt := st.chat_input("Ask a question:"):
    # Add user's message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process the query with the AiResearcher agent
    try:
        context = format_chat_history(st.session_state.messages)
        ai_researcher = AiResearcher()
        inputs = {"query": prompt,"context":context}
        ai_researcher.crew().kickoff(inputs=inputs)

        # Read the response from 'answer.md'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_file_path = os.path.join(current_dir, 'answer.md')
        if os.path.exists(output_file_path):
            with open(output_file_path, 'r') as f:
                response = f.read()
        else:
            response = "No response generated."

        # Add the AI's response to the session state
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    except Exception as e:
        error_message = f"Error: {e}"
        st.session_state.messages.append({"role": "assistant", "content": error_message})
        with st.chat_message("assistant"):
            st.markdown(error_message)
