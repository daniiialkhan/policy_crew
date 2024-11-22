import streamlit as st
from dotenv import load_dotenv

st.title("Policy Word Agent")

load_dotenv()



from src.ai_researcher.crew import AiResearcher

st.text(AiResearcher().crew())