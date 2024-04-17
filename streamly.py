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

# Website Configuration
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
            
            **GitHub**: https://github.com/rosariogabe/WN-Chatbot-Development-
            
            The AI Assistant named, Winney.
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
    Animation to simulate long running process.
    """
    time.sleep(duration)
    return "Long-running operation completed."

@st.cache_data(show_spinner=False)
def load_and_enhance_image(image_path, enhance=False):
    img = Image.open(image_path)
    if enhance:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.8)
    return img

@st.cache_data(show_spinner=False)
def load_streamlit_updates():
    """Load the latest updates from a local JSON file."""
    try:
        p=""
    except (FileNotFoundError, json.JSONDecodeError):
        return {}



def img_to_base64(image_path):
    """Convert image to base64"""
    with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

@st.cache_data(show_spinner=False)
def on_chat_submit(chat_input, api_key, latest_updates, use_langchain=False):
    
    user_input = chat_input.strip().lower()



    #First we need to initiate conversation with some system instructions 
    if 'conversation_history' not in st.session_state:
        assistant_message = "Hello! I am WiNny. How can I assist you today?"
        
        st.session_state.conversation_history = [
            {"role": "system", "content": "You are WiNny, a specialized AI assistant trained in Insurance in Canada Ontario."},
            {"role": "system", "content": "You work for Whitley Newman."},
            {"role": "system", "content": "Refer any un asked question to the following email: info@whitleyfinancial.com."},
            {"role": "system", "content": "Any question or comment about claims redirect the user to the following url: https://whitleynewman.com/about/claims/report-a-claim/"},
            {"role": "system", "content": "Refer emergency claims to the following contacts : Emergency Claims: 1.844.321.LOSS (5677) and After Hours Claims to: claims@whitleynewman.com"},  
            {"role": "system", "content": "You need to make our customers to feel they’re not only getting good value but getting the right coverage, the right advice; to feel their assets, families and businesses are protected and secure."},
            {"role": "system", "content": "Whitley Newman is well regarded as a market leader in auto, property, life and investments – for both personal and business insurance needs."},
            {"role": "system", "content": "Refer to conversation history to provide context to your reponse."},            {"role": "assistant", "content": assistant_message}
        ]

    #This is where we append the user query or input
    st.session_state.conversation_history.append({"role": "user", "content": user_input})

    #Initiate the variable
    assistant_reply = ""
        
    client = AzureOpenAI(
      azure_endpoint = st.session_state.api_base, 
      api_key=st.session_state.api_key,  
      api_version=st.session_state.api_version
    )    

    message_text = st.session_state.conversation_history

    completion = client.chat.completions.create(
      model="WNChatbotDevelopment", # model = "deployment_name" its using  Azure OpenAI GPT-3.5-Turbo-16k
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
    #In the config.json file we are storing all of the api keys from the environment we are using
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
        initial_bot_message = "I am WiNny, what can I help you with today?"
        st.session_state.history.append({"role": "assistant", "content": initial_bot_message})
        st.session_state.conversation_history = [
            {"role": "system", "content": "You are WiNny, a specialized AI assistant trained to assist with Insurances Policies"},
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

    #convert image to base64 before reading this is for the avatar or persona we design for newman
    def img_to_base64(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    # Displaying sidebar image with glowing effect
    img_path = "imgs/sidebar_streamly_avatar.png"
    img_base64 = img_to_base64(img_path)
    st.sidebar.markdown(
        f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")
    
    #Option for future purpose to diferentiate client and prospect
    mode = st.sidebar.radio("Client/Prospect:", options=["Non an Existing Client", "Existing Client"], index=1)
    use_langchain = st.sidebar.checkbox("Send me an email with the Chat Summary 🦜️🔗 ", value=False)
    st.sidebar.markdown("---")
    show_basic_info = st.sidebar.toggle("Interactions", value=False)

    #Display if checked st.info box
    if show_basic_info:
        st.sidebar.markdown("""
        ### Basic Interactions
        - **Ask About Insurance Policy**.
        - **Recommendation**.
        - **Future pourpose
        """)

    #Checked this in the sidebar for advanced interactions
    show_advanced_info = st.sidebar.toggle("Interactions-Future Quotations-Claims", value=False)

    #Display the st.info box if the checkbox is checked
    if show_advanced_info:
        st.sidebar.markdown("""
        ### Advanced Interactions
        - **Login using Microsoft**.
        - **Quotation**:.
        - **Claims
        - **Assistance with products update**:
        """)

    st.sidebar.markdown("---")
    img_path = "imgs/stsidebarimg.png"
    img_base64 = img_to_base64(img_path)

    st.sidebar.markdown(
        f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
        unsafe_allow_html=True,
    )

    #API Key from st.secrets and validate it
    api_key = "ba93393aa0a84bc790a5d2e60420bc10"#st.secrets["OPENAI_API_KEY"]
    if not api_key:
        st.error("Please add your OpenAI API key to the Streamlit secrets.toml file.")
        st.stop()
    
    if mode == mode:
        chat_input = st.chat_input("Ask me about Insurance updates:")
        if chat_input:
            latest_updates = load_streamlit_updates()
            on_chat_submit(chat_input, api_key, latest_updates, use_langchain)

        for message in st.session_state.history[-20:]:
            role = message["role"]
            
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