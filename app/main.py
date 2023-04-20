# standard library modules
import os
import re

# third-party modules
import streamlit as st
from streamlit_chat import message
from langdetect import detect
from langdetect import DetectorFactory
# from dotenv import find_dotenv, load_dotenv

# local modules
from function import conversational_chat, start_conversation

# load_dotenv(find_dotenv())


DetectorFactory.seed = 0
os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"]
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hello! I'm your guide for migrant domestic workers. Ask me anything!"]

if 'past' not in st.session_state:
    st.session_state['past'] = ["Hey ! 👋"]

# Chinese character Unicode range: \u4e00-\u9fff
chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')

chain = start_conversation()

# container for the chat history
response_container = st.container()
# container for the user's text input
container = st.container()

with container:
    with st.form(key='sgwp', clear_on_submit=True):

        welcome_text = "How would you like us to help you today?"
        mandarin_welcome = "用普通话和我交谈"
        button_text = 'Send'

        user_input = st.text_input(
            welcome_text,
            max_chars=200
        )
        button_text = 'Send'
        send_button = st.form_submit_button(label=button_text)

        with st.spinner('loading...'):
            if send_button and user_input:
                lang = detect(user_input)
                if lang == "zh-cn" or lang == "zh-tw":
                    response_text = f'{user_input}. Return your response in Mandarin. If you don"t have the info, just respond with "我很抱歉，但我没有可用的细节。"'
                elif lang == "ms":
                    response_text = f'{user_input}. Return your response in Bahasa Malay. If you don"t have the info, just respond with "Maaf, tetapi saya tidak mempunyai maklumat."'
                else:
                    response_text = f'{user_input}. If you don"t have the info, just respond with "I am sorry but I do not have the information."'

                print("response_text", response_text)

                output = conversational_chat(
                    chain,
                    response_text
                )
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)


    if st.button('Reset this conversation?'):
        st.session_state['history'] = []
        st.session_state['past'] = ["Hey ! 👋"]
        st.session_state['generated'] = ["Hello! I'm your guide for migrant domestic workers. Ask me anything!"]


if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="adventurer")
            message(st.session_state["generated"][i], key=str(i), avatar_style="bottts")