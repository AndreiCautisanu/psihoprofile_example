import streamlit as st
import os
import opik
from dotenv import load_dotenv
from llm_service import get_available_models, get_llm_response

# Load environment variables
load_dotenv()

# Check if OpenRouter API key is set
if not os.getenv("OPENROUTER_API_KEY"):
    st.error("OpenRouter API key not found. Please add it to the .env file.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="LLM Psihoprofile Test",
    page_icon="🧠",
    layout="wide"
)

# App title and description
st.title("Psychology LLM Research with Opik")
st.markdown("""
This application demonstrates how to use Opik for LLM observability in psychology research.
You can interact with various LLM models and track metrics using Opik.
""")

# Sidebar for model selection and settings
st.sidebar.title("Settings")

# Model selection
models = get_available_models()
model_options = {model["name"]: model["id"] for model in models}
selected_model_name = st.sidebar.selectbox("Select Model", list(model_options.keys()))
selected_model_id = model_options[selected_model_name]

# System prompt (optional)
st.sidebar.subheader("System Prompt (Optional)")
system_prompt = st.sidebar.text_area(
    "Prompt de context pentru model",
    value="Esti un asistent al unui profesor universitar in psihologie. Vei oferi raspunsuri relevante stiintific, fara opinii neverificate sau nefondate, raspunde prompt prin informatii factuale.",
    height=100
)

# Opik information
st.sidebar.subheader("Opik Observability")
st.sidebar.info("""
Opik is tracking:
- User inputs
- LLM responses
- Model usage
- Token counts
""")

# Main chat interface
st.subheader("Chat Interface")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_prompt = st.chat_input("Type your message here...")

if user_prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    # Get response from LLM
    with st.chat_message("assistant"):
        with st.spinner(f"Getting response from {selected_model_name}..."):
            try:
                # Get response from LLM (this will be tracked by Opik)
                response = get_llm_response(
                    model_id=selected_model_id,
                    prompt=user_prompt,
                    system_prompt=system_prompt
                )
                
                # Display response
                st.markdown(response["content"])
                
                # Add assistant message to chat history
                assistant_message = {
                    "role": "assistant",
                    "content": response["content"],
                    "metadata": {
                        "model": selected_model_id,
                        "total_tokens": response["total_tokens"]
                    }
                }
                
                st.session_state.messages.append(assistant_message)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Display information
st.subheader("Ghid initial")
st.info("""
1. Selectati un model din partea stanga
2. Optional, modificati promptul de context, tot din partea stanga
3. Trimiteti un mesaj catre modelul de limbaj si asteptati raspunsul
4. Verificati existenta informatiilor in proiectul "psihoprofile" din Opik
""")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and Opik for LLM observability in psychology research")
