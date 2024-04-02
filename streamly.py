import logging
import streamlit as st


from langchain.adapters import openai as lc_openai
from PIL import Image, ImageEnhance
import time
import json
import requests
import base64
import os
from openai import AzureOpenAI
import json

#client = OpenAI()

logging.basicConfig(level=logging.INFO)

custom_css = """
        <style>
        body { background-color: #f7f7f7; }
        .stAppHeader { background-color: #009900;}
        .stAppHeader .title { color: #ffffff;}
        .stSidebar { background-color: #ffffff;}
        .stSidebar .stText { color: #000000; }
        .stPage { background-color: #ffffff;}
        .stFooter { background-color: #009900;}
        .stFooter div, .stFooter a { color: #ffffff;}
        </style>
        """

# Streamlit Page Configuration
st.set_page_config(
    page_title="Whitley-Newman (WN) Chatbot",
    page_icon="imgs/avatar_whitley-newman.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://github.com/rosariogabe/WN-Chatbot-Development-",
        "Report a bug": "https://github.com/users/rosariogabe/projects/1/views/1",
        "About": """
            ## Whitley-Newman (WN) Chatbot
            
            **GitHub**: https://github.com/AdieLaine/
            
            The AI Assistant named, Max-WN.
        """
    }
)

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Streamlit Updates and Expanders
st.title("Whitley-Newman (WN) Chatbot")

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
        p=""
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
    
    user_input = chat_input.strip().lower()



    # Initialize the conversation history with system and assistant messages
    if 'conversation_history' not in st.session_state:
        assistant_message = "Hello! I am WhitNey. How can I assist you today?"
        # Initialize conversation_history
        st.session_state.conversation_history = [
            {"role": "system", "content": "You are WhitNey, a specialized AI assistant trained in Insurance in Canada Ontario."},
            {"role": "system", "content": "Refer to conversation history to provide context to your reponse."},            {"role": "assistant", "content": assistant_message}
        ]

    # Append user's query to conversation history
    st.session_state.conversation_history.append({"role": "user", "content": user_input})

    # Logic for assistant's reply
    assistant_reply = ""
        
    client = AzureOpenAI(
      azure_endpoint = st.session_state.api_base, 
      api_key=st.session_state.api_key,  
      api_version=st.session_state.api_version
    )    

    message_text = st.session_state.conversation_history

    completion = client.chat.completions.create(
      model="WNChatbotDevelopment", # model = "deployment_name"
      messages = message_text,
      temperature=0.7,
      max_tokens=800,
      top_p=0.95,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None
    )

    import json
    completion_response = completion.model_dump_json(indent=2)
    completion_dict = json.loads(completion_response)
    assistant_reply = completion_dict["choices"][0]["message"]["content"]

    # Append assistant's reply to the conversation history
    st.session_state.conversation_history.append({"role": "assistant", "content":assistant_reply})

    # Update the Streamlit chat history
    if "history" in st.session_state:
        st.session_state.history.append({"role": "user", "content": user_input})
        st.session_state.history.append({"role": "assistant", "content": assistant_reply})

