__import__('pysqlite3')
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from dotenv import load_dotenv
from src.ai_researcher.crew import PolicyAgenticRAG
import os


# Load environment variables
load_dotenv()
# Function to switch pages
def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()  # Force the app to rerun immediately

# Set up session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'Page 1'  # Default to the first page

def page_1():
    st.title("📄 Policy Word Explainer")
    # Upload Folder Configuration
    UPLOAD_FOLDER = "uploaded_files"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if it doesn't exist
    
    # Instructions
    st.subheader("Instructions:")
    st.markdown(
        """
        1. Click **Browse files** to upload a PDF file.
        2. Wait until the upload completes.
        3. You can overwrite the file by uploading a new one.
        4. Only **one PDF** is allowed at a time.
        5. After uploading the file, press Proceed to Next Page
        """,
    
    )
    
    # Upload PDF File
    uploaded_file = st.file_uploader(
        "Upload a single PDF file below (max 200 MB).",
        type=["pdf"],
        accept_multiple_files=False,
        help="Drag and drop a PDF file or click Browse files.",
    )
    
    if uploaded_file:
        with st.spinner("Uploading your file..."):
            # Save the uploaded file as 'uploaded.pdf' inside UPLOAD_FOLDER
            file_path = os.path.join(UPLOAD_FOLDER, "uploaded.pdf")
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            st.success("🎉 File uploaded successfully!")
    
        # Show File Details
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # File size in MB
        st.info(f"**File Name:** {uploaded_file.name}")
        st.info(f"**File Size:** {file_size:.2f} MB")
    
        # Next Page Button
        st.markdown("---")
        if st.button("Proceed to Next Page ➡️"):
            go_to_page("Page 2")
            # st.success("✅ Next page functionality is coming soon!")
    else:
        st.warning("Please upload a PDF file to proceed.")
    
    # Footer
    st.markdown("---")

def page_2():
    # Streamlit app title
    st.title("📄 Policy Word Explainer")

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

        # Process the query with the PolicyAgenticRAG agent
        try:
            print("Trying...")
            context = format_chat_history(st.session_state.messages)
            ai_researcher = PolicyAgenticRAG()
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


# Render the current page
if st.session_state.page == 'Page 1':
    page_1()
elif st.session_state.page == 'Page 2':
    page_2()
