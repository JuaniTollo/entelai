
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
import streamlit as st

# Access the OpenAI API key: prioritize Streamlit secrets, fallback to environment variables
# Gracefully handle missing secrets.toml
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except FileNotFoundError:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def string_to_stream(text):
    for char in text:
        yield char

def parse_options_to_json(options_text):
    """
    Parse options from a single text input into a JSON-like dictionary.
    """
    options = {}
    lines = options_text.split("\n")
    for line in lines:
        if ")" in line:
            key, value = line.split(")", 1)
            options[key.strip().upper()] = value.strip()
    return options

# Load the .env file
load_dotenv()

# Get the OpenAI API key from environment variables
#openai_api_key = os.getenv('OPENAI_API_KEY')
openai_api_key = OPENAI_API_KEY

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This chatbot answers medical questions using Retrieval-Augmented Generation (RAG) with the language model "
    "**OpenAI/gpt-3.5-turbo-16k**, configured with RAG disabled (**rag=False**). "
    "It relies entirely on the LLM's generative capabilities without retrieving external knowledge, "
    "based on the implementation described in [this paper](https://aclanthology.org/2024.findings-acl.372) presented at ACL 2024."
)

# Ask user for their OpenAI API key if not provided
if not openai_api_key:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.", icon="🗝️")
        st.stop()

from medrag import MedRAG
# Initialize MedRAG with the OpenAI API key
cot = MedRAG(llm_name="OpenAI/gpt-3.5-turbo-16k", rag=False)

# Create a session state variable to store the chat messages.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input fields for question and options
with st.form("chat_form", clear_on_submit=True):
    question = st.text_input("Enter your question:", placeholder="Type your question here...")
    options_text = st.text_area(
        "Enter the options as text (e.g., 'a) Option A\\nb) Option B\\nc) Option C'):",
        placeholder="a) Option A\nb) Option B\nc) Option C\nd) Option D"
    )
    submit_button = st.form_submit_button("Submit")

if submit_button:
    if question and options_text:
        # Parse the input into JSON
        options = parse_options_to_json(options_text)

        # Store and display the current question and options
        st.session_state.messages.append({"role": "user", "content": f"**Question:** {question}\n**Options:** {options}"})
        with st.chat_message("user"):
            st.markdown(f"**Question:** {question}")
            st.markdown(f"**Options (JSON):** {options}")

        # Generate answer using MedRAG
        answer, _, _ = cot.answer(question=question, options=options)

        # Parse the answer into readable components
        try:
            answer_data = eval(answer)  # Convert string output to a dictionary
            step_by_step_thinking = answer_data.get("step_by_step_thinking", "No explanation provided.")
            answer_choice = answer_data.get("answer_choice", "No answer choice provided.")

            # Display the response
            with st.chat_message("assistant"):
                st.markdown("### Step-by-Step Thinking")
                st.markdown(step_by_step_thinking)
                st.markdown("### Final Answer Choice")
                st.markdown(f"**{answer_choice}**")

            # Save response in session state
            st.session_state.messages.append({"role": "assistant", "content": f"### Step-by-Step Thinking\n{step_by_step_thinking}\n### Final Answer Choice\n**{answer_choice}**"})
        except Exception as e:
            st.error(f"Error parsing the response: {e}")
    else:
        st.warning("Please enter both a question and options to proceed.")