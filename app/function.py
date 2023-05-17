# standard library modules
import os

# third-party modules
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
import pinecone

# local modules
from constants import (
    INDEX_NAME,
    MODEL_NAME,
    OPENAI_API_KEY,
    PINECONE_API_ENV,
    PINECONE_API_KEY,
    TEMPERATURE
)

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
    vectors = Pinecone.from_existing_index(
        INDEX_NAME,
        embeddings
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(
            temperature=TEMPERATURE,
            model_name=MODEL_NAME,
            openai_api_key=OPENAI_API_KEY
        ), retriever=vectors.as_retriever())

    return chain


def conversational_chat(chain, query):

    result = chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))

    return result["answer"]
