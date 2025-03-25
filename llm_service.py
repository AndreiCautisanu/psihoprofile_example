import os
from typing import List, Dict, Any, Optional
import opik
from opik.integrations.openai import track_openai
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
os.environ["OPIK_API_KEY"] = "6dJsjTs0Q3IkZza7ifYfC1Rtv"
os.environ["OPIK_PROJECT_NAME"] = "psihoprofile"

# Initialize OpenAI client for OpenRouter
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# Track OpenRouter client with Opik
tracked_client = track_openai(client)

def get_available_models() -> List[Dict[str, str]]:
    """
    Get a list of popular models available on OpenRouter.
    
    Returns:
        A list of dictionaries containing model information
    """
    # List of popular models with their display names
    models = [
        {"id": "anthropic/claude-3-opus", "name": "Claude 3 Opus"},
        {"id": "anthropic/claude-3-sonnet", "name": "Claude 3 Sonnet"},
        {"id": "anthropic/claude-3-haiku", "name": "Claude 3 Haiku"},
        {"id": "google/gemini-pro", "name": "Gemini Pro"},
        {"id": "openai/gpt-4-turbo", "name": "GPT-4 Turbo"},
        {"id": "meta-llama/llama-3-70b-instruct", "name": "Llama 3 70B"},
        {"id": "meta-llama/llama-3-8b-instruct", "name": "Llama 3 8B"},
        {"id": "mistralai/mistral-large", "name": "Mistral Large"},
        {"id": "mistralai/mistral-medium", "name": "Mistral Medium"},
    ]
    
    return models

@opik.track()
def get_llm_response(model_id: str, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
    """
    Get a response from an LLM model via OpenRouter API with Opik tracking.
    
    Args:
        model_id: The ID of the model to use
        prompt: The user prompt to send to the model
        system_prompt: Optional system prompt to set context
        
    Returns:
        A dictionary containing the response and metadata
    """
    if not OPENROUTER_API_KEY:
        raise ValueError("OpenRouter API key not found. Please check your .env file.")
    
    # Prepare the messages
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    # Make the API request with tracked client
    try:
        # This call will be automatically tracked by Opik
        response = tracked_client.chat.completions.create(
            model=model_id,
            messages=messages
        )
        
        # Extract the response content
        content = response.choices[0].message.content
        
        # Return the response and metadata
        return {
            "content": content,
            "model": model_id,
            "total_tokens": response.usage.total_tokens if response.usage else 0
        }
        
    except Exception as e:
        # Re-raise the exception
        raise
