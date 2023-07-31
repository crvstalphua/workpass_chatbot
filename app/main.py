# standard library modules
import os
import re

# third-party modules
import streamlit as st
from streamlit_chat import message
from dotenv import (
    find_dotenv,
    load_dotenv
)
from langdetect import detect
from langdetect import DetectorFactory

# local modules
from function import (
    conversational_chat,
    start_conversation
)

load_dotenv(find_dotenv())

# To enforce consistent results for langdetect
DetectorFactory.seed = 0

# Default text
generated_session_text = "Hello! I'm your guide for migrant domestic workers. Ask me anything!"
past_session_text = "Hey ! 👋"
welcome_text = "How would you like us to help you today?"
button_text = "Send"

# Conditional response
default_response = "Return your response in English. Respond with 'I'm sorry, I don't have the information.' if you don't have the inro."
mandarin_response = "Return your response in Mandarin. Respond with '我很抱歉，但我没有可用的细节。' if you don't have the info."
malay_response = "Return your response in Bahasa Malay. Respond with 'Maaf, tetapi saya tidak mempunyai maklumat.' if you don't have the info."

# Language Mapping
chinese_mapping = ["zh-cn", "zh-tw", "ko"]
malay_mapping = ["ms", "id"]

if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = [generated_session_text]

if 'past' not in st.session_state:
    st.session_state['past'] = [past_session_text]

chain = start_conversation()

# container for the chat history
response_container = st.container()

# container for the user's text input
container = st.container()

with container:
    with st.form(key='sgwp', clear_on_submit=True):

        user_input = st.text_input(
            welcome_text,
            max_chars=200
        )
        send_button = st.form_submit_button(label=button_text)

        with st.spinner('loading...'):
            if send_button and user_input:
                lang = detect(user_input)
                if lang in chinese_mapping:
                    response_text = f'{user_input}. {mandarin_response}'
                elif lang in malay_mapping:
                    response_text = f'{user_input}. {malay_response}'
                else:
                    response_text = f'{user_input}. {default_response}'

                output = conversational_chat(
                    chain,
                    response_text
                )
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

    if st.button('Reset this conversation?'):
        st.session_state['history'] = []
        st.session_state['past'] = [past_session_text]
        st.session_state['generated'] = [generated_session_text]


if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="personas")
            message(st.session_state["generated"][i], key=str(i), avatar_style="bottts")