def main():
    # Initialize session state variables for chat history and conversation history
    with open(r'config.json') as config_file:
        config_details = json.load(config_file)
    
    chatgpt_model_name = config_details['CHATGPT_MODEL']
    
    if "api_key" not in st.session_state:
        st.session_state.api_key = config_details['OPENAI_API_KEY']
        st.session_state.api_base = config_details['OPENAI_API_BASE']
        st.session_state.api_version = config_details['OPENAI_API_VERSION']
        st.session_state.api_type = "azure"

    if "history" not in st.session_state:
        st.session_state.history = []
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
        initial_bot_message = "I am WhitNey, what can I help you with today?"
        st.session_state.history.append({"role": "assistant", "content": initial_bot_message})
        st.session_state.conversation_history = [
            {"role": "system", "content": "You are WhitNey, a specialized AI assistant trained to assist with Insurances Policies"},
            {"role": "system", "content": "Refer to conversation history to provide context to your reponse."},
            {"role": "system", "content": "Use the streamlit_updates.json local file to look up the latest Streamlit feature updates."},
            {"role": "assistant", "content": initial_bot_message}
        ]
    
    
    # Inject custom CSS for glowing border effect
    st.markdown(
        """
        <style>
            .cover-glow {
                width: 100%;
                height: auto;
                padding: 5px;
                box-shadow: 
                    0 0 5px #003300,
                    0 0 10px #006600,
                    0 0 15px #009900,
                    0 0 20px #00CC00,
                    0 0 25px #00FF00,
                    0 0 30px #33FF33,
                    0 0 35px #66FF66;
                position: relative;
                z-index: -1;
                border-radius: 20px;  /* Rounded corners */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Function to convert image to base64
    def img_to_base64(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    # Load and display sidebar image with glowing effect
    img_path = "imgs/sidebar_streamly_avatar.png"
    img_base64 = img_to_base64(img_path)
    st.sidebar.markdown(
        f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")
    
    # Sidebar for Mode Selection
    mode = st.sidebar.radio("Client/Prospect:", options=["Non an Existing Client", "Existing Client"], index=1)
    use_langchain = st.sidebar.checkbox("Send me an email with the Chat Summary 🦜️🔗 ", value=False)
    st.sidebar.markdown("---")
    # Toggle checkbox in the sidebar for basic interactions
    show_basic_info = st.sidebar.toggle("Show Basic Interactions", value=True)

    # Display the st.info box if the checkbox is checked
    if show_basic_info:
        st.sidebar.markdown("""
        ### Basic Interactions
        - **Ask About Streamlit**: Type your questions about Streamlit's latest updates, features, or issues.
        - **Search for Code**: Use keywords like 'code example', 'syntax', or 'how-to' to get relevant code snippets.
        - **Navigate Updates**: Switch to 'Updates' mode to browse the latest Streamlit updates in detail.
        """)

    # Add another toggle checkbox in the sidebar for advanced interactions
    show_advanced_info = st.sidebar.toggle("Show Advanced Interactions", value=False)

    # Display the st.info box if the checkbox is checked
    if show_advanced_info:
        st.sidebar.markdown("""
        ### Advanced Interactions
        - **Generate an App**: Use keywords like **generate app**, **create app** to get a basic Streamlit app code.
        - **Code Explanation**: Ask for **code explanation**, **walk me through the code** to understand the underlying logic of Streamlit code snippets.
        - **Project Analysis**: Use **analyze my project**, **technical feedback** to get insights and recommendations on your current Streamlit project.
        - **Debug Assistance**: Use **debug this**, **fix this error** to get help with troubleshooting issues in your Streamlit app.
        """)

    st.sidebar.markdown("---")
    # Load image and convert to base64
    img_path = "imgs/stsidebarimg.png"  # Replace with the actual image path
    img_base64 = img_to_base64(img_path)



    # Display image with custom CSS class for glowing effect
    st.sidebar.markdown(
        f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
        unsafe_allow_html=True,
    )

    # Access API Key from st.secrets and validate it
    api_key = "ba93393aa0a84bc790a5d2e60420bc10"#st.secrets["OPENAI_API_KEY"]
    if not api_key:
        st.error("Please add your OpenAI API key to the Streamlit secrets.toml file.")
        st.stop()
    
    # Handle Chat and Update Modes
    if mode == mode:
        chat_input = st.chat_input("Ask me about Streamlit updates:")
        if chat_input:
            latest_updates = load_streamlit_updates()
            on_chat_submit(chat_input, api_key, latest_updates, use_langchain)

        # Display chat history with custom avatars
        for message in st.session_state.history[-20:]:
            role = message["role"]
            
            # Set avatar based on role
            if role == "assistant":
                avatar_image = "imgs/avatar_streamly.png"
            elif role == "user":
                avatar_image = "imgs/stuser.png"
            else:
                avatar_image = None  # Default
            
            with st.chat_message(role, avatar=avatar_image):
                st.write(message["content"])



if __name__ == "__main__":
    main()