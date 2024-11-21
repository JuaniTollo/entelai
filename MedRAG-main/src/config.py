import streamlit as st
import os
from dotenv import load_dotenv


load_dotenv()

# Access the OpenAI API key: prioritize Streamlit secrets, fallback to environment variables
# Gracefully handle missing secrets.toml
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except FileNotFoundError:
    # Fall back to environment variable if secrets.toml is missing
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    

config = {
	"api_type": "openai",
	"api_base": "YOUR_API_BASE_URL",
	"api_version": "2024-17-10",
	"api_key": f"{OPENAI_API_KEY}"
}