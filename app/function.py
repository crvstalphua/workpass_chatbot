# standard library modules
import os

# third-party modules
# from dotenv import find_dotenv, load_dotenv
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
import pinecone

# local modules

# load_dotenv(find_dotenv())

os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"]
os.environ["INDEX_NAME"] == st.secrets["INDEX_NAME"]
os.environ["PINECONE_API_KEY"] == st.secrets["PINECONE_API_KEY"]
os.environ["PINECONE_API_ENV"] == st.secrets["PINECONE_API_ENV"]

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
INDEX_NAME = os.getenv('INDEX_NAME')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_API_ENV = os.getenv('PINECONE_API_ENV')

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_API_ENV
)

def start_conversation():
    """
        Embeddings
    """

    # texts = text_splitter.split_text(saved_file)
    embeddings = OpenAIEmbeddings(
        openai_api_key=OPENAI_API_KEY
    )
    vectors = Pinecone.from_existing_index(INDEX_NAME, embeddings)

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(
            temperature=0.0,
            model_name='gpt-3.5-turbo',
            openai_api_key=OPENAI_API_KEY
        ), retriever=vectors.as_retriever())

    return chain


def conversational_chat(chain, query):

    result = chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))

    return result["answer"]