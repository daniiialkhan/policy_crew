import streamlit as st
from dotenv import load_dotenv

st.title("Policy Word Agent")

load_dotenv()

from src.ai_researcher.crew import AiResearcher

input = st.text_input(label="Enter Query here:")
# input = st.chat_input()
# output = ""
# st.session_state["output"] = ""
# inputs = {
#         # 'query': 'Answer me in list form, tell me the meaning of the following terms: Dividend, Dwelling Property, Derivative.'
#         'query': input
#     }

if st.button("Run Query"):
    if input.strip():
        # Pass the user query to the crew
        try:
            inputs = {'query': input}
            ai_researcher = AiResearcher()
            result = ai_researcher.crew().kickoff(inputs=inputs)
            
            # Display the result
            st.subheader("Output:")
            st.text(result)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query before running.")


