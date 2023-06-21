# standard library modules
import os

# thid part modules
from dotenv import (
    find_dotenv,
    load_dotenv
)
import streamlit as st

load_dotenv(find_dotenv())

DOCUMENT = "Combined_MDW_OCR_16Jun23.pdf"
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
