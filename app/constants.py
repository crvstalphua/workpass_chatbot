# standard library modules
import os

# thid part modules
from dotenv import (
    find_dotenv,
    load_dotenv
)
import streamlit as st

load_dotenv(find_dotenv())

DOCUMENT = "mdw-handy-guide-english-bahasa-indonesia.pdf"
INDEX_NAME = os.getenv('INDEX_NAME')
MODEL_NAME = 'gpt-3.5-turbo'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_API_ENV = os.getenv('PINECONE_API_ENV')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
TEMPERATURE = 0

# INDEX_NAME == st.secrets["INDEX_NAME"]
# OPENAI_API_KEY == st.secrets["OPENAI_API_KEY"]
# PINECONE_API_ENV == st.secrets["PINECONE_API_ENV"]
# PINECONE_API_KEY== st.secrets["PINECONE_API_KEY"]
