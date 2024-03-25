import logging
import streamlit as st

from langchain.adapters import openai as lc_openai
from PIL import Image, ImageEnhance
import time
import json
import requests
import base64

import openai 
client = openai

logging.basicConfig(level=logging.INFO)

# Streamlit Page Configuration
st.set_page_config(
    page_title="Streamly Streamlit Assistant",
    page_icon="imgs/avatar_streamly.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://github.com/AdieLaine/Streamly",
        "Report a bug": "https://github.com/AdieLaine/Streamly",
        "About": """
            ## Streamly Streamlit Assistant
            
            **GitHub**: https://github.com/AdieLaine/
            
            The AI Assistant named, Streamly, aims to provide the latest updates from Streamlit,
            generate code snippets for Streamlit widgets,
            and answer questions about Streamlit's latest features, issues, and more.
            Streamly has been trained on the latest Streamlit updates and documentation.
        """
    }
)

# Streamlit Updates and Expanders
st.title("Streamly Streamlit Assistant")

API_DOCS_URL = "https://docs.streamlit.io/library/api-reference"

@st.cache_data(show_spinner=False)
def long_running_task(duration):
    """
    Simulates a long-running operation.
    """
    time.sleep(duration)
    return "Long-running operation completed."

@st.cache_data(show_spinner=False)
def load_and_enhance_image(image_path, enhance=False):
    """
    Load and optionally enhance an image.

    Parameters:
    - image_path: str, path of the image
    - enhance: bool, whether to enhance the image or not

    Returns:
    - img: PIL.Image.Image, (enhanced) image
    """
    img = Image.open(image_path)
    if enhance:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.8)
    return img

@st.cache_data(show_spinner=False)
def load_streamlit_updates():
    """Load the latest Streamlit updates from a local JSON file."""
    try:
        with open("data/streamlit_updates.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

@st.cache_data(show_spinner=False)
def get_latest_update_from_json(keyword, latest_updates):
    """
    Fetch the latest Streamlit update based on a keyword.

    Parameters:
        keyword (str): The keyword to search for in the Streamlit updates.
        latest_updates (dict): The latest Streamlit updates data.

    Returns:
        str: The latest update related to the keyword, or a message if no update is found.
    """
    for section in ["Highlights", "Notable Changes", "Other Changes"]:
        for sub_key, sub_value in latest_updates.get(section, {}).items():
            for key, value in sub_value.items():
                if keyword.lower() in key.lower() or keyword.lower() in value.lower():
                    return f"Section: {section}\nSub-Category: {sub_key}\n{key}: {value}"

    return "No updates found for the specified keyword."

def get_streamlit_api_code_version():
    """
    Get the current Streamlit API code version from the Streamlit API documentation.

    Returns:
        str: The current Streamlit API code version.
    """
    try:
        response = requests.get(API_DOCS_URL)
        if response.status_code == 200:
            return "1.32.0"
    except requests.exceptions.RequestException as e:
        print("Error connecting to the Streamlit API documentation:", str(e))
    return None

def display_streamlit_updates():
    """It displays the latest updates of the Streamlit."""
    with st.expander("Streamlit 1.32 Announcement", expanded=False):
        image_path = "imgs/streamlit128.png"
        enhance = st.checkbox("Enhance Image?", False)
        img = load_and_enhance_image(image_path, enhance)
        st.image(img, caption="Streamlit 1.32 Announcement", use_column_width="auto", clamp=True, channels="RGB", output_format="PNG")
        st.markdown("For more details on this version, check out the [Streamlit Forum post](https://docs.streamlit.io/library/changelog#version-1320).")

def img_to_base64(image_path):
    """Convert image to base64"""
    with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

@st.cache_data(show_spinner=False)
def on_chat_submit(chat_input, api_key, latest_updates, use_langchain=False):
    """
    Handle chat input submissions and interact with the Azure OpenAI GPT.

    Parameters:
        chat_input (str): The chat input from the user.
        api_key (str): The Azure OpenAI GPT API key.
        latest_updates (dict): The latest Streamlit updates fetched from a JSON file or API.
        use_langchain (bool): Whether to use LangChain OpenAI wrapper.

    Returns:
        None: Updates the chat history in Streamlit's session state.
    """
    user_input = chat_input.strip().lower()

    # Initialize the Azure OpenAI GPT
    model_engine = "azure-gpt-3.5-turbo-1106"

    # Initialize the conversation history with system and assistant messages
    if 'conversation_history' not in st.session_state:
        assistant_message = "Hello! I am Streamly. How can I assist you with Streamlit today?"
        formatted_message = []
        highlights
